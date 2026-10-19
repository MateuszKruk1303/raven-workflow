---
name: raven-medusa-ecommerce-init
description: "Initialize or complete a local Medusa + Next.js monorepo from the official starter: Docker Compose, envs, migrations, seed, admin and a working storefront. Use to prepare the ecommerce environment before product implementation; not for production deployment."
argument-hint: "[shop-name]"
---

# Raven Medusa Ecommerce Init

Set up a complete development environment in the current project directory. By default the apps run on the host with hot reload, and PostgreSQL and Redis in Docker Compose. Every shop is a separate app, repository and data set. This workflow is what gets reused. Talk to the user in their language.

## Result

- The official Medusa starter: backend and Admin in `apps/backend`, Next.js in `apps/storefront`, a shared workspace and lockfile.
- Compatible Node LTS and pnpm versions recorded in the project; the starter's orchestration preserved.
- PostgreSQL and Redis with healthchecks and durable, isolated volumes.
- Real local env files, safe secrets, an admin account and the storefront's publishable key.
- Migrations, a sample catalog, region, prices, local delivery and local checkout with the manual/system payment provider available in the chosen version.
- Commands for setup, development, stopping and resuming, and a verified product → cart → order flow.

Do not add a second backend, ORM, auth system, CMS or your own ecommerce framework. Do not implement a specific shop's requirements, courier integrations, live payments or production infrastructure. Do not run `raven-init-stack`: that is a different stack. Creating or editing this skill alone is not an order to initialize the application.

## 1. Recognize the project and the current starter

Read the local AGENTS.md and CLAUDE.md, existing manifests and project findings. Keep `context/`, agent instructions, `.git` and user files. A PRD or other Raven skills are not a precondition. Derive the name from the project or the user's argument; reduce it to a valid slug, do not interpret it as a path or shell code.

Before generating, check the current sources:

- [Next.js starter](https://docs.medusajs.com/resources/nextjs-starter)
- [create-medusa-app](https://docs.medusajs.com/resources/create-medusa-app)
- [Official DTC starter](https://github.com/medusajs/dtc-starter)
- [Docker](https://docs.medusajs.com/learn/installation/docker)

Use the official monorepo the current documentation points to. Do not choose the historical, separate `nextjs-starter-medusa` if the documentation marks it as deprecated. Check the starter's real `engines`, `packageManager`, scripts, envs and configuration: package requirements may be stricter than the general installation page.

Check Git, a compatible Node, pnpm, Docker Compose v2, a running daemon and port availability. Do not change the global toolchain of other projects. Use the existing version manager or name the concrete gap. When Docker does not run, you may prepare the files, but do not claim a completed setup.

Resolve and record a specific generator version, check its `--help`. Example direction, only after confirming the flags:

```sh
pnpm dlx create-medusa-app@<cli-version> <name> --with-nextjs-starter --skip-db --no-browser --use-pnpm
```

The generator's `--version` may set the Medusa package version; do not treat that flag as just printing the CLI version. `--directory-path` may mean the project's parent directory. Check the semantics instead of guessing.

## 2. Create or complete the monorepo

For a new project generate the starter in a separate temporary directory outside the target repository. Compare paths and move the result into the current directory, without nesting the whole project in an extra folder. Do not copy `.git`, `node_modules` or build artifacts. Install dependencies in the target location. Merge existing files instead of overwriting them blindly; check symlink targets before writing.

For an existing Medusa monorepo complete the missing elements without regeneration, automatic upgrade or secret rotation. If the directory contains another application or a conflict cannot be merged safely, present the concrete conflict. Do not delete the project to force the CLI to run. After a failure fix the cause before retrying; do not repeat generation on a partial result.

Keep the official starter's workspace names and structure, set a private root workspace. Initialize Git only if the directory does not belong to a repository/worktree; do not automatically commit, push or create a remote repository. Stop only your own generator processes, if the CLI left them running.

## 3. Wire up infrastructure and envs

Read [local-development.md](references/local-development.md) when configuring services, envs and seeding. Use [compose.local.yaml](assets/compose.local.yaml) and [compose.env.example](assets/compose.env.example) as the base; adapt them to the existing project and confirmed versions.

Create both tracked templates and real ignored env files. Default ports: storefront 8000, backend/Admin 9000, PostgreSQL 5432, Redis 6379, Admin HMR 5173 if used. On a collision pick a free port and consistently change commands, URLs, CORS and upload configuration. Do not kill other processes. A `PORT` entry alone is not enough: confirm the script reads it.

Configure Redis in Medusa code, not only in env: sessions and the native Redis event bus, per the current APIs. Keep the starter's other modules. Configure a local file provider without an S3 dependency. Generate secrets randomly and keep them on a retry.

## 4. Prepare data and convenient commands

Check the Compose configuration without printing secrets, start the services and wait for healthchecks with a bounded wait time. Before migrations and seed confirm that the effective `DATABASE_URL` points to this project's local database, not an inherited external one. Use the official migration and seeding mechanisms of the chosen version.

Provide an admin, a catalog, a region with prices, a sales channel, stock levels and a delivery option and local payment sufficient for an order. The publishable key must be linked to the right channel and written to the storefront's env. Write the sign-in data to an ignored file with restricted access; in the report give its path, not the password.

The setup must be safe on a repeated and partial run. Do not assume the official seed is idempotent: check its code and the real entities before creating. Do not treat any product or a marker file alone as evidence of a full bootstrap. Do not reset existing passwords, orders, keys or volumes. Do not mask connection errors as "already exists".

Add or adapt root workspace commands:

| Command | Behavior |
|---|---|
| `pnpm run setup` | Dependencies/infrastructure, local envs, migrations and a safe bootstrap; can be retried |
| `pnpm dev` | Ensures running infrastructure, starts backend and storefront with hot reload; no reseeding |
| `pnpm infra:up` | Starts PostgreSQL and Redis, waits for readiness |
| `pnpm infra:down` | Stops Compose, keeping data |
| `pnpm infra:logs` | Service logs |
| `pnpm db:migrate` | Migrations of the local database |
| `pnpm db:seed` | Safe bootstrap of development data |

Keep existing equivalents and the orchestrator if they meet this contract. Run scripts with the right cwd/env and propagate errors. `Ctrl+C` should end both own app processes; describe that the infrastructure stays running until `infra:down`. Do not add an elaborate process manager. A data reset, if described, must be a separate, explicitly destructive operation; never run it as setup verification.

## 5. Verify readiness

Do not stop at files existing. Check:

1. Healthy containers, the backend health endpoint, availability of Admin and storefront, correct admin sign-in.
2. The Store API accepts the publishable key, the storefront shows products and prices in the right region.
3. In the browser: product → variant → cart → checkout with local delivery and manual/system payment → saved order. Do not make a real payment. Report missing UI or browser support; an API test is not evidence of the UI flow.
4. Upload of a local image through Medusa and its display; hot reload of backend and storefront.
5. A second `pnpm run setup` does not duplicate data or keys. Stopping and restarting keep the admin, catalog, order and upload. Never `down -v` or `docker system prune`.
6. Existing typecheck/build checks adequate to the changes. Do not add a full test framework just for initialization.

Write a short start guide in the project README: versions, commands, URLs, env and sign-in data locations, stopping/resuming, checks done and gaps. Do not write secrets. The setup alone does not mean a business roadmap task is done or production readiness.

In the answer give the start command, the storefront and Admin URLs, the sign-in data location and the verification result. Clearly mark checks not run and blockers; a manual local checkout does not mean online payments are connected.
