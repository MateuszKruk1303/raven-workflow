---
name: raven-prepare-env
description: "Prepare a checkout for a task before raven-plan or raven-auto-implement when other worktrees or checkouts may run at the same time: pick the checkout (new worktree from the default branch, stash and work here, or the user's choice), give it its own ports, Compose project and database after the user accepts the proposal, and keep a machine-local environment recipe so later runs do not rediscover the setup. Also cleans up a finished worktree."
argument-hint: "[#issue | ticket URL | branch] | cleanup <branch | path>"
disable-model-invocation: true
---

# Raven Prepare Env

Prepare one isolated checkout for one task, so that it can run next to other checkouts of the same repo without port, container or database collisions. You only prepare: you do not plan, implement or run the task's skills. Follow [working on GitHub tasks](../raven-workflow/references/git-workflow.md). Talk to the user in their language.

The user decides which checkout to use and accepts the environment before you apply it. You write only ignored or excluded files; a collision that only a change to a tracked file would remove is reported with the proposed change, and the user handles it.

## Recipe

The recipe is `<common dir>/raven/environment.md`, where `<common dir>` is `git rev-parse --path-format=absolute --git-common-dir`. It is shared by all worktrees of the repo on this machine and is not versioned. Write it in English; it holds no secret values. It contains:

- services: what runs (app processes, Compose services), the start command and working directory of each, the default port and the variable that sets it;
- env files: which files the app and Compose read, where they come from (copied from the main checkout, or created from a template) and which variables hold ports, URLs and the Compose project name;
- isolation: how the Compose project name and host ports are set per checkout, and any local override file;
- setup: install, migrations and seed commands for a new empty database, in order;
- check: how to see that the app is up (URL or command) and how to check the database connection;
- cleanup: commands to run before removing a checkout;
- pitfalls: what did not isolate and why (e.g. a host port hardcoded in `compose.yaml`, a fixed volume `name:`, a main-checkout tool config that scans `.claude/worktrees/`, auth cookies shared across ports on `localhost`).

When the recipe exists, read it first and use it instead of rediscovering. Check it against the repo (scripts, Compose services and env variables it names still exist); when it no longer matches, fix the affected part and show the change in the proposal. When it does not exist, discover the setup from the project's package manifests, Compose files, env templates, `context/foundation/tech-stack.md` and project instructions, and write the recipe after the environment works. Writing the recipe needs no separate consent.

## Prepare

1. **Task and branch.** Resolve the argument: an issue, an external ticket (only its key and title are needed here; read-only, per [external ticket](../raven-workflow/references/git-workflow.md#external-ticket)), a branch, or nothing — then ask for a short name. Run `git fetch --prune`, read `git status --porcelain` and `git worktree list`, and find the task's existing branch per the shared rules (local, remote, by the exact key; a branch whose PR was merged is not existing work). A worktree that already has the task's branch checked out is reused: continue at step 2 there. A new branch is named by the project's convention and the shared rules.
2. **Checkout.** The current checkout passes without a question when it is clean on the default branch, or on the task's own branch (its uncommitted changes are the task's earlier work). Otherwise ask, with `AskUserQuestion`, naming the branch and the changed files:
   - **New worktree** (recommended) at `.claude/worktrees/<branch slug>`; pick another slug when that path exists. A new branch: `git worktree add --no-track -b <branch> <path> origin/<default>`. An existing local branch: `git worktree add <path> <branch>`. A remote-only branch: `git worktree add --track -b <branch> <path> origin/<branch>`. Make sure `.claude/worktrees/` is in `<common dir>/info/exclude`. The current checkout stays untouched.
   - **Stash and work here**: the user's choice is the consent the shared rules require for a stash. `git stash push -u -m "raven-prepare-env <date> <current branch>"`, then `git switch -c <branch> --no-track origin/<default>` (or switch to the existing task branch). Tell the user how to restore: find the entry by its message in `git stash list` and `git stash pop` it on the original branch. Never reset or delete the changes.
   - Anything else the user writes.
3. **Env files.** In a worktree that lacks them, copy the env files the recipe names from the main checkout without displaying their values. A copied or created env file that is not ignored goes into `<common dir>/info/exclude`, so it never reaches a commit.
4. **Collisions.** Find what is taken: listening ports (`lsof -nP -iTCP -sTCP:LISTEN`, or `ss -ltn` where `lsof` is missing) plus a bind test of each port you pick; running Compose projects (`docker compose ls`); and the port and project variables (read by name, not whole files) in the env files of the other worktrees — those count as taken even when not running. Read the resolved Compose model through a filter that prints no values (e.g. `docker compose config --format json | jq '{s: .services | map_values({container_name, ports, volumes}), volumes, networks}'`) for fixed `container_name`, volume `name:` or `external`, and fixed network names: they defeat project isolation.
5. **Proposal.** Show in one message, and ask for acceptance with `AskUserQuestion`: the checkout path and branch; per service the port (the default when free, otherwise a free one kept stable for this checkout); the Compose project name `<repo>-<branch slug>`, distinct from every other checkout's project and directory name, which gives its own containers and volumes and therefore its own database; the env changes by variable name (`DATABASE_URL` shown without credentials); the setup commands; the recipe changes. A host port, container name or volume name fixed in a tracked Compose file is overridden in an untracked local override file added to `info/exclude`: the standard override name matching the base file (`compose.override.yaml` or `docker-compose.override.yml`) when the repo has none, otherwise a separately named file, loaded by `COMPOSE_FILE=<base file>:<local file>` in the excluded `.env` of the Compose project directory; ports need `ports: !override` (Compose 2.24.4+). When that is not possible, report the collision with the tracked change that would fix it (e.g. `${DB_PORT:-5432}:5432`) and do not make it. The user may change any value; apply only the accepted version.
6. **Apply.** Write the env changes, only to ignored or excluded files. Note which volumes carry the label `com.docker.compose.project=<project>`, then install dependencies in the checkout and start its Compose services, waiting for their healthchecks with a bounded time. The database is new and empty only when no volume of the project existed before this `up`, no bind-mounted data directory of its services holds files, and the database has no tables in the app's schema; only then run the recipe's migrations and seed through the project's scripts. Never run migrations, resets or `down -v` on an existing volume, and never touch other checkouts' containers or files.
7. **Check.** Start the app on its new ports, confirm the recipe's check (the URL responds, the database answers through the app's configuration, e.g. `SELECT 1`) and stop the app again; leave the Compose services running. Then write or update the recipe and, with a GitHub issue, take it up (assignee, `in-progress`) as the shared rules describe.

Re-running on a prepared checkout reuses its ports, project and data and only repeats what is missing.

## Cleanup

`/raven-prepare-env cleanup <branch | path>` removes one finished worktree and its environment; never the main checkout. Run `git fetch --prune`, then check before touching anything:

- `git status --porcelain` in the worktree is empty; otherwise show it and refuse.
- The branch is done: its tip is on its remote branch, an ancestor of `origin/<default>`, or the tip of a merged PR (`gh pr view <branch> --json state,headRefOid`, state `MERGED` and `headRefOid` equal to the local tip — the case after a squash merge). Otherwise show the unpublished commits and refuse.
- The project's volumes (label `com.docker.compose.project=<project>`) belong to no other checkout: the project name differs from every other checkout's project and directory name.

Show what will go — the worktree path, the project's containers and volumes, the local branch — and after the user accepts: the recipe's cleanup commands, `git worktree remove <path>`, `docker compose -p <project> down -v`, then delete the branch with `git branch -d`, or `git branch -D` only when the merged-PR check above proved it. No `--force` on the worktree; on a failure stop and report what is left.

## Limits

- Without Docker or a running daemon, prepare the files, mark the start and checks as not run and give the command to finish.
- Without GitHub access, skip the take-up of the issue and the merged-PR check, and report it.
- An interrupted run leaves what it made; the next run detects the worktree, env files and Compose project and continues.
- A check that was not run or failed is never reported as passed.

## Final message

In chat: the checkout path and branch; the ports and URLs; the Compose project; what was installed, migrated or seeded; the stash ref and message, if one was made; checks run with results and anything not run; collisions left to the user with the proposed fix; on the "work here" path, that the isolation stays in this checkout's env files until the user reverts it. Then the next step: in a new terminal `cd <path> && claude`, then `/raven-plan` or `/raven-auto-implement` with the task. A worktree inside the repo also sees the main checkout's `CLAUDE.md` above it; name it when the two differ.
