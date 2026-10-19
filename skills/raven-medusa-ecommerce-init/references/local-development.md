# Local development contract

Read when creating configuration, envs and the bootstrap. Check variable names and APIs in the generated starter version; the examples below do not replace its code.

## Compose and isolation

Copy the Compose asset as `compose.yaml` if the project has no configuration yet; merge an existing one. Pick a stable `COMPOSE_PROJECT_NAME`, e.g. the project slug and a short hash of its real path. Write it to env and keep it on later runs. Do not use global `container_name`, external shared networks or volume names shared between shops.

The template uses PostgreSQL 17 and Redis 7 as a starting point. Confirm compatibility with the chosen Medusa and pin a specific image/tag or digest. Do not change the PostgreSQL major version with an existing volume. PostgreSQL 18+ needs a separate check of the directory layout and mounts.

Bind the database and Redis ports to loopback. Apps on the host use `127.0.0.1` and the published port, not Compose service DNS names. Run `docker compose config --quiet`; do not print the expanded configuration with passwords. Do not enable public tunnels or router ports.

Use full app containers when the user wants it. Then rely on the [official Docker configuration](https://docs.medusajs.com/learn/installation/docker), accounting for the pnpm workspace, separate container dependencies and hot reload. Distinguish the backend's internal URL from the URL reachable in the browser. `http://medusa:9000` does not work as the public URL of a client running in the host's browser.

## Envs and credentials

| Default file | Contents |
|---|---|
| `.env` | Compose project, images, ports and local database credentials |
| `apps/backend/.env` | Backend connections, CORS, JWT/cookie secrets |
| `apps/storefront/.env.local` | Public backend address, publishable key, region and storefront address |
| `.local/dev-credentials.json` | Local admin login and generated password |
| `.env.example` / `.env.template` templates | The same variable names, without real secrets |

Keep the starter's template convention. Real envs and the credentials file must be ignored in Git; `git check-ignore` does not replace checking that a secret is not already tracked. Do not rewrite Git history. Restrict permissions of secret files, e.g. to `0600` on POSIX. Do not display their contents in logs or the report.

Generate secrets with a cryptographic RNG: at least 32 bytes for JWT and cookie, random database and admin passwords. Keep existing values. Changing `POSTGRES_PASSWORD` with an existing volume does not change the role's password in the database; do not fix that by deleting data. Do not store the admin password in package.json or in arguments written in documentation. If the CLI needs the password in argv, do not log the command with the expanded value.

Write connection values literally in the consumer's env. Do not assume dotenv, Next and Compose expand references to other variables identically. Encode the password correctly in the PostgreSQL URL or generate a URL-safe password. Before database operations check the process's effective configuration, including shell variables that take precedence over the file.

Typical backend variables:

- `DATABASE_URL`, `REDIS_URL`, `JWT_SECRET`, `COOKIE_SECRET`.
- `STORE_CORS`: the storefront's real origin.
- `ADMIN_CORS`: the origin of Admin and the dev server, if needed.
- `AUTH_CORS`: the storefront and Admin origins their sign-in needs.

Do not copy documentation domains or wildcards into CORS without need. `localhost` and `127.0.0.1` are different origins; choose consistent URLs. A port change must also reach the app start command, CORS, redirects and file serving.

Typical storefront variables:

- `NEXT_PUBLIC_MEDUSA_BACKEND_URL`, `NEXT_PUBLIC_MEDUSA_PUBLISHABLE_KEY`.
- `NEXT_PUBLIC_DEFAULT_REGION`: the code of a country served by a real region in the database.
- `NEXT_PUBLIC_BASE_URL`: the local address with `http`, if TLS is not configured.

Check the SDK code and server actions: another version may use `MEDUSA_BACKEND_URL` or other names. Do not add envs nobody reads. The publishable key is public; the admin key and backend secrets never go into `NEXT_PUBLIC_*`. Leave Stripe, Cloud and S3 optional, without fake keys suggesting a working integration.

## Medusa, Redis and files

Merge configuration into `medusa-config.ts`. If the local database needs SSL disabled, limit that to the local configuration; do not disable SSL universally for deployments.

`REDIS_URL` alone does not configure modules. Check the [Medusa configuration](https://docs.medusajs.com/learn/configurations/medusa-config) and the [official Redis providers](https://docs.medusajs.com/learn/deployment/general). By default connect `projectConfig.redisUrl` to sessions and the native `@medusajs/medusa/event-bus-redis` to the event bus, with a version matching the backend. Test startup and operation; do not add a duplicate of a module already in the starter.

Leave other modules as in the starter. If its features need a shared workflow engine or locking, use the current native Redis providers. Do not copy historical option names from other versions. Do not add optional feature flags and a cache module just because Redis already runs. In the setup documentation state which features use Redis and which stay local/in-memory.

Use the [local file provider](https://docs.medusajs.com/resources/architectural-modules/file/local). Check the real upload directory and the public `backend_url` of the chosen version, image availability from the host and the Next Images configuration. Upload through Medusa; dropping a file into the directory does not verify the provider. Ignore uploads in Git, keep them across restarts. Do not add MinIO or Mailpit without a real need; sending emails is not part of the local checkout if the starter does not require it.

## Migrations and bootstrap

Check the official seed and CLI of the chosen version. For example migrations may run through `pnpm --dir apps/backend exec medusa db:migrate`, and the seed through a `medusa exec` script; use the starter's actual scripts and the right cwd. Stop the operation when it points to a database outside this project's local Compose, unless the user explicitly named and authorized another development environment.

Ensure consistent links store → sales channel → publishable key and region → country/currency/prices, stock location and availability, fulfillment and a delivery option. Use the official workflows and SDK of the chosen version, not direct inserts into internal tables.

On a retry check each group of required entities and fill in the missing ones. Use stable identifiers/handles or your own marking of demo data; "some product exists" is not enough. Control the result of a partially finished seed. The publishable key must serve the channel of the products the storefront displays. If the key cannot be read again, keep the previously safely stored value; do not create a new one on every start.

Create the admin only when it is missing. If the account exists but the password is not available, do not reset it automatically: report the concrete access problem. Errors other than an unambiguous "entity exists" must abort the bootstrap.

Use the country/currency agreed in the project; for a Polish shop PL/PLN. Without findings you may keep the starter's demo region. Do not set just `NEXT_PUBLIC_DEFAULT_REGION=pl` without a region and prices in the database.

To check checkout use the available native manual/system payment provider and a local delivery option. Verify the storefront can handle them. If needed add minimal handling of the existing provider only for development; do not build your own payment system. Do not automatically enable test payments that need an external account. Describe an agreed absence of real payment or email sending as the environment's scope, not as a working integration.

## Commands and acceptance

`setup` is responsible for preparing and completing the environment; `dev` only for starting it and HMR. Run the `setup` script as `pnpm run setup` — plain `pnpm setup` is a built-in pnpm command. Use the starter's orchestrator. Every script must propagate errors, use the right env and clean up only its own processes. Avoid a global `pkill` and appending `|| true` to migrations or seeding.

Verification includes a real second setup and a restart without deleting volumes. Do not replace that with a syntax check. Record the commands run, the CLI/Medusa/Next/Node/pnpm/image versions and results without secrets. Do not announce a ready environment if Docker, sign-in or checkout are still blocked.
