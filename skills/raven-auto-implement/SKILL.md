---
name: raven-auto-implement
description: "Carry out the user's instruction, optionally with a given issue or plan, verify the change at a `quick`, `standard` or `thorough` level matched to risk, and summarize the result only in the final chat message."
argument-hint: "[#issue | instruction]"
---

# Raven Auto Implement

Carry out the user's instruction and prove the change works to a degree matching its risk. A given issue or plan is context; the instruction refines or changes their scope without re-planning or review. A small change needs neither an issue nor a plan. Read only the code and context the change needs; do not replay the Raven cycle. Follow [working on GitHub tasks](../raven-workflow/references/git-workflow.md). Talk to the user in their language.

## Rules

- **Input.** The specification is the instruction, supplemented by the given issue or plan; ask only when the goal is ambiguous. When the plan diverges from the real code, deviate minimally and describe in the final message what you changed and why.
- **Decisions.** Make routine technical decisions yourself. Ask only about a missing product decision that genuinely blocks the work, and continue the independent part meanwhile.
- **Executor.** You work as one current agent: no delegation, separate planner, tester or QA. The only exception is the independent review at `thorough`. Do not add stages, acceptance gates, process reports, checkpoints or metrics; on GitHub you only take up the issue as described below.
- **Branch and issue.** Before the first commit: with a given issue and no existing branch, assign yourself, set `in-progress` and create a branch from the current base per [working on GitHub tasks](../raven-workflow/references/git-workflow.md); when resuming, use the existing branch. Without an issue work on the current branch, and if it is the default branch, create a short branch following the project's convention. Never commit to the default branch.
- **Repo.** Before changing anything, note the base SHA. Preserve other people's work in the working tree. Respect project instructions (including `context/foundation/lessons.md` if present), security and real tool and permission limits. Project instructions (AGENTS.md, CLAUDE.md) take precedence over minimal verification: if they require checks before a commit, run them. Commit logical steps following the project's convention; no push and no PR.
- **Tests.** Use existing tests first; add or adapt a test for a gap in the changed behavior. After every fix, rerun the check that found the problem.
- **Pre-existing failures.** Do not fix unrelated pre-existing failures of tests, fixtures, locators or infrastructure. Report the limitation and, if possible, check the changed behavior through another adequate channel.
- **A check that was not run or was blocked is never reported as passed.**

## Choosing the level

Before changing anything, pick the level and state it in one sentence with the reason. The user overrides it with the word `quick`, `standard` or `thorough` in the instruction or during the work. You may only raise the level during the work, noting it in the final message — never lower it.

- `quick` — the change does not alter behavior: copy, styles, rename, config, small refactor. When in doubt, pick `standard`.
- `standard` — the default: an ordinary feature or fix without a risk signal.
- `thorough` — a mistake in the change would be costly, hard to reverse or hard to notice before a user does. Judge this yourself from the project and the change; when unsure between `standard` and `thorough`, pick `thorough`.

At `thorough`, read and follow [references/thorough.md](references/thorough.md) instead of the `quick` and `standard` steps; the "Checking it works", "Time budget" and "Final message" sections still apply.

## `quick`

Must prove: the change compiles and does not break existing tests.

1. Implementation.
2. Typecheck of the affected workspace or package.
3. Existing tests of the changed files or modules.
4. Render only for a visual change.

Approximate verification overhead: ~1–3 min.

## `standard`

Must prove: the changed feature works in the running application.

1. Everything from `quick`.
2. Checking it works (below) — the happy path of the changed behavior.

Approximate verification overhead: ~5–10 min (+~2 min for a cold app start).

### Checking it works

Tests do not replace checking that the feature works. Start the application (or use one already running) and go through the changed feature the way a user or API client would:

- UI → isolated Playwright session and an observable effect on screen, per the [UI guidance](references/browser-review.md);
- API/backend → call the local endpoint and check the response;
- logic without an interface → a test or a short script calling the changed code.

Confirm data writes by reading back (reload, repeated GET, admin view). Check error scenarios only when the change concerns error handling or you found a problem. When the app cannot be started, record it in the final message as a limitation, not a pass; if possible, check the behavior through another channel and state clearly what it actually confirms.

## Time budget

Overheads are approximate, not limits. When verification clearly exceeds the level's overhead (e.g. more than twice), do not extend it further without a concrete detected problem, and in the final message say what took the time.

## Final message

Give the result in the final chat message; do not write it to Markdown, the plan or the issue, and do not create acceptance.md. A summary of the verification reaches the PR only through `raven-pr`. Do not start the next stage. The final message contains:

- the level (and any raise, with the reason);
- what changed, including deviations from the plan (what, why);
- what was checked — at `standard` also what exactly was observed and through which channel;
- limitations: checks not run or blocked, and what remains to be checked;
- step-by-step acceptance instructions: concrete actions or commands and the expected effect, with detail matched to the change.

When blocked, also give the summary and instructions, clearly naming what is missing.
