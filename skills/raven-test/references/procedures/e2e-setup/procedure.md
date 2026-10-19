# Internal Raven procedure

This is part of the raven-test skill, not a separate command. Read it together with the parent raven-test SKILL.md, which defines scope and permissions. All templates, references and scripts ship locally in this directory. Do not search for or install other workflow packages.

**Execution rules that apply:** [working on GitHub tasks](../../../../raven-workflow/references/git-workflow.md).

# Raven E2E setup — Playwright infrastructure for the E2E procedure

You take the project from "no Playwright" (or "some Playwright") to exactly what the [E2E procedure](../e2e/procedure.md) needs, and nothing more:

```
DETECT → INSTALL → CONFIGURE → SEED → AGENT WIRING → RECORD → HAND OFF
```

Every step first checks whether its result already exists and fills in only what is missing. **A second run on a finished project changes no files** — no rewritten config, no global `playwright-cli` install, no new `updated` date. That is the test of this procedure.

Optional input from raven-test: a risk identifier or a one-line risk description for the seed (skips the risk question in step 4).

## What this procedure covers — and what it won't do

Covers: the Playwright config, `tests/e2e/auth.setup.ts`, the seed test, `playwright-cli` wiring and the `## E2E` section in `context/foundation/test-stack.md`.

In the config, "covers" means **the app `webServer` entry** (the one whose `url` is the base URL) and every field `test-stack.md` records. The E2E procedure may later add extra `webServer` entries for mock servers (array form) and hook its mock into the app entry (`references/playwright-setup-templates.md` → "Who owns what in the config"). A re-run reads and records only the app entry's build + preview command, url, port and `reuseExistingServer`, and never touches extra entries.

It will not:
- write E2E tests other than the seed — that is the E2E procedure's job;
- touch CI workflows;
- overwrite an existing config key or spec without asking;
- write to the agent rules files (AGENTS.md, CLAUDE.md, …). E2E rules matter only while working on E2E tests, so they live in `../e2e/references/e2e-quality-rules.md` and the E2E procedure loads them, not every session. An E2E rules block added by an earlier version of this procedure stays as is; you may remove it;
- read or display secret values, create users outside the local stack or commit credentials;
- approve acceptance or publish on its own — raven-test handles commits, and PR and review are separate requests.

## Conventions

> **Asking the user.** Wherever this procedure says *ask the user*, use the `AskUserQuestion` tool with described options. Ask only about what could not be detected.

> **Browser tool.** Read `references/tool-wiring.md`: apply the mode choice from raven-browser (CLI by default, MCP on the user's explicit instruction or consent). Do not require an extra skill, a global CLI or an installer manifest.

Keep a short checklist in the conversation, one line per step (`- [ ] 1. Detect` … `- [ ] 7. Hand off`), and mark every step `done`, `already in place` or `changed`. The final report is built from it.

---

## 1. Detect

Read, do not write. Gather these facts and show them to the user as one short table before step 2.

1. **Agent tool.** Read `references/tool-wiring.md`. Use the tools available in the current session and the project's existing configuration; do not require an installer manifest or additional skills.
2. **Package manager** from the lockfile: `package-lock.json` → npm, `pnpm-lock.yaml` → pnpm, `yarn.lock` → yarn, `bun.lock`/`bun.lockb` → bun. Use it for every install and run command.
3. **Stack and commands.** From `package.json` scripts and the framework config: the build command and a production-like preview/start command. Prefer build + preview over the dev server.
4. **Port — read it, never assume.** In order:
   - an explicit port in the framework config (e.g. `server.port` in `astro.config.*`, `preview.port`/`server.port` in `vite.config.*`);
   - a `--port`/`-p` flag in the preview/start script;
   - the framework's documented default for its preview/start command (e.g. Astro 4321, Vite preview 4173, Next.js 3000).
   Record where the number came from. If `E2E_PORT` is already set in the env file (the name and port number are not secrets, so read them), that is the port the run uses: the user answered the port question on an earlier run, so do not ask again.
5. **Is the port free?** Check the port the run uses (`E2E_PORT` if set, otherwise the detected one) before relying on it: `lsof -nP -iTCP:<port> -sTCP:LISTEN` (macOS/Linux) or `netstat -ano | findstr :<port>` (Windows); `nc -z localhost <port>` also works. If something is listening, say so clearly and name the process if you can: with `reuseExistingServer` outside CI, Playwright **would silently test whatever app is already running at that address**. Offer two ways out — stop that process or set `E2E_PORT=<free port>` in the env file (the config reads it). Never pick a new default port yourself.
6. **Existing Playwright.** `@playwright/test` in `package.json`; `playwright.config.*` (read it in full: `testDir`, `use.baseURL`, `webServer`, projects, `storageState`, `trace`, `screenshot`); existing specs (`*.spec.ts`, `*.setup.ts`); an existing seed (a file named `seed.spec.ts` or the `seed` field in `test-stack.md`).
7. **Unit runner overlap.** If a unit runner is configured (e.g. Vitest, Jest), check its include globs. If they would also pick up `tests/e2e/**/*.spec.ts`, the E2E specs must be excluded there — note it for step 3.
8. **Auth approach.** Look at middleware / route guards, the sign-in page and its form, and the auth provider (e.g. Supabase, Auth.js, Clerk, custom session). Record: protected routes, sign-in path, landing page after sign-in, and whether the provider runs locally (e.g. `supabase/config.toml` → local stack via `npx supabase start`). No sign-in at all → `auth: none`.
9. **App env.** Which gitignored env file the app reads (e.g. `.env`), whether preview reads a different one (see `references/playwright-setup-templates.md` → Preview env), and whether the backend URL there points at a local stack. Read only variable **names**, never values — except to check that the backend URL is local.
10. **State.** `context/foundation/test-stack.md` (existing `## E2E` section).

If the project has no web app to drive (no server/preview command at all), stop and say E2E needs a runnable app.

## 2. Install

Only what is missing:

- `@playwright/test` not in `package.json` → add it as a dev dependency with the detected package manager (`npm i -D @playwright/test`, `pnpm add -D @playwright/test`, `yarn add -D @playwright/test`, `bun add -d @playwright/test`).
- Browser: `npx playwright install chromium` (use the package manager's exec equivalent). It does nothing when the browser is present and changes no project files.

Record the installed version (`npx playwright --version`).

## 3. Configure

Use `references/playwright-setup-templates.md`.

- **`.gitignore` first** (before the first `playwright-cli` call): append the missing Playwright lines from the template (at least `playwright/.auth/` and `.playwright-cli/`, which the first `playwright-cli` call creates, with snapshots and console logs that may contain credentials), and confirm the env file holding credentials is ignored.
- **Start the app for exploration.** Steps 3 and 4 explore the sign-in page and the seed flow with the available browser tool, so the app must run: run the build command, then the preview command on the port from steps 1.4–1.5 **in the background** (the same commands the `webServer` entry runs; check the stack notes in the template first). Stop it, and any daemon it left behind, **before every `playwright test` run**, so `webServer` starts the server and owns it. A server left running is silently reused and hides a stale build. When using an existing `playwright-cli`, pass a named session on every call (`-s=<repo-name>`); the default session is shared by every project on the machine (per `references/tool-wiring.md`). `playwright-cli fill` prints the typed value in its output and logs: when typing the test user's password, do not show that line to the user.
- **No config** → create `playwright.config.ts` from the template, filled with detected values: a `PORT` constant defaulting to the detected port and reading `E2E_PORT` first; `webServer` runs build + preview **on that port** (the port is passed explicitly to the preview command), `url: baseURL`, `reuseExistingServer: !process.env.CI`; `use.baseURL`; a `setup` project matching `*.setup.ts`, whose session file is `playwright/.auth/user.json`, loaded via `use.storageState` by the browser project that depends on it; `trace: 'on-first-retry'` and `screenshot: 'only-on-failure'`; env loaded explicitly from the gitignored env file.
- **Config exists** → add only the missing pieces (template → "Extending an existing config"). If a key exists with a different value, establish the cause and impact, and ask the user before changing it, showing the old and new value. Keys that already match stay byte-identical. When `webServer` is an array, compare only the app entry; the other entries are the E2E procedure's mock servers, so leave them alone.
- **Auth setup** (skip when `auth: none`): if no `*.setup.ts` exists, open the sign-in page with the available browser tool, take a snapshot and write `tests/e2e/auth.setup.ts` from the template using the accessible names you saw. It signs in through the real UI with `E2E_USERNAME` / `E2E_PASSWORD` from the env file and saves `playwright/.auth/user.json`.
- **Test user**: if `E2E_USERNAME` / `E2E_PASSWORD` are not set, follow the template's "Test user (local only)" section — confirm the backend is local, create the user there (or ask the user to), and put the two variables in the gitignored env file.
- **`.env.example`**: whether or not the test user already existed, add the two names (without values) if that file exists and lacks them.
- **Unit runner overlap** from step 1.7: within the requested scope, add the right E2E directory to the exclude list if it stops the wrong runner from picking up the tests; keep existing exclusions.

## 4. Seed

The seed is the pattern every generated test copies (`../e2e/references/seed-test-pattern.md`), so it must be small, correct and green.

- **Seed exists** (the `seed` path from `test-stack.md` or `seed.spec.ts`) → do not rewrite it; just run it (below).
- **No seed → pick one risk.** If raven-test passed a risk, use it. Otherwise take the browser-level risks from the issue or plan AC and pick the one **fastest to get green without mocks**, e.g. an auth-gate redirect rather than a flow calling an external API. Ask only about a genuinely missing expectation. A risk without an id (described by the user) gets a short kebab-case slug, e.g. `auth-gate-roundtrip`.
- **Is the outcome implemented?** Explore the flow before committing to the risk. If the observable outcome does not match what the app currently does (e.g. the user expects a return to the protected page, but sign-in always goes to `/`), tell the user. Then create the seed for the implemented part and record the rest as unimplemented, or pick another risk. Never assert behavior the app does not have.
- **Write** `tests/e2e/seed.spec.ts` (or the project's existing E2E directory) following the four patterns from `../e2e/references/seed-test-pattern.md`: role-based locators, self-contained setup → action → assertion → cleanup, waiting for state, and a test name naming the risk. Explore the flow first with the tool chosen per `references/tool-wiring.md` and use the accessible names from the snapshot. Wait until the form is interactive before typing (see the seed pattern: input typed into a form that has not finished hydrating is lost). Add a provenance comment with the risk identifier. A seed whose risk is the signed-out path opts out of the saved session (see the seed pattern).
- **Run it green from a cold server** with the single-spec command (the `setup` project runs first as a dependency). First stop the exploration server and confirm nothing listens on the port (the step 1.5 command prints nothing), so `webServer` builds and starts the app itself. A warm server hides hydration races and stale builds, so a seed that went green only against one is not confirmed. If the backend is a local stack, make sure it runs. On red: read the error and the trace, fix the seed or setup — never weaken the assertion until it cannot fail, and never skip the test. Then ask the control question: would this assertion fail if the risk materialized? If not, strengthen it. (A deliberate break, when effectiveness is uncertain, belongs to the E2E procedure.)

## 5. Agent wiring

Read `references/tool-wiring.md` and check access to the chosen tool against the test app. By default use the existing CLI or an npx invocation, in its own named session. Pick MCP only on the user's explicit instruction or consent, never as a fallback for a missing CLI. Do not install a global CLI or additional skills automatically. Report a missing chosen tool as a concrete exploration blocker.

## 6. Record

Write the `## E2E` section in `context/foundation/test-stack.md` exactly per `references/test-stack-e2e-schema.md` — every required field, filled with facts from steps 1–5 (for `web server command`, only the app entry's build + preview command). Keep the rest of the file. If all fields except `updated` already match, leave the file unchanged. Create `context/foundation/` if it does not exist.

## 7. Hand off

Give in chat:

```
E2E setup — done

[checklist: each step with done / already in place / changed]

Created or changed:
- [files, one per line — or "nothing: the project was already set up"]

Review before you commit:
- tests/e2e/seed.spec.ts — the pattern every generated test will copy
- playwright.config.ts (port [port] from [source]; override with E2E_PORT)

Never commit: playwright/.auth/, the env file with E2E_USERNAME / E2E_PASSWORD.

Next risk for the E2E procedure: [browser-level risk from issue/plan AC without a spec, or "none"]
```

Then return to raven-test: for named E2E gaps continue with the [E2E procedure](../e2e/procedure.md) only after the setup is confirmed working, without invoking the skill again.

## References

- `references/tool-wiring.md` — choice of available tool, session isolation and data protection.
- `references/playwright-setup-templates.md` — templates for config, auth setup, test user and `.gitignore`.
- `references/test-stack-e2e-schema.md` — contract of the `## E2E` section read by the E2E procedure and raven-hooks.
- `../e2e/references/seed-test-pattern.md` — the four patterns the seed carries, with an example (shared with the E2E procedure).
- `../e2e/references/e2e-quality-rules.md` — E2E rules the seed follows and the E2E procedure enforces, with the reasoning.
