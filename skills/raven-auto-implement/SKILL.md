---
name: raven-auto-implement
description: "Carry out the user's instruction, optionally with a given GitHub issue, plan or external ticket link (Jira, Linear and similar) read as the specification, work in parallel where the change splits, verify the change once at the end at a `quick`, `standard` or `thorough` level matched to risk, and summarize the result only in the final chat message."
argument-hint: "[#issue | ticket URL | instruction] [--recording]"
---

# Raven Auto Implement

Carry out the user's instruction and prove the change works to a degree matching its risk. A given issue, ticket or plan is context; the instruction refines or changes their scope without re-planning or review. A small change needs neither an issue nor a plan. Read only the code and context the change needs; do not replay the Raven cycle. Follow [working on GitHub tasks](../raven-workflow/references/git-workflow.md). Talk to the user in their language.

## Rules

- **Input.** The specification is the instruction, supplemented by the given issue, ticket or plan; ask only when the goal is ambiguous. When the plan diverges from the real code, deviate minimally and describe in the final message what you changed and why.
- **External ticket.** A link or key from Jira, Linear or a similar tracker is the specification; read it and work from it per the [external ticket](../raven-workflow/references/git-workflow.md#external-ticket) rules (read-only, no GitHub issue). A plan at `context/changes/<KEY>/plan.md` is the plan for that ticket.
- **Decisions.** Make routine technical decisions yourself. Ask only about a missing product decision that genuinely blocks the work, and continue the independent part meanwhile.
- **Executor.** You lead the work and own the result: contracts, integration, the final checks and the commits. You may spawn implementers per [parallel implementers](references/parallel.md), but no separate planner, tester or QA; the only reviewer is the independent review at `thorough`. Do not add stages, acceptance gates, process reports, checkpoints or metrics; on GitHub you only take up the issue as described below.
- **Branch and issue.** Before the first commit: with a given issue and no existing branch, assign yourself, set `in-progress` and create a branch from the current base per [working on GitHub tasks](../raven-workflow/references/git-workflow.md); when resuming, use the existing branch. With an external ticket, find or create its branch per the [external ticket](../raven-workflow/references/git-workflow.md#external-ticket) rules. Without an issue or ticket work on the current branch, and if it is the default branch, create a short branch following the project's convention. Never commit to the default branch.
- **Repo.** Before changing anything, note the base SHA. Preserve other people's work in the working tree. Respect project instructions (including `context/foundation/lessons.md` if present), security and real tool and permission limits. Project instructions (AGENTS.md, CLAUDE.md) take precedence over minimal verification: if they require checks before a commit, they run as part of the final checks. Commit only after the final checks pass, in logical steps following the project's convention (stage them by file or hunk); no push and no PR.
- **Tests.** Tests come at the end, after you have seen the feature work (see [Order of work](#order-of-work)). Use existing tests first; for a gap, add or adapt a test of the full changed flow at the cheapest layer that covers it, and a unit test only for logic the flow test cannot reach.
- **Resuming.** Commits come only at the end, so an interrupted run leaves its work uncommitted on the task's branch. On resuming, take the base from `git merge-base <default branch> HEAD`, treat uncommitted changes that clearly belong to the task as the earlier run's work (ask when unclear) and continue from "See it work".
- **Pre-existing failures.** Do not fix unrelated pre-existing failures of tests, fixtures, locators or infrastructure. Report the limitation and, if possible, check the changed behavior through another adequate channel.
- **A check that was not run or was blocked is never reported as passed.**

## Order of work

1. **Start.** Pick the level. Start the long-running tools in the background: the dev server (at `standard` and `thorough`) and the typecheck in watch mode, when the project has one. Read their output instead of rerunning the commands. Send independent reads and commands as parallel tool calls.
2. **Contract first.** When the change crosses layers or will be split, write the shared types and interface signatures (API procedures, endpoints, props) with stubs, and check that they compile. From here the parts that depend only on the contract can proceed independently.
3. **Implementation.** Work alone or spawn implementers per [parallel implementers](references/parallel.md). While building, rely on the background typecheck and quick local runs; do not run test suites yet.
4. **See it work.** After integration, check the whole changed behavior once per the level (below).
5. **Final checks.** Add the missing flow tests, then run the level's checks and the checks the project instructions require once. When something fails, fix it and rerun only the failing tests or checks until they pass, then run the full set once more. Run independent checks in parallel.
6. **Recording.** Only when the user asked for it with `--recording` (or in words): record the finished feature per the [recording guidance](references/browser-review.md#recording), after the last fixes (at `thorough`, after the review round). Without that request, make no recording.
7. **Commits.** Commit after the final checks pass (at `thorough`, after the review round). Stop the background processes you started, unless the user's acceptance needs the dev server; the final message says what is left running.

## Choosing the level

Before changing anything, pick the level and state it in one sentence with the reason. The user overrides it with the word `quick`, `standard` or `thorough` in the instruction or during the work. You may only raise the level during the work, noting it in the final message — never lower it.

- `quick` — the change does not alter behavior: copy, styles, rename, config, small refactor. When in doubt, pick `standard`.
- `standard` — the default: an ordinary feature or fix without a risk signal.
- `thorough` — a mistake in the change would be costly, hard to reverse or hard to notice before a user does. Judge this yourself from the project and the change; when unsure between `standard` and `thorough`, pick `thorough`.

At `thorough`, read and follow [references/thorough.md](references/thorough.md) instead of the `quick` and `standard` steps; the "Checking it works", "Time budget" and "Final message" sections still apply.

## `quick`

Must prove: the change compiles and does not break existing tests.

1. Implementation.
2. Render only for a visual change.
3. At the end: typecheck of the affected workspace or package and existing tests of the changed files or modules.

Approximate verification overhead: ~1–3 min.

## `standard`

Must prove: the changed feature works in the running application.

1. Implementation.
2. Checking it works (below) — the happy path of the changed behavior, once, after integration.
3. At the end: the missing flow test, then typecheck, lint and the tests of the affected area (or the suite the project instructions require).

Approximate verification overhead: ~5–10 min (+~2 min for a cold app start).

### Checking it works

Tests do not replace checking that the feature works. Use the application started at the beginning (or one already running) and go through the changed feature the way a user or API client would:

- UI → isolated Playwright session and an observable effect on screen, per the [UI guidance](references/browser-review.md);
- API/backend → call the local endpoint and check the response;
- logic without an interface → a test or a short script calling the changed code.

Confirm data writes by reading back (reload, repeated GET, admin view). Check error scenarios only when the change concerns error handling or you found a problem. When the app cannot be started, record it in the final message as a limitation, not a pass; if possible, check the behavior through another channel and state clearly what it actually confirms.

## Time budget

Overheads are approximate, not limits. When verification clearly exceeds the level's overhead (e.g. more than twice), do not extend it further without a concrete detected problem, and in the final message say what took the time.

## Final message

Give the result in the final chat message; do not write it to Markdown, the plan or the issue, and do not create acceptance.md. A summary of the verification reaches the PR only through `raven-pr`. Do not start the next stage. The final message contains:

- the level (and any raise, with the reason);
- the source ticket (key and link), when there was one;
- what changed, including deviations from the plan (what, why);
- how the work was split: alone, or which implementer did which part;
- what was checked — at `standard` also what exactly was observed and through which channel;
- the recording paths (video, trace) with what each part shows, when one was requested;
- limitations: checks not run or blocked, and what remains to be checked;
- step-by-step acceptance instructions: concrete actions or commands and the expected effect, with detail matched to the change.

When blocked, also give the summary and instructions, clearly naming what is missing.
