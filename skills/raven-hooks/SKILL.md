---
name: raven-hooks
description: "Configure GitHub Actions that run lint, typecheck and the right tests when a PR is opened or updated, matching the project's stack and strategy. Does not configure agent session hooks."
---

# Raven Hooks

Seed or complete GitHub Actions checks for the project's actual stack. The name means CI after a PR here, not local agent hooks. Do not implement product tests or publish a PR during setup. Talk to the user in their language.

Follow [working on GitHub tasks](../raven-workflow/references/git-workflow.md). Read the repo instructions, manifests/lockfile, workspace config, existing workflows, test-stack and run scripts. Do not assume Node/Playwright or a single package.

## Design the checks

Detect the runtime and versions, the package manager, the lint/format-check/typecheck, unit, integration, E2E and build commands, if needed. Pick checks consistent with existing tools and strategy; report a missing runner/tests as a gap for raven-test, do not create a green placeholder. Not every layer has to fit the project.

Use one or several workflows with separate readable jobs by time and dependency, without artificially multiplying files. Merge existing configuration and keep other people's jobs. pull_request triggers must cover opening, new commits and reopening a PR; include ready_for_review if you filter drafts. Do not add deploy or automatic merge.

Set the draft CI policy deliberately. Usually run cheap checks, e.g. lint/typecheck and fast tests, also for drafts, so an early PR gives feedback. Costly integration/E2E may wait for ready_for_review if the risks and project policy allow; then also cover later commits of a ready-for-review PR. Do not disable existing required checks just to save. Record which checks run when and why.

Every required check must emit a result for the current SHA at the right moment of the gate. A skipped draft check is not evidence of PASS; before merge it must actually run for the version under review. Draft/path filters and an aggregate job must not turn a skipped, cancelled or unrun required check into a fake green. Check the draft → ready → new commit flow and the conditions of required checks, without treating an old run as the result of a new SHA.

Before writing YAML, verify the current syntax and action versions in the official GitHub documentation and the documentation of the detected tools. Prefer actions pinned to a verified full SHA with a version comment. Use minimal permissions, usually contents: read; do not run untrusted PR code through pull_request_target with secrets.

## Implementation and checking

- Install dependencies reproducibly from the lockfile; use the real workspace directories, correct cache keys and runtime versions.
- Integration/E2E get isolated test services, migrations/seed, healthcheck and cleanup. Replace external paid/non-deterministic services with suitable fixtures/mocks. Do not use production data or connections.
- Add timeouts, concurrency that cancels a stale run of the same PR, and failure diagnostics. Report/trace artifacts must not contain secrets or private data; set a reasonable retention.
- Test failures must fail the job. Do not use continue-on-error, `|| true` or pass-with-no-tests to work around missing required checks. Path filters must not leave required checks permanently pending; do not add them without settling that behavior.
- Validate the YAML and workflow with an available validator, and the real commands locally where possible. If the validator/environment is unavailable, name the check not run; do not claim Actions passed before a real run.

Write the configuration in the repo, and give the result in chat: jobs, triggers and the draft/ready policy, commands, environment, files, validation, required secrets/variables (names only) and fork PR limitations. Surface missing settings without inventing values. Do not change branch protection/rulesets or Done automation without a separate request; adding a workflow alone does not mean the check blocks merge.

Handoff: what will run after a PR, what was checked locally and what the first run will only prove. A repeated invocation updates the configuration without duplicates. Do not change product code for a green CI and do not run raven-pr automatically.

## Enforcing gates

This stage owns recognizing the gap between the existing Actions workflow and the actually required checks. Read, where you have access, the rulesets/branch protection of the target branch; in the report distinguish: a configured job, a confirmed run and a check that blocks merge. No access means UNKNOWN, not no rules.

When the user separately requests enforcing gates, prepare a concrete change of the existing rules with the real check names, keeping other protections. Apply it within the requested scope and read the state back after writing. Do not create a mandatory check that emits no result for the right PRs. CI automation does not change issue status; merge and closing the issue belong to [raven-merge](../raven-merge/SKILL.md). CI setup alone is not consent to change these settings.
