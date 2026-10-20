---
name: raven-merge
description: "Merge the given PR after green CI and the user's consent, then confirm its GitHub issue, if any, is closed. Deploy is separate."
argument-hint: "[#PR | #issue]"
---

# Raven Merge

Follow [working on GitHub tasks](../raven-workflow/references/git-workflow.md). Talk to the user in their language.

The instruction "merge <PR/change>" is consent to merge the unambiguously identified PR. Do not ask for it again; with several candidates, establish which one.

## Before merge

Read the current head, base, draft state, mergeability, required checks and reviews, branch protection and merge queue. FAIL, a conflict or a missing required check blocks the merge; pending means waiting. No access to protection data does not mean there is none. Do not use `--admin` or any bypass, and do not approve your own PR.
## Merge

Use the method required by the repo policy; without a preference, the first allowed of: squash, merge commit, rebase. Merge exactly the checked head (`gh pr merge --match-head-commit <SHA>`); with a queue, use its mechanics. After the request, including after a timeout, read `mergedAt` and the merge commit; do not blindly send a second request.

## After merge

Check that the linked GitHub issue is closed (ticket-only work has none; never close or transition an external ticket); if not, close it and remove the `in-progress`/`blocked` labels. If that fails, report "PR merged; issue needs closing", without reverting the merge. In chat give the PR, merge commit, issue state (if there is an issue) and the state of the local checkout. Merge does not start the next task or a deploy.
