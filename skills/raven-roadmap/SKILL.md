---
name: raven-roadmap
description: "Create or refresh a queue of self-contained changes as GitHub Issues, sourced from the PRD, from given Jira tickets, sprint or epic, or from a task description the user asks to turn into issues (no PRD needed). Places new issues among existing ones with dependencies and order. No implementation plans and no writes to Jira."
argument-hint: "[prd path | Jira keys | task description]"
---

# Raven Roadmap

Follow [working on GitHub tasks](../raven-workflow/references/git-workflow.md) and [change boundaries](../raven-workflow/references/change-scope.md). Talk to the user in their language; write issues in the language the repository uses, or the user's language for a new repository.

The roadmap is GitHub Issues in the established repo: one issue = one independently acceptable outcome. A roadmap request covers writing those issues. A Project is an optional view. Do not create a local roadmap or a second backlog. An addition to one existing issue is [raven-issue-update](../raven-issue-update/SKILL.md), not a queue reorganization.

## Source

- **PRD** (`context/foundation/prd.md` or a given document): cover the whole agreed PRD — every requirement has its change, evidence of earlier delivery or an explicit deferral.
- **Jira** (keys, URL, sprint, epic): fetch descriptions, AC and relations only for that scope. An epic or sprint is a container, not a change; one ticket can be a change, a too-wide one gets split. The GH issue links the ticket (with ID and update date), without copying content or status. Never write to Jira. A Jira Done status does not prove a merge.
- **Task description** (text in the prompt): the user's description is the requirement; no PRD or Jira is needed. Cover only what it asks for, one issue or a split when it is too wide. Fill in outcome, scope and AC from the description and the code; ask only about gaps that change the scope or the AC, and record the rest as assumptions in the issue. Read the PRD when it exists only to check the task does not contradict it.

## Split

Split into vertical outcomes (UI, API, data and validation together), not layers or phases. Every issue: outcome, scope and exclusions, link to the source, observable AC, dependencies. The dependency graph is acyclic. Briefly justify a larger inseparable scope. Do an ordinary split of the agreed scope yourself; changing requirements or priorities needs the user's decision.

## Write

Before creating, check existing issues in scope to avoid duplicates (also after a timeout). New issues join the existing queue: follow its title and numbering convention, link dependencies on open and delivered issues, and state where they fall in the order. When refreshing, update only the differences, preserving people's text, assignees and statuses; show added/changed/unchanged/out-of-scope. Do not set In progress or close issues while building the queue. Read the issues back after writing. Without GitHub access, give the proposal in chat and name the write that was not performed.

## Final message

In chat: links to the issues, order and dependencies, the first change ready for work, gaps. Do not create plans for all changes or start implementation.
