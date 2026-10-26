# Working on GitHub tasks

Work happens on tasks in GitHub Issues. The issue body holds only the business requirements and behavioral acceptance criteria ([issue template](../../raven-roadmap/references/issue-template.md)); technical decisions belong to the plan (`raven-plan`), or without a plan to the implementer, who asks when there is a real alternative. When the source is Jira, the issue links the ticket without copying its content. `raven-plan` and `raven-auto-implement` can also work straight from an external ticket, without a GitHub issue ([below](#external-ticket)).

## Task, plan, branch

- One issue is one branch and one PR. A quick drive-by change needs neither an issue nor a plan.
- The plan (`context/changes/<id>/plan.md`) is optional, one-off working context for the agent: outcome, decisions, approach, verification. It is not a contract. Do not version it or keep checkpoints, statuses or reports in it. A new requirement goes into the issue or the instruction, without updating the plan.
- Read the state of work from the issue (state, assignee), the branch, commits and the PR, not from conversation memory. Do not scan the board. When the user has not named a task and the order is not obvious, ask.
- When taking up an issue (`raven-plan`, or `raven-auto-implement` without an earlier plan), assign yourself and set the `in-progress` label (plus the In progress status if the project uses a GitHub Project).
- For a new issue, create a branch from the current base (`git pull --ff-only`) following the project's convention. When resuming, use the existing branch. A branch whose PR was merged does not point to the next task.
- Never commit or push directly to the default branch. A drive-by change without an issue also gets a short branch following the project's convention.
- Preserve other people's changes in the working tree. Do not switch branches or update the base when they conflict; ask how to preserve them. No automatic stash, reset or commit of someone else's changes.
- Commit logical steps following the project's convention.

## External ticket

A Jira, Linear or similar ticket given to `raven-plan` or `raven-auto-implement` takes the place of the issue: the ticket is the specification, one ticket is one branch and one PR.

- Read its description, acceptance criteria, comments and the attachments or linked items needed for the change through an available connector (MCP), the tracker's CLI or an authenticated fetch. A GitHub issue URL is an issue, not a ticket. When the ticket cannot be read, name the missing access and ask the user to paste its content; do not guess the scope from the URL or key.
- Raven never writes to the ticket: no assigning, transitions, comments or edits, and no Jira smart-commit commands (`#comment`, `#time`, transitions) or closing words before the key (`Closes`/`Fixes`/`Resolves PP-1234`) in commits or the PR; reference it plainly, e.g. `Ticket: PP-1234 <link>`. The ticket's status is not work state.
- Find existing work by the exact key (not followed by a digit, so `PP-12` does not match `PP-123`) in local and remote branches (after `git fetch`) and in open PRs. A branch whose PR was merged is not existing work; follow-up work on the same key gets a suffix, e.g. `feat/PP-1234-2`. With several candidates, ask. Without one, create a branch from the current base (`git pull --ff-only`) named `feat/<KEY>` (e.g. `feat/PP-1234`) unless the project instructions set another branch convention, and reference the key in commits where the convention allows it.
- When an explicit `#issue` is also given, the issue path applies and the ticket stays a linked source.

## Publishing

- Push, PR and merge only on an explicit user instruction.
- The PR links the issue (`Closes #N`), or the external ticket when the work came from one (key and link; with only the key known, give the key and do not construct a URL), describes the change briefly and has a "Verification" section (below).
- Merge requires green required CI and the user's consent. After merge, check that the GitHub issue is closed; work from an external ticket has no issue to close and the ticket is not transitioned. Deploy is a separate operation.

## Verification and reporting

- A check that was not run or was blocked is never reported as passed.
- Give verification results and acceptance instructions in the final chat message. Do not create reports, acceptance.md or copies of them in the issue unless the user asks.
- The exception is the PR: its "Verification" section is a short durable trace for the reviewer — level (`quick`/`standard`/`thorough`, if there was one), checks run with channel and result, what was not checked. Only what was actually run and is visible in context; without evidence write "not confirmed". Local checks are not CI.
- A review or test delegated to a separate agent runs in a fresh context without the author's transcript. The reviewer does not fix the work under review.

## Limits

- No GitHub access does not block local work. Report the operation that was not performed; do not create a substitute local backlog.
- Leave historical artifacts (old plans, checkpoints, reports, acceptance fields) as they are. They are not gates and need no migration.
