---
name: raven-init-stack
description: "Initialize the Raven stack with Better T Stack in the current folder, after a short architecture interview based on the PRD. Prepare local PostgreSQL in Docker Compose and record decisions, configuration and verification in context/foundation/tech-stack.md. Use for raven-init-stack or preparing this project stack."
argument-hint: "<app-name>"
---

# Raven Init Stack

Invocation: `/raven-init-stack <app-name>`, e.g. `/raven-init-stack equi-sell`. Talk to the user in their language; write tech-stack.md in the user's language unless the project already uses another.

Take the name as the application name and the workspace package prefix, not as a path. If the user did not give it and did not state it unambiguously in the current instruction, add the name question to the interview below. Use kebab-case, e.g. `equi-sell`; do not treat the argument as shell code. Do not rename the user's folder.

## PRD and architecture decisions — before generating

Read `context/foundation/prd.md`, the existing `tech-stack.md`, the repository instructions and findings available from the conversation. Analyze the requirements first, only then ask questions. If the PRD does not exist, ask for its location or a short product description; do not invent requirements. The user may consciously request just the base skeleton without a PRD.

The user acts as the architect. Run a short interview: a few significant questions that follow from the product, 1–3 per turn, with the `AskUserQuestion` tool. Do not use a universal questionnaire and do not re-ask settled decisions. With every question point to the PRD requirement, a recommendation and a short reason or trade-off. Example topics, only when they apply:

- Images and files: where do we store files — e.g. S3/R2-compatible storage or a local disk — and does the database keep only metadata? How should development work?
- Access: does the product need sign-in, or is it a personal localhost tool? Do not add accounts just because the starter supports them.
- Long operations, agent processes and realtime: what runs outside an HTTP request, how does it survive closing the page and restarting the app?
- Integrations and data: what is the source of truth, which services are needed from the start, what can be deferred?

Allow the answers "I don't know", "propose" and "let's defer". With uncertainty, present a recommendation and let the user accept or change it; silence alone is not consent. If the user explicitly delegates a specific choice, choose and record the justification. Do not block the skeleton on integrations that can be added later. Decisions affecting generation must be settled before it; for a deferred decision agree on a minimal variant that allows starting.

Collect the result in a short summary in chat and in `tech-stack.md`: decision, status (approved / proposal / deferred), justification and consequence for initialization. Do not add a separate acceptance ritual if the answers already settled the choices. Decisions concern this project; writing to global preferences needs the user's separate consent. Do not rework the PRD or implement product features within this interview.

## Generating the skeleton

The base is Next.js, Hono, Bun, tRPC, PostgreSQL, Drizzle and Turborepo. Use Better Auth when the findings include sign-in; for an agreed absence of sign-in choose the variant without auth. Agree on other deviations from the base instead of changing the stack yourself. Check the options of the current CLI before using changed flags.

After the interview run the command below in the current directory, adjusting auth to the findings. `--db-setup none` leaves the local database setup to the Docker Compose step below:

```sh
bun create better-t-stack@latest . --frontend next --backend hono --runtime bun --api trpc --auth better-auth --payments none --database postgres --orm drizzle --db-setup none --package-manager bun --no-git --web-deploy none --server-deploy none --install --addons turborepo --examples none
```

- The `.` argument means the current directory as the project root. Do not create an extra parent directory or a temporary subdirectory for the skeleton. The generator initially derives the package name from the current folder name; after generating, adjust it to the skill argument per the instruction below. The standard monorepo directories `apps/` and `packages/` are created directly in it.
- Check that Bun is available and the contents of the current folder. If Bun is not available, report it. Initialize an empty folder right away. If it contains earlier files, check for collisions: keep `.git/`, `context/` and project instructions. For non-colliding files choose merging (`merge` / `--directory-conflict merge`); do not choose cleaning (`overwrite`) or a new directory name (`increment`). Merging does not guarantee protection of colliding files: if an app or generator target files already exist, name the concrete collisions and agree on how to handle them before running.
- Do not add `--yes`: Better T Stack rejects combining that flag with its own stack options. If the generator asks about opening an editor, choose `Not now`, unless the user asked to open it.
- Wait for the installation to finish. Handle permission or network errors according to the environment rules. On another error keep the partial files and report the cause; do not run further attempts overwriting the directory and do not change the stack yourself.
- The project stays in the invocation folder. Do not change the working directory to the parent and do not use the workaround of generating into a subdirectory. After initialization, create or deliberately update `context/foundation/tech-stack.md` per the rules below. Do not change other documentation of an existing project without an additional instruction.
- After generating, give the application the name from the argument. If it differs from the name derived by the CLI, change the root `package.json.name`, the scope of generated packages (e.g. `@horse-market/db` → `@equi-sell/db`), workspace dependencies, imports, exports and references in generated configs, scripts and UI metadata. Keep the `web` and `server` task/app names. Limit changes to files created by the generator: do not do a global replace in existing documentation, secrets, node_modules or build artifacts. In `bts.jsonc` the reproduce command must still point to `.` as the directory; do not change it to the app name.
- After renaming, run `bun install` to sync the lockfile and workspace links, then `bun run check-types` if the script exists. Do not treat changing only the root package.json as completed renaming.
- On success, check the root package name, scope/import consistency and the presence of `package.json` and `bts.jsonc` in the invocation directory. Then prepare the local database and write the stack document per the rules below. Generator success alone does not confirm that auth or the database connection works.

This skill creates the skeleton and installs the chosen dependencies. It does not create cloud services, deploy the application or run migrations on an existing database.

## Local PostgreSQL in Docker Compose

This step is part of initialization. Create `compose.yaml` in the root or complete the existing Compose configuration, keeping its services and data. On a re-run, reuse the existing PostgreSQL service if it meets the findings; do not create a second container or a new volume instead of the existing one.

- Use the official PostgreSQL image with an explicit, compatible major version, not `latest`. Check the image's current documentation for the chosen version, in particular the data mount path. Add a named volume and a healthcheck with `pg_isready`.
- Expose the port only on `127.0.0.1`. Check whether the host port is taken and on a collision pick a free one, updating the application's connection. Do not set a global `container_name` or a global volume name; rely on Compose project isolation, accounting for parallel projects and worktrees.
- Prepare local credentials and a consistent connection configuration in the env files the generated app actually reads. For Bun running on the host use localhost and the host port. Distinguish the env file read by Compose from the app's env file; check that both use the same data. Do not overwrite existing secrets or a remote `DATABASE_URL`; on a conflict agree on the local configuration.
- Add a safe `.env.example` and the right `.gitignore` entries. Do not write passwords or connection strings with credentials into documentation, chat or tool logs. Do not display the expanded Compose configuration; validate with a variant that does not print values.
- Check that Docker Compose and a running daemon are available. Validate the configuration and start only the database service (`docker compose up -d <service>` with the right file/project if needed). Wait for the healthcheck with a bounded time, then check the connection from a host process through the app configuration and a simple `SELECT 1`. A healthy container alone does not prove a correct app connection.
- If Docker is unavailable, prepare the files and mark the start and connection check as not run. Give the concrete user action and the resume command; do not claim full success and do not install Docker within this skill.
- On a confirmed new, empty development database, apply the generated schema through the project's existing script if it is needed to start. On an existing database do not run migrations or resetting operations within this skill. Do not use `down -v`, do not delete volumes and do not change the image version of an existing database without an agreed migration. Changing the image's init variables does not change the password in an existing volume.

In the final handoff in chat give the real commands to start and stop the local database without deleting data and to start the app, the connection check result and any missing step. Do not send the user only to the documentation. Do not add E2E within initialization.

## Writing tech-stack.md automatically

Writing `context/foundation/tech-stack.md` is part of this skill, not a separate optional step. The initialization invocation also authorizes this write — do not ask again for consent to document the result.

### Before initialization

If the document exists, read it together with the applicable project instructions and check manual/uncommitted changes. Keep decisions, justifications and integration information. Resolve a significant contradiction between the chosen set and the approved stack or project requirements before running the generator; do not overwrite decisions with the default configuration. The document is not evidence that dependencies are already installed.

### After initialization

Create a missing `context/foundation/` without initializing other workflow folders. Build the document from the real `package.json`, workspace manifests, lockfile, `bts.jsonc`, generated configs and results of commands run. Do not copy just the planned generator command as a description of the state.

The document contains:

- **Project and state** — name, update date and initialization state: planned, partial or completed. "Completed" also requires a started and verified local database.
- **Stack** — a table: area, technology, role in the app, version and source. Cover frontend, backend, runtime/package manager, API, database, ORM, auth and workspace/build tooling. Give the version from the lockfile if established; mark a manifest range as declared. Do not write invented versions or "latest" as the installed version.
- **Architecture decisions** — the interview result, statuses, justifications and open questions. Record deferred decisions without presenting recommendations as approved.
- **Structure and boundaries** — the real app/package directories, their responsibilities and links to configs. Include architecture decisions from the conversation only when they concern this project; distinguish the target architecture from the created skeleton.
- **Running and local configuration** — existing scripts, the directory to run them in, required services and variable names from safe templates. Include the Compose file, the PostgreSQL service, image version, host port, volume, env file locations and the database start/stop commands. No secret values, tokens or connection strings with credentials.
- **Verification** — commands actually run and their results. Distinguish a passed typecheck from untested database or auth behavior.
- **Remaining steps and limitations** — e.g. unavailable Docker, unapplied schema, deferred decisions, checks not run and agreed integrations the initializer does not install. Do not claim them as working.

Do not impose the Raven harness architecture on every application. GitHub as a queue, agent policies or no sign-in appear only if they follow from this project's findings. Writing the document does not extend the initialization scope with those integrations. Do not create a roadmap or tasks in this file.

### Update and check

Write a new document in the user's language; for an existing one keep its language and useful structure. Update initialization facts; do not rewrite the document from scratch. Keep manual decisions and unknown sections. Before writing, check whether the file changed since reading; if so, re-read it and include the changes.

Write atomically through a temporary file in the same directory. After writing, check consistency with the generated project and correctness of relative links. A re-run does not create another document or append duplicate sections; it is also not consent to regenerate an existing application.

If initialization left a partial skeleton, record the confirmed facts with the "partial" state and the concrete error, keeping earlier decisions. If the generator did not start at all, you may record the agreed architecture with the "planned" state, but do not suggest that initialization ran. If writing the document fails after a successful bootstrap, report a partial completion of the skill: the skeleton exists, the document needs completing; do not run the generator again for that reason.
