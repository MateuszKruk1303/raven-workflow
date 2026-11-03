---
name: raven-roadmap
description: "Create or refresh a queue of self-contained changes as GitHub Issues, sourced from the PRD, given Jira tickets, sprint or epic, or a task description the user asks to turn into issues (no PRD needed). Places new issues among existing ones with dependencies and order, grouped into epics (native sub-issues) the user accepts. Settles business rules with the user first; issues are business-only. No technical decisions, no implementation plans and no writes to Jira."
argument-hint: "[prd path | Jira keys | task description]"
---

# Raven Roadmap

Follow [working on GitHub tasks](../raven-workflow/references/git-workflow.md) and [change boundaries](../raven-workflow/references/change-scope.md). Talk to the user in their language; write issues in the language the repository uses, or the user's language for a new repository.

The roadmap is GitHub Issues in the established repo: one issue = one independently acceptable outcome. A roadmap request covers writing those issues. A Project is an optional view. Do not create a local roadmap or a second backlog. An addition to one existing issue is [raven-issue-update](../raven-issue-update/SKILL.md), not a queue reorganization.

An issue is business-only: outcome, business rules, scope and behavioral AC per the [issue template](references/issue-template.md). Every technical decision is made later in [raven-plan](../raven-plan/SKILL.md), together with the user. A business rule is the user's to settle; never assume one.

Every sentence of an issue traces to the source or to the user's answer. Content you derived yourself (an extra edge case, a message wording, an admin view, an exclusion) is left out, or asked about in the interview only when it changes scope or an acceptance criterion. A short issue with only agreed content beats a complete one with additions the user never settled.

## Source

- **PRD** (`context/foundation/prd.md` or a given document): cover the whole agreed PRD — every requirement has its change, evidence of earlier delivery or an explicit deferral.
- **Jira** (keys, URL, sprint, epic): fetch descriptions, AC and relations only for that scope. A Jira epic or sprint is a container, not a change (a natural candidate for one GitHub epic); one ticket can be a change, a too-wide one gets split. The GH issue links the ticket (with ID and update date) without copying its text or status; it holds the business rules and behavioral AC in its own words, including the answers from the interview. Never write to Jira. A Jira Done status does not prove a merge.
- **Task description** (text in the prompt): the user's description is the requirement; no PRD or Jira is needed. Cover only what it asks for; the user chooses the granularity of the split (below); quote it in Sources. Its gaps go into the business interview, never into assumptions. Read the PRD when it exists only to check the task does not contradict it.

An accepted prototype in `context/prototypes/` (from [raven-prototype](../raven-prototype/SKILL.md)) shows how its flow should work: read its `notes.md` with the source. A rule that lives only there is a business question, not a source. An issue delivering an accepted flow names it in Sources, per the [issue template](references/issue-template.md).

Technical hints in the user's own words (e.g. "use the official plugin") do not enter the issue body; record each as one Sources line, `Client's technical hint, to settle in the plan: …`. Technical content of a PRD or ticket stays in that source; a technical decision the source already settles (e.g. an approved vendor) gets at most one Sources line pointing to it, per the template.

## Code

Read the code only to avoid duplicating delivered behavior, to detect a conflict with existing behavior and to set dependencies between issues right. A conflict becomes a business question to the user. Technical findings do not go into the issue.

## Business interview

Before writing a new or changed issue, settle its business rules with the user through `AskUserQuestion`, whatever the source; do not re-interview untouched issues on a refresh. Format each question per [planning questions](../raven-plan/references/questions.md): concrete data, a recommendation first, and a strength and cost for every option. Run its "Undefined terms" pass (tiebreaks, thresholds, counting) on the business rules.

Ask only about business rules, for example:

- parameters: rates, thresholds, limits, rounding;
- timing: when something is granted, expires or is reversed;
- who it applies to: guests, registered customers, segments;
- currencies and markets;
- edge cases: return, cancellation, partial refund, negative balance;
- what the customer sees and what the admin sees.

Keep it proportionate: do not ask what the source already states unambiguously, and group at most 4 questions per round, asking first the rules that change scope or that other answers depend on. Stop when every rule that changes scope or an AC is answered, placed in Open questions or left out of scope by the user, or when the user asks to stop; remaining unknowns go to Open questions. Never ask about technology, architecture or implementation. When the user does not know an answer or declines to decide, the rule goes to Out of scope as consciously unhandled or to the issue's Open questions — never into an assumption made by the agent.

## Split

Split into vertical outcomes (UI, API, data and validation together), not layers or phases; the issue describes that outcome as behavior, without naming the layers. The dependency graph is acyclic. Briefly justify a larger inseparable scope. Propose the split of a PRD or Jira scope yourself after the business interview, then show it to the user (issue titles, one-line outcomes, dependencies and any PRD requirement you propose to defer) and write only after they accept it; on a refresh show only the added and changed issues; changing requirements or priorities needs the user's decision.

**Epics and labels.** Every split preview, at every granularity, also shows the grouping: the epic each issue goes into (an existing one first, otherwise a proposed one with its title and one-line goal) and any label it would get. An epic groups related outcomes for orientation; it is never a change of its own. Propose one only for a group of at least two issues; a small queue needs none, and each issue has at most one epic. Find existing epics by `sub_issues_summary.total` above 0. On a refresh, putting an existing issue into an epic or moving it is a change to that issue: show it in the preview. Group only with epics, and add no milestones the repo does not already use; labels follow [working on GitHub tasks](../raven-workflow/references/git-workflow.md#labels-and-epics). Nothing in the grouping is written that the user did not see and accept.

**Task description: the user chooses the granularity.** After the business interview and before writing, present three split proposals through `AskUserQuestion` (one question, a `preview` per option):

- **Low granularity:** the fewest issues that still keep independent outcomes apart.
- **Medium granularity:** the split you would make yourself.
- **High granularity:** the most issues where each still has its own acceptance — a vertical outcome a user can check, never a layer, phase or a test task.

Each option lists its issues (title and one-line outcome) with dependencies and epics, and says why: when this split is the right one and what it costs (review and merge overhead, waiting on dependencies, a larger diff to accept at once). Mark the one you recommend, but keep the low → medium → high order. Safeguards required for an outcome to be correct stay with it at every level (per [change boundaries](../raven-workflow/references/change-scope.md)); a granularity level never leaves a released outcome wrong until a later issue. Write previews in the user's language, with issue titles as they will be written. A business gap that would change the split is asked before this question; other gaps go to Open questions. When the task honestly allows fewer distinct splits (e.g. one indivisible outcome), show only those and say why; do not invent artificial splits to fill three. Write the issues of the chosen option; the user may adjust it in a free-text answer, and you show the adjusted split again before writing. Never create any issue before the user has chosen, even when only one split makes sense: then show it and wait for confirmation. The number of issues written always matches what the user saw and accepted.

## Write

Write every issue per the [issue template](references/issue-template.md) and run its sentence check before creating it. Before creating, check existing issues in scope to avoid duplicates (also after a timeout). New issues join the existing queue: follow its title and numbering convention, link dependencies on open and delivered issues, and state where they fall in the order. When refreshing, update only the differences, preserving people's text, assignees and statuses; show added/changed/unchanged/out-of-scope. Do not rewrite existing issues to the template on the side. Do not set In progress or close issues while building the queue. Read the issues back after writing. Without GitHub access, give the proposal in chat and name the write that was not performed.

### Dependencies on GitHub

Every dependency in an issue's Dependencies section is also set as a native GitHub "blocked by" relation, so GitHub shows the issue as blocked until the blocker is closed. Create issues in dependency order, then link each one (`gh issue` has no flag for it; use the REST API):

```bash
id=$(gh api repos/<owner>/<repo>/issues/<blocker> --jq .id)   # numeric id, not the number
gh api -X POST repos/<owner>/<repo>/issues/<blocked>/dependencies/blocked_by -F issue_id="$id"
gh api repos/<owner>/<repo>/issues/<blocked>/dependencies/blocked_by --jq '.[].number'   # read back
gh api -X DELETE repos/<owner>/<repo>/issues/<blocked>/dependencies/blocked_by/<blocker id>   # remove
```

- A relation to a delivered (closed) issue does not block, but records the order.
- On a refresh, add missing relations for the issues you write. Remove a relation only for a dependency the user agreed to drop; keep relations people set themselves, and name any that contradict the Dependencies section instead of changing them.
- Do not use the `blocked` label for dependencies: it means the issue waits for a user decision and is removed by hand.
- When the API refuses (e.g. a GitHub Enterprise Server without issue dependencies), keep the Dependencies section and name the relations not set.

### Epics on GitHub

An epic is an issue whose body follows the epic part of the [issue template](references/issue-template.md); its sub-issues are native GitHub sub-issues, never a checklist in the body. Before the first epic, check that the repo supports sub-issues (`gh api repos/<owner>/<repo>/issues/<any issue>/sub_issues` answers instead of 404); without support create no epics and name the grouping not set. Create a new epic before its issues and attach each issue right after creating it, so the epic does not stand empty:

```bash
id=$(gh api repos/<owner>/<repo>/issues/<child> --jq .id)   # numeric id, not the number
gh api -X POST repos/<owner>/<repo>/issues/<epic>/sub_issues -F sub_issue_id="$id"
gh api --paginate 'repos/<owner>/<repo>/issues/<epic>/sub_issues?per_page=100' --jq '.[].number'   # read back
```

- An issue already under another epic is moved (`-F replace_parent=true`) only when the user accepted that move in the preview.
- Do not close an epic while building the queue, even when all its sub-issues are closed; name it in the final message.
- When attaching fails anyway, stop creating epics and name the empty epic and the grouping not set.

## Final message

In chat: links to the epics and their issues, order and dependencies (with relations or sub-issues not set on GitHub, if any), open business questions, the first change ready for work, gaps. Do not create plans for all changes or start implementation.
