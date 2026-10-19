---
name: raven-create-skill
description: Design, refine in conversation and create or change a Raven skill together with its real dependencies, routing, cookbook and validation. Use when developing the Raven family; not for implementing app features or for just asking for a skill idea.
---

# Raven Create Skill

Develop Raven as a coherent process. The result is a working change set in the skills repo: instructions, needed resources, integration and evidence of checking. Creating a new directory is not a goal in itself — extending an existing skill may solve the need better. Talk to the user in their language; write skill files in English.

The final review is done by a separate fresh reviewer, without the author's transcript. A delegated reviewer does not rerun the whole metaskill. The coordinator handles user questions.

## 1. Establish the repo and scope

Read the needed shared Raven references directly, and Claude Code's `skill-creator` skill if available. Apply its rules for writing instructions and progressive disclosure; do not copy its content into Raven. If the dependency is unavailable, name the gap and continue, but do not claim validated creation.

Find the indicated Raven source repo: it contains `skills/raven-workflow/SKILL.md`, `workflow-contract.json` and `tools/raven.py`. Check the repo instructions, Git status and the scope of existing changes. An installed copy of a skill is not evidence of the repo location. If the repo is not indicated and the cwd does not identify it, ask for the path; do not search the whole disk or create a new repo. Do not edit only a global installation. Keep other people's changes, in particular in the raven-workflow tutorial and README.

Distinguish a conversation about an idea from an order to create/change. Discussion does not trigger writes. With an order to execute, writing the skill and necessary integrations is covered by the task. Do not force the app cycle plan → implementation → tests or creating GH issues just because you develop skills.

## 2. Refine the behavior in conversation

First read the catalog and the closest existing skills. Ask about real unknowns, usually one question or a small related group. Do not re-ask findings available in the conversation. When the scope is complete, move to execution without an artificial interview.

Establish and briefly summarize:

- the user's problem and 2–3 realistic invocation examples, including a case the skill should not handle;
- inputs, sources of truth, result and observable completion conditions;
- place in the workflow: optional tool, variant of an existing stage or a new stage;
- what the agent does, which decisions belong to the user and which writes the invocation covers;
- tools and behavior with missing capabilities, interruption and resumption.

Compare a new skill with extending an existing one. Recommend a solution and explain the significant trade-off. Do not change the user's chosen goal or add a mandatory stage under the guise of integration. Changing the meaning of an existing process (e.g. a new gate, automatic writes to another service, different acceptance responsibility) needs the user's explicit decision, unless already made. Show the current and proposed behavior concretely; do not ask for consent to routine links, tests or the directory.

## 3. Check dependencies and prepare the package

Use `rg` to find invocations, links and artifact names. Read only the found producers/consumers and their shared contracts. Do not rewrite the whole Raven family. Before editing, briefly name the affected files and the reason for each integration.

- Create or change `skills/raven-<name>/SKILL.md` in English: a precise trigger, boundaries, execution and handoff. Use Claude Code frontmatter (`name`, `description`, and where it fits `argument-hint` or `disable-model-invocation: true` for manual-only skills). Add references and scripts only when they shorten instructions or give a reliable, repeated operation.
- Add the skill to the `skills` list in `workflow-contract.json`, the skill map in the raven-workflow tutorial and the right row in both README tables (the "which one to use" guide and the Catalog). Extend a recipe/diagram only when the user path changes.
- Change related skills only where inputs, outputs, responsibilities or invocations really change. Keep compatibility and existing identifiers; do not migrate historical project artifacts on the side.
- Do not add stages, gates or process evidence: the contract is only a catalog. Do not weaken the validator just to get PASS.

Keep shared rules in one place. A new skill links to [working on GitHub tasks](../raven-workflow/references/git-workflow.md), browser or independence only if it really needs them; do not duplicate whole procedures or load unrelated references.

## 4. Verify behavior and review independently

In the repo run the doctor and the tests relevant to the change, using its documented Python environment:

```bash
.venv/bin/python tools/raven.py doctor
.venv/bin/python -m unittest discover -s tests -v
```

Also use the `quick_validate.py` validator from the available `skill-creator` for new/changed skills. When `.venv` does not exist, prepare the environment per the repo README; do not install dependencies globally. Run new/changed helpers on realistic data. A missing environment is an unrun check, not PASS.

Pick trials from the [scenario reference](references/verification.md). The static doctor does not prove the meaning of instructions. For a behavior change run an isolated forward-test: the author provides real input and sources, a fresh reviewer derives the run on its own, and the coordinator compares the result with the agreed contract. Do not give the reviewer the expected answer or the bug hypothesis. Do not publish test issues, drive the private browser or run production writes as part of a trial.

The final fresh reviewer gets the user's requirements, public decisions, the current diff (including new files), the scope of changes, sources and check results. It checks producer → consumer consistency, permission boundaries, independence, resumption, duplicated rules and context cost. It works read-only and reports concrete errors and locations. Without a fresh reviewer, hand off a draft and name the missing review; do not claim full readiness.

Fix confirmed errors within the agreed scope. After a fix, refresh the affected tests and review. After two unsuccessful attempts at the same problem, stop the dependent loop with a reproduction and the decision needed from the user; switching agents does not reset the counter. Remarks that change scope go back to decision, not automatic rework.

## 5. Hand off or install

Finish with a concrete package: skill path, changed integrations, a usage example, validation/review results and limitations. Do not create an extra report in the repo unless needed for resumption. On a break, summarize decisions, files, open problems and the next step; do not restart the interview.

Install globally only when it is part of the order, also an earlier one in this session. Run `tools/raven.py sync --to <skills-dir>` without `--apply`, review the whole installation diff and only then apply `--apply`. Sync covers the whole registered family: do not overwrite unrelated local modifications the user did not include in the order. With such a conflict, hand off the ready package and agree on merging before installing. After installing run `doctor --installed <skills-dir>`; give the result and the backup path, if one was created. Copying files alone does not confirm the skill catalog refreshed in the active session.

Commit, push and PR publishing do not follow from creating a skill alone. Do them only within the order. Do not install a draft as a verified version after FAIL/BLOCKED of a required check.
