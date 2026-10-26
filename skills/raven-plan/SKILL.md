---
name: raven-plan
description: "Prepare a plan for one change: requirements from the issue or an external ticket (Jira, Linear and similar), decisions and approach in the project's code. Optionally request one independent plan review. The plan is one-off working context for raven-auto-implement."
argument-hint: "[#issue | ticket URL | change-id]"
---

# Raven Plan

Follow [working on GitHub tasks](../raven-workflow/references/git-workflow.md) and [change boundaries](../raven-workflow/references/change-scope.md). Talk to the user in their language; write the plan in the user's language unless the project already uses another.

The plan gathers what the implementer needs to do the job well: outcome, settled decisions, approach in the real code and how to verify it. It is neither a contract nor a tracker. A small change needs no plan — point straight to `raven-auto-implement`.

## Input

Accept an issue, description, change ID or an existing plan. Read the issue body (scope and AC), the referenced sources and decisions, and `context/foundation/lessons.md` if present. For a new issue, assign yourself, set `in-progress` and create a branch per [working on GitHub tasks](../raven-workflow/references/git-workflow.md). A request to plan one change does not authorize reorganizing the queue.

An external ticket link or key is the requirements source: read it, find or create its branch per the [external ticket](../raven-workflow/references/git-workflow.md#external-ticket) rules (read-only, no GitHub issue) and use the key as the change ID. Gaps and contradictions in the ticket go into the planning questions; the answers go into the plan, not the ticket.

## Steps

1. **Boundaries.** Before detailed research, judge whether this is one independently acceptable outcome. A scope that is too wide goes back to the user with a split proposal and a first change.
2. **Code.** Investigate only what settles feasibility, contracts and acceptance: existing patterns, architecture, tests. A negative search result does not prove absence.
3. **Questions.** Ask only about real unsettled product or architecture decisions, with a recommendation and trade-off — [examples](references/questions.md). Settle technical details within the agreed boundaries yourself.
4. **Write.** Save `context/changes/<id>/plan.md` following the [template](references/plan-template.md), proportionate to the change. Split the work into vertical slices with their contracts and dependencies, so independent slices can be built in parallel; name the flow tests in Verification.

## Plan review (optional)

Run it when the user asks, or when the plan touches a costly or hard-to-reverse change. One fresh subagent without the author's transcript gets the plan, the issue or the ticket content as read, and access to the code. It assesses read-only: one outcome and requirement coverage, feasibility against real files and APIs, fit with the architecture, error and migration handling, observable AC and tests. Every finding has a severity (critical/warning/suggestion), location, impact and recommendation.

Fix confirmed findings within the agreed boundaries yourself in one round; a change of requirements or scope goes back to the user. Give the review result in chat, without a separate file. Without the ability to launch a fresh subagent, report the missing review; self-assessment is not a review.

## Final message

In chat: the plan path, key decisions, open issues (if any), the review result (if there was one) and the next step `/raven-auto-implement <id>` (for a ticket, its link). Writing the plan does not start implementation. When the host does not allow writing the file, give the plan in chat.
