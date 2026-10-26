---
name: raven-issue-update
description: "Weave an additional or clarified requirement into the body of a given existing GitHub issue. Optional helper for updating scope and acceptance criteria, without reorganizing the roadmap or implementing the change."
argument-hint: "[#issue] [requirement]"
---

# Raven Issue Update

Follow [working on GitHub tasks](../raven-workflow/references/git-workflow.md). Talk to the user in their language; keep the issue's existing language.

The instruction "update the issue with…" covers writing **the body of one given existing issue**. Do not require additional routine consent for that write. A plain question, an idea without a write instruction or a request for a proposal stays read-only. Do not create new issues, comments or a local backlog; do not change the title, dependencies, order, status, assignee, plan, code, PRD or Jira. Do not take up the task as In progress: writing a requirement does not start planning or implementation. This is an optional helper, without a mandatory review of every update.

## Establish the target and intent

Resolve the exact issue URL/number or change ID from the repo instructions, the remote and the given plan. A bare number needs an unambiguous repo, a change ID needs an unambiguous mapping. Do not pick the newest/similar issue and do not scan the whole queue. With a missing target, ask only for its identification.

Read the current full body, the issue state and its link to a PR/change. Read the sources and decisions needed for the edit, including referenced threads. Do not copy the whole history or Jira tickets. Distinguish a new user requirement from an existing decision and from a technical proposal.

The issue is business-only, with the content bans of the [issue template](../raven-roadmap/references/issue-template.md). Do not weave in a technical requirement: decline it and say it belongs in the plan made with [raven-plan](../raven-plan/SKILL.md). If the user still wants it on the issue, record it only as one Sources line, `Client's technical hint, to settle in the plan: …`. When a business parameter the requirement needs is missing, ask the user per [planning questions](../raven-plan/references/questions.md); never assume it. An unanswered rule goes to Out of scope or Open questions. Do not clean up other technical content or agent assumptions already in the body on the side.

If the issue is closed or its change is merged, clarify before editing whether this corrects the description of delivered behavior or is new scope. Do not add unfulfilled scope to finished work, do not reopen the issue and do not create a follow-up on the side.

A significant contradiction with an earlier requirement, exclusion or decision needs the user's resolution before the dependent write. Show the concrete contradiction and ask about intent; do not weaken the addition or widen it yourself to fit the old text. An unambiguous instruction to replace an earlier requirement is already a decision. Settle minor editorial details yourself. When the addition requires changing other issues or splitting work, name the need for a separate [raven-roadmap](../raven-roadmap/SKILL.md), without reorganizing in this invocation.

## Weave the requirement in

Prepare the smallest semantic change to the existing description: extend the relevant business rules, scope and observable acceptance criteria, and possibly the directly affected exclusion, open question or outcome description. Run the template's sentence check on every new sentence. Keep the issue's structure. Do not end with a loose "to remember", a comment or a note under the finished text. AC describe the outcome the user requires, without inventing parameters, guarantees or implementation decisions.

Keep the rest of the content, AC identifiers, links, decisions, managed markers/sections and progress. Do not extend the meaning of a checked `[x]` with an unverified condition: keep the passed item and record the new duty as a separate unchecked AC. Do not reset existing checkboxes or mark new ones as done. If the requirement already follows from the scope and AC, finish as a no-op pointing to the existing text; a different phrasing alone does not justify a duplicate.

The issue holds business requirements; the plan is one-off working agent context, not a contract. For an active change, writing to the issue is enough: do not update the plan, do not suggest it needs review and do not start a cycle. Implementation will take the requirement from the issue or the instruction. Do not edit historical decisions or PASS results; earlier evidence does not confirm the new scope.

## Write and confirm

Use an available connector/API or `gh` per its current help; do not require a specific integration. Before writing, check the difference: only the agreed addition and its necessary connections in the body. For the CLI, pass the exact multi-line body through a temporary file and `--body-file`, without interpolating content into a shell command.

Re-read the body and state right before writing. If they changed since drafting, build the delta on the latest content, preserving other people's changes; clarify a conflict of meaning before writing. If the API supports a conditional version write, use it. A plain read → write is not a lock: on signs of a concurrent edit that cannot be safely resolved, stop the write instead of overwriting someone else's work. Do not send fields outside the body or a stale payload after a version conflict.

After writing, read the issue and check the requirement, the AC and the preservation of earlier content/progress. After a timeout, read the state first: if the change already exists, do not retry; if it is missing, prepare a possible retry on the current content. A failed read does not mean a failed write. After two unsuccessful attempts at the same write, finish with an explicit unconfirmed result and a ready proposal in the conversation; do not automatically restore the old body.

No GitHub access or write permission does not create a local backlog: give in the conversation a ready fragment to weave in, or the full proposed body if the original was read, and name the operation not performed. Without the original, do not claim a complete merge. When resuming, read the actual state and account for earlier attempts instead of assuming the last mutation failed.

Give the issue link, briefly what was woven in, and the readback result or no-op/unperformed write. Do not claim finished implementation or updates of other artifacts.
