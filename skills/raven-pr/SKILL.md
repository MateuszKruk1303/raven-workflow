---
name: raven-pr
description: "Push the branch and create or update the PR of the given change, linked to its issue or external ticket. Only on explicit request; no merge."
argument-hint: "[#issue | ticket URL]"
---

# Raven PR

Follow [working on GitHub tasks](../raven-workflow/references/git-workflow.md). Talk to the user in their language; write the PR description in the language the repository uses.

Invoking `raven-pr` is consent to an ordinary push of the current branch and to creating or updating its PR. Do not ask for it again.

1. Determine the repo, branch, base and issue or external ticket (from the argument, the context or the key in the branch name). When the current branch is the default branch, create a new branch from HEAD following the project's convention (`git switch -c`) and push only that; do not reset the local default branch, and say in chat that it is ahead of the remote. Never push directly to the default branch. Commit all uncommitted work on the branch (modified and untracked files, including the plan and other files in `context/changes/`) in logical steps; only files ignored by Git stay out.
   - **Secret check before every commit.** Scan the staged diff (`git diff --cached`) for API keys and credentials: provider key formats (e.g. `sk_live_`/`sk_test_`/`rk_`, `AKIA`, `ghp_`/`github_pat_`, `xox[bap]-`, `AIza`), private key blocks (`-----BEGIN ... PRIVATE KEY-----`), connection strings with a password, and literal values assigned to names like `*_KEY`, `*_SECRET`, `*_TOKEN`, `PASSWORD`. Also never stage `.env*` files other than templates (`.env.template`, `.env.example`). Placeholders, test fixtures with obviously fake values and publishable keys meant for the client (e.g. `pk_` in a template) are not findings.
   - On a finding: unstage it, do not commit, push or open the PR, and report the file and line to the user without printing the value. Continue only after the user decides.
2. Find an existing PR for this branch; update it instead of creating a duplicate. After a timeout, read the state first, then retry if needed.
3. Ordinary push, no force-push. PR description: problem and outcome, `Closes #N`, or for ticket work the ticket per [external ticket](../raven-workflow/references/git-workflow.md#external-ticket) (an explicit issue wins), scope, a `## Verification` section per the [rules](../raven-workflow/references/git-workflow.md#verification-and-reporting), known gaps. Take the verification from the final message of `raven-auto-implement`, `raven-test` or a review in the current context; do not add checks you cannot see. When updating the PR, refresh the section with new checks. Pass a multi-line body through a file (`--body-file`). Draft when the user asks for it or the work is incomplete.
4. Read the PR back after writing (URL, head, base, state) and give it in chat together with any gaps.

Do not merge, change branch protection or close the issue. A local test result is not CI.
