---
name: raven-auto-plan
description: "Prepare a plan for one change without asking the user: the unattended variant of raven-plan for autonomous loops. Every decision raven-plan would ask is settled by the agent with the recommended option and recorded as an agent decision for later review; stops only on an irreversible or contradicting decision. Use only when the user asks for unattended planning; otherwise use raven-plan."
argument-hint: "[#issue | ticket URL | change-id]"
---

# Raven Auto Plan

Do everything [raven-plan](../raven-plan/SKILL.md) does — input, boundaries, code research, the [plan template](../raven-plan/references/plan-template.md), slices and Verification — with one difference: never ask the user. The user chose this skill to keep an unattended loop moving and reviews the agent's decisions afterwards. Talk to the user in their language; write the plan in the user's language unless the project already uses another.

## Deciding instead of asking

Where raven-plan would ask a question (business or technical, including the issue's Open questions), decide yourself:

1. A decision already recorded in the issue, its Sources, the PRD, `context/foundation/architecture.md`, `lessons.md` or an earlier plan is the answer; do not reopen it.
2. Otherwise build the question as [planning questions](../raven-plan/references/questions.md) describe — real options, each with a strength and cost — and pick the recommended one, in this order of precedence: fits the existing code and architecture, meets the AC with the smallest scope, easiest to reverse with a follow-up PR. A missing business rule is decided the same way when a sensible default exists (the most common or conservative behavior the AC allow); it is then a **business** agent decision.
3. Record it in the plan under `## Agent decisions`, placed right after "Decisions and approach", one line each: **business** or **technical**, the decision, the chosen option, the rejected alternatives, why, and how to reverse it. Keep minor details settled within agreed boundaries out of this list, as raven-plan does.

Business decisions stay in the plan; do not write them into the issue and do not run raven-issue-update. The final message lists them so the user can confirm or move them to the issue later.

## When to stop

The loop merges without review, so "reversible" means reversible by a follow-up PR without losing data or breaking users. Do not decide, and write no plan, when the choice:

- contradicts the issue, PRD or an accepted architecture decision, or needs changing one of them;
- is hard to reverse after merge: destructive data migrations, paid services or vendor contracts, publishing, breaking a public API, changing the auth or permission model, or secret handling beyond what is already agreed;
- is a business rule with no sensible default (e.g. a price, rate or legal term that only the user can set);
- needs a too-wide scope split (raven-plan step 1) — a split changes the queue, which is the user's call.

Then, for a GitHub issue, replace `in-progress` with `blocked` and comment on the issue with the question, its options and your recommendation; leave the branch as it is. For an external ticket report the stop in chat only (the ticket is read-only). The caller moves on to independent work.

Taking up the issue (assignee, `in-progress`, branch) follows raven-plan. Run raven-plan's optional plan review without being asked when the plan touches a costly or hard-to-reverse area that did not trigger a stop.

## Final message

In chat: the plan path, the list of agent decisions (business ones first), any stop with its question, and the next step `/raven-auto-implement <id>`. Writing the plan does not start implementation.
