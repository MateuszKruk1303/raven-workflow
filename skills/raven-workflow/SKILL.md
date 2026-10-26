---
name: raven-workflow
description: "Manually invoked Raven tutorial: explain the GitHub-task work model, the skill map and the fitting next step for the work at hand. Not a router or a mandatory stage."
disable-model-invocation: true
---

# Raven Workflow

Run only on explicit request, as a tutorial and hint. The tutorial is read-only: do not take up an issue and do not run other skills. Talk to the user in their language.

## Work model

Work happens on tasks in GitHub Issues — details in [working on GitHub tasks](references/git-workflow.md). The issue carries business requirements, the plan is optional one-off agent context, and the state of work is the issue, branch, commits and PR. The boundaries of one change are described in [change boundaries](references/change-scope.md).

When asked about the state of some work, read the issue (state, assignee), branch, commits and PR (for ticket work, the branch and PR found by its key), explain where the work stands and suggest the fitting skill.

## Typical path

- **Small change:** [raven-auto-implement](../raven-auto-implement/SKILL.md) with just the instruction.
- **Task:** issue → optionally [raven-plan](../raven-plan/SKILL.md) → [raven-auto-implement](../raven-auto-implement/SKILL.md) → manual acceptance following the chat instructions, plus fixes if needed → [raven-pr](../raven-pr/SKILL.md) → [raven-merge](../raven-merge/SKILL.md).
- **Ticket from Jira or another tracker:** [raven-auto-implement](../raven-auto-implement/SKILL.md) with the ticket link (optionally [raven-plan](../raven-plan/SKILL.md) with it first) → acceptance → [raven-pr](../raven-pr/SKILL.md) → [raven-merge](../raven-merge/SKILL.md). The ticket is read-only; no GitHub issue.
- **On request or when risky:** [raven-implement-review](../raven-implement-review/SKILL.md) (requirements, code, tests), [raven-test](../raven-test/SKILL.md) (durable tests, before-change), [raven-manual-qa](../raven-manual-qa/SKILL.md) (exploratory QA).

`raven-auto-implement` matches verification to risk (`quick`/`standard`/`thorough`) and does not run further skills.

## Project setup

**Greenfield:** [shape](../raven-shape/SKILL.md) → [PRD](../raven-prd/SKILL.md) → [architecture](../raven-architecture/SKILL.md) → [stack](../raven-init-stack/SKILL.md) or [Medusa](../raven-medusa-ecommerce-init/SKILL.md) → [AGENTS.md + CLAUDE.md](../raven-md/SKILL.md), [CI](../raven-hooks/SKILL.md), [GitHub](../raven-github-setup/SKILL.md) → [roadmap](../raven-roadmap/SKILL.md).

**Brownfield:** as needed [repo map](../raven-repo-map/SKILL.md), [research](../raven-research/SKILL.md) or [architecture](../raven-architecture/SKILL.md). A small known task needs none of them. Jira or a plain task description as the requirements source: [raven-roadmap](../raven-roadmap/SKILL.md).

## Tools

[raven-issue-update](../raven-issue-update/SKILL.md) adds a requirement to an existing issue. [raven-browser](../raven-browser/SKILL.md) drives the browser for other skills. [raven-lesson](../raven-lesson/SKILL.md) records a recurring rule on request. [raven-create-skill](../raven-create-skill/SKILL.md) extends Raven.
