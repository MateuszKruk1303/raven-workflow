---
name: raven-plan
description: "Prepare a plan for one change: business requirements from the issue or an external ticket (Jira, Linear and similar); every technical decision (technology, vendor, architecture, contracts, data, tests, CI) settled here with the user, and the approach in the project's code. Optionally request one independent plan review. The plan is one-off working context for raven-auto-implement."
argument-hint: "[#issue | ticket URL | change-id]"
---

# Raven Plan

Follow [working on GitHub tasks](../raven-workflow/references/git-workflow.md) and [change boundaries](../raven-workflow/references/change-scope.md). Talk to the user in their language; write the plan in the user's language unless the project already uses another.

The plan gathers what the implementer needs to do the job well: outcome, settled decisions, approach in the real code and how to verify it. It is neither a contract nor a tracker. The issue holds only the business side; the plan owns the whole technical layer: technology and vendor choice, architecture, contracts, data, events, tests and CI. A small change needs no plan — point straight to `raven-auto-implement`.

## Input

Accept an issue, description, change ID or an existing plan. Read the issue body (outcome, business rules, scope, AC, open questions, Sources including the user's technical hints), the referenced sources and decisions, the accepted prototype in `context/prototypes/` that the issue's Sources name or whose `notes.md` Source names this issue, its epic or ticket (read `notes.md`; open its `index.html` only for UI states; the issue body wins, and a difference is a business question) and `context/foundation/lessons.md` if present. An epic is not planned; handle it per [labels and epics](../raven-workflow/references/git-workflow.md#labels-and-epics). Otherwise, for a new issue, assign yourself, set `in-progress` and create a branch per [working on GitHub tasks](../raven-workflow/references/git-workflow.md); the issue number is the change ID. A request to plan one change does not authorize reorganizing the queue.

An external ticket link or key is the requirements source: read it, find or create its branch per the [external ticket](../raven-workflow/references/git-workflow.md#external-ticket) rules (read-only, no GitHub issue) and use the key as the change ID. Gaps and contradictions in the ticket go into the planning questions; the answers go into the plan, not the ticket.

## Steps

1. **Boundaries.** Before detailed research, judge whether this is one independently acceptable outcome. A scope that is too wide goes back to the user with a split proposal and a first change.
2. **Code.** Investigate only what settles feasibility, contracts and acceptance: existing patterns, architecture, tests. A negative search result does not prove absence. Facts are your job: never ask the user what the code, the tools or the sources can tell you. When the host allows, a larger exploration goes to a subagent; meanwhile ask the questions that do not depend on its result.
3. **Sketch.** The first round of questions carries a sketch in chat: the current behavior, the behavior after the change and the intended direction, 2–3 sentences in total, so a misunderstanding surfaces before the details. When the direction depends on an open question or on exploration still running, describe it for the recommended option and mark it provisional. No file yet. With nothing to ask, skip the sketch and write the plan.
4. **Questions.** Ask about real unsettled decisions, each with a recommendation and trade-off; run the undefined-terms pass from [planning questions](references/questions.md) before choosing them. Ask in rounds: a round holds only questions whose prerequisites are already settled; a question whose meaning depends on another one still open waits for a later round. After each answer recompute what is now askable. The interview ends when no decision is left silently assumed: each one is settled with the user (a decision they hand back to you counts, recorded with its reason), recorded in a linked source, or a minor detail within the agreed boundaries. One the user cannot answer yet goes into the final message as open.
   - **Business.** A missing or ambiguous business rule, including the issue's Open questions: ask the user, never assume it. Record the answer in the plan and propose recording it in the issue through [raven-issue-update](../raven-issue-update/SKILL.md), running it when the user agrees; do not keep a business rule silently only in the plan. For an external ticket or a plain description without an issue, the answer goes into the plan only and the final message names it (Raven never writes to the ticket).
   - **Technical.** Technical and architecture decisions with a real alternative: technology or vendor, plugin or own module, where the data lives, synchronous call or event, contracts. A technical hint from the user in the issue's Sources, or a decision already recorded in the linked PRD, ticket or `context/foundation/architecture.md`, is the default; do not re-ask it unless the code shows a significant reason against it or it leaves a real choice open. Technical content or assumptions an agent wrote into an older issue are proposals, not decisions.
   - Settle minor technical details within the agreed boundaries yourself.
5. **Write.** Save `context/changes/<id>/plan.md` following the [template](references/plan-template.md): core sections always, conditional ones only when their condition holds. Split the work into vertical slices with their contracts and dependencies, so independent slices can be built in parallel. Name the flow tests and other technical criteria (lint, CI, migrations) in Verification; they never become issue AC.

## Plan review (optional)

Run it when the user asks, or when the plan touches a costly or hard-to-reverse change. One fresh subagent without the author's transcript gets the plan, the issue or the ticket content as read, and access to the code. It assesses read-only:

- one outcome and requirement coverage; observable AC;
- feasibility against real files and APIs; reuse of the project's established primitives instead of parallel inventions;
- a failure mode and user-visible behavior for every external call, migration and long-running job;
- rollback described as precisely as the forward path for every hard-to-reverse state change (migration, backfill, data written by a job);
- sensitive data the change touches following the project's protection conventions;
- every slice verifiable by a test and leaving the app working.

Every finding has a severity (critical/warning/suggestion), location, impact and recommendation. The result ends with its limits: what was examined, what was not checked or lacked evidence.

Fix confirmed findings within the agreed boundaries yourself in one round; a change of requirements or scope goes back to the user. Give the review result in chat, without a separate file. Without the ability to launch a fresh subagent, report the missing review; self-assessment is not a review.

## Commit

After the plan and any review fixes are written, commit only `context/changes/<id>/plan.md` on the change's branch following the project's commit convention (e.g. `docs: plan for #12`), so the plan travels with its branch and does not leak into another change. Skip the commit when the project instructions say not to commit plans. No push.

## Final message

In chat: the plan path, key decisions, open questions (if any), the review result (if there was one) and the next step `/raven-auto-implement <id>` (for a ticket, its link). Writing the plan does not start implementation. When the host does not allow writing the file, give the plan in chat.
