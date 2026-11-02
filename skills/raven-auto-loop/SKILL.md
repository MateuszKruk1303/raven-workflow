---
name: raven-auto-loop
description: "Deliver a given scope of GitHub issues unattended, one after another: for each ready issue a fresh agent runs raven-auto-plan, raven-auto-implement and raven-pr, then the loop merges the PR and moves on. Invoking it with a scope is consent to push and merge within that scope. Use only on an explicit request for an autonomous loop."
argument-hint: "<#issues | #from..#to | milestone | label | all open> [— time limit]"
disable-model-invocation: true
---

# Raven Auto Loop

Coordinate the delivery of a scope of issues without the user. You are the coordinator: you pick the next issue, hand it to a fresh agent, merge its PR and keep the state honest. You do not plan or implement yourself. Follow [working on GitHub tasks](../raven-workflow/references/git-workflow.md). Talk to the user in their language.

## Scope and consent

The argument sets the scope: explicit issues, a range, a milestone, a label or all open issues of the repo, optionally with a time limit. Without a scope, ask once and wait. Invoking the loop with a scope is the user's explicit instruction, for issues in that scope only, to take them up, push their branches, open PRs and merge them — what [raven-pr](../raven-pr/SKILL.md) and [raven-merge](../raven-merge/SKILL.md) require. It is not consent to change the queue: do not create, split, reorder or close issues other than by merging their PR.

**Preflight**, once: note the start time (`date`); check `gh` access, the default branch and that the working tree is clean or holds only work of an `in-progress` issue in scope; make sure the `in-progress` and `blocked` labels exist (create the missing ones). Say in one line what will run and that an unattended run needs a permission mode in which git, `gh` and the project's commands do not prompt. Then continue without asking.

## The loop

1. **Pick.** Check the time (`date`). Read the open issues in scope. An issue is ready when it has no `blocked` label and every issue in its Dependencies section and its GitHub "blocked by" relations (`gh api repos/<owner>/<repo>/issues/<n>/dependencies/blocked_by`; when the API does not offer them, the section alone) is closed; a dependency outside the scope that is still open leaves the issue not reached. Take an issue already `in-progress` first (resume), then the lowest-numbered ready one. Skip an issue whose branch `git worktree list` shows checked out in another worktree; it is worked on there, so report it as not reached. None ready → finish.
2. **Prepare.** New issue: `git switch <default>` and `git pull --ff-only`. Resumed issue: switch to its existing branch. An issue whose PR is already merged but which is still open is only closed (step 4 cleanup).
3. **Delegate.** Spawn one fresh agent for the issue; it runs all three skills in one context, in order: `raven-auto-plan` (skip when the plan already exists), `raven-auto-implement` (skip to its final checks when the branch already holds the implementation), `raven-pr` (it updates an open PR). It reads their `SKILL.md` from the project's or the user's skills directory when the Skill tool cannot load them. Give it the repo path, the issue number, the consent above for push and PR of this issue, the reason of a previous failed attempt if any, and these rules:
   - Never ask the user and never merge. Choose the verification level yourself.
   - Uncommitted changes on the issue's branch are this issue's earlier work.
   - A question that an inner skill would ask the user (an unresolved Open question, a missing product decision, a raven-auto-plan stop, a raven-pr secret finding) ends the run as `blocked` with the question; for a GitHub issue, replace `in-progress` with `blocked` and comment the question with options and a recommendation.
   - A usage limit or another environment failure ends the run as `interrupted` with the error text.
   - Return: outcome (`pr-ready` / `blocked` / `failed` / `interrupted`), PR URL, agent decisions, checks run with results, and the reason of any stop.
4. **Check and merge** `pr-ready`. Read the PR back: it links the issue and its Verification reports the checks the project instructions require (e.g. typecheck, tests, build) as run and passed; anything not run or failing makes it `failed`. Then apply raven-merge. When the repo has no required CI checks, the local checks in the Verification are the gate: say "no CI" in the progress line and merge; when it has them, wait for green. Afterwards confirm the issue is closed without `in-progress`.
5. **Retry once.** On `failed`, start one more fresh agent on the same branch with the failure reason; it reruns the final checks before raven-pr. After the second failure, replace `in-progress` with `blocked`, comment the reason and what was tried, leave the branch and PR, and continue with issues that do not depend on it.
6. **Progress:** one chat line per issue (merged / blocked / failed / interrupted, PR link). Back to step 1.

## Stop

Finish when no issue in scope is ready; when the time limit has passed (do not start a new issue after it); or on `interrupted` — the issue stays `in-progress` and the next invocation with the same scope resumes it first. Do not wait for a usage reset; report its time if known. Keep no loop state outside GitHub and Git. `blocked` issues are skipped on later runs until the user answers and removes the label.

Do not force-push, use `--admin` or bypass protections, hooks or permission denials; report them.

## Final message

In chat: merged PRs with their issues; agent decisions per issue, business ones first, for the user to confirm or move into the issue; blocked issues with their questions or failure reasons; issues in scope not reached and why; the local checkout (branch, clean or not).
