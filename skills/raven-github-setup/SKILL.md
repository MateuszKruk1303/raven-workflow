---
name: raven-github-setup
description: "Prepare or complete a GitHub repo for working on tasks: remote, enabled Issues, in-progress/blocked labels; a Project only on request."
argument-hint: "[owner/repo]"
---

# Raven GitHub Setup

Follow [working on GitHub tasks](../raven-workflow/references/git-workflow.md). Talk to the user in their language.

1. **Target.** The repo from an explicit instruction or an unambiguous remote; resolve a conflict before writing. Check the account (`gh auth status`) and owner/repo without revealing tokens. No access does not mean the resource is missing.
2. **Repo.** Create a requested new repo as private; do not change the visibility of an existing one without an instruction. Do not put confidential company content into a personal repo by assumption.
3. **Issues.** Check that they are enabled, and that the `in-progress` and `blocked` labels (or their existing equivalents) exist. Create only the missing ones.
4. **Project (optional, on request).** A view of the same issues, not a second work state. Map fields and options by ID, keep existing statuses and automations.

Do not create test issues or PRs, and do not configure secrets, CI, branch protection or deploy on the side. In chat: the repo, the readback result after writing and remaining gaps.
