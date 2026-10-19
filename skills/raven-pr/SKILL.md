---
name: raven-pr
description: "Push the branch and create or update the PR of the given change, linked to its issue. Only on explicit request; no merge."
argument-hint: "[#issue]"
---

# Raven PR

Follow [working on GitHub tasks](../raven-workflow/references/git-workflow.md). Talk to the user in their language; write the PR description in the language the repository uses.

Invoking `raven-pr` is consent to an ordinary push of the current branch and to creating or updating its PR. Do not ask for it again.

1. Determine the repo, branch, base and issue. When the current branch is the default branch, create a new branch from HEAD following the project's convention (`git switch -c`) and push only that; do not reset the local default branch, and say in chat that it is ahead of the remote. Never push directly to the default branch. Check the working tree: only your own work goes into a commit, other people's changes stay untouched. Commit your own uncommitted work in logical steps.
2. Find an existing PR for this branch; update it instead of creating a duplicate. After a timeout, read the state first, then retry if needed.
3. Ordinary push, no force-push. PR description: problem and outcome, `Closes #N`, scope, a `## Verification` section per the [rules](../raven-workflow/references/git-workflow.md#verification-and-reporting), known gaps. Take the verification from the final message of `raven-auto-implement`, `raven-test` or a review in the current context; do not add checks you cannot see. When updating the PR, refresh the section with new checks. Pass a multi-line body through a file (`--body-file`). Draft when the user asks for it or the work is incomplete.
4. Read the PR back after writing (URL, head, base, state) and give it in chat together with any gaps.

Do not merge, change branch protection or close the issue. A local test result is not CI.
