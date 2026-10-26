# Raven Workflow

[Working model](#working-model) · [Greenfield](#greenfield) · [Brownfield](#brownfield) · [Work patterns](#work-patterns) · [Which skill to use](#raven-skills--which-one-to-use-and-when) · [Catalog](#skill-catalog)

Raven skills for Claude Code. You invoke them directly with `/raven-<name>`; write in any language and the agent answers in it. `raven-workflow` is an optional tutorial, invoked manually only.

## Working model

We work on tasks in GitHub Issues, without extra process machinery.

- **Issue** carries the business requirements and acceptance criteria. Jira, if used, stays the requirements source; the issue only links it, or `/raven-plan` and `/raven-auto-implement` with a ticket URL work straight from the ticket.
- **Plan** (`context/changes/<id>/plan.md`) is an optional, one-off working context for the agent. It is not a contract: no fingerprint, checkpoints or statuses. A new requirement goes into the issue or the instruction.
- **Work state** is the issue, branch, commits and PR.
- **Small change** (removing a button, changing a phone number) needs no issue or plan: `/raven-auto-implement` with just the instruction.
- **Push, PR and merge** only on explicit instruction.
- **Results and acceptance instructions** go to the chat, not to reports. The PR gets a short "Verification" section: what was actually checked and what was not.
- **Project instructions**: `AGENTS.md` holds the shared content and `CLAUDE.md` imports it with `@AGENTS.md`, so both formats work.

Rules: [working on GitHub tasks](skills/raven-workflow/references/git-workflow.md), [change scope](skills/raven-workflow/references/change-scope.md).

## Greenfield

A new product from idea to the first task. Each step writes one document the next one uses.

```text
raven-shape          messy idea, notes, conversations → structured problem, audience, MVP, rules
│                    context/foundation/shape-notes.md
▼
raven-prd            requirements and acceptance criteria
│                    context/foundation/prd.md
▼
raven-architecture   cross-cutting decisions: data, integrations, auth, module boundaries
│                    context/foundation/architecture.md
▼
raven-init-stack     Better T Stack skeleton + local Postgres
OR raven-medusa-ecommerce-init   Medusa + Next.js shop
▼
raven-md             AGENTS.md + CLAUDE.md from the real commands and conventions
raven-github-setup   repo, Issues, in-progress/blocked labels
raven-hooks          CI: lint, typecheck, tests after a PR
▼
raven-roadmap        PRD → issues: outcomes, AC, dependencies, order
▼
first issue → the "Task from an issue" pattern
```

## Brownfield

An existing project. Pick only what is missing; a small known task needs none of these.

```text
Unknown code?                       raven-repo-map            map of areas, dependencies, history, risks
Concrete question about the code?   raven-research            answer with path:line evidence
Cross-cutting decision?             raven-architecture        architecture.md
No AGENTS.md / CI / labels?         raven-md · raven-hooks · raven-github-setup
Weak AGENTS.md or CLAUDE.md?        raven-md (review mode)    scorecard, no rewriting
Queue from a PRD or Jira?           raven-roadmap             issues linking the source
Refactor without tests?             raven-test (before-change) before the change
▼
a work pattern below
```

## Work patterns

### Drive-by change

A small thing without issue or plan: copy, style, removing an element, config.

```text
/raven-auto-implement remove the phone number from the footer
```

The agent usually picks `quick`, commits on a short branch (never on the default one) and tells you in chat how to check the result. Push, PR and merge are separate requests, if you want them.

### Task from an issue

A typical feature or fix.

```text
/raven-plan #42              (optional) plan in the real code; plan review on request
/raven-auto-implement #42    implementation + verification (standard by default)
  ↳ manual acceptance following the chat instructions
  ↳ problem? /raven-auto-implement #42 — <what does not work>
/raven-pr #42                push + PR with Closes #42
/raven-merge #42             green CI → merge → issue closed
```

Skip the plan when the issue and instruction are enough. A new requirement during work goes into the instruction or through `/raven-issue-update`; the plan is not updated.

### Risky change

When a mistake would be costly, hard to reverse or hard to notice before the user does.

```text
/raven-plan #57 — with review     a fresh agent assesses the plan, one round of fixes
/raven-auto-implement #57         the agent picks thorough itself, or you say "thorough"
/raven-implement-review #57       (optional) independent review of the whole change before the PR
/raven-pr → /raven-merge
```

`thorough` adds tests of the whole area (a baseline only when one fails for an unclear reason), an end-to-end path with a failure scenario and one independent review.

### Bugfix

```text
/raven-test reproduce <bug description>    (optional) EXPECTED_RED test on the current code
/raven-auto-implement fix <bug>            the fix; the test goes green
```

For a simple bug `/raven-auto-implement` alone is enough: if a test for the fixed behavior is missing, it adds one.

### Refactor

```text
/raven-test before-change <module>         characterization tests of the current behavior
/raven-auto-implement refactor <module>    the change with tests green
```

### Quality checks on request

```text
/raven-implement-review <branch/PR>   requirements, correctness, security, test effectiveness
/raven-test <change>                  AC → test map, only the missing tests
/raven-manual-qa <issue/PR>           exploration in the browser, defects with reproduction
```

None of them runs automatically and none is a precondition for a PR.

### Jira in a team

```text
/raven-roadmap PROJ-120..PROJ-128   GH issues linking the tickets, no copying and no writes to Jira
```

Then the "Task from an issue" pattern. Requirements stay in Jira, execution is tracked in GitHub.

Or straight from one ticket, without a GH issue:

```text
/raven-plan https://acme.atlassian.net/browse/PP-1234             (optional) plan from the ticket, with questions
/raven-auto-implement https://acme.atlassian.net/browse/PP-1234   reads the ticket (and plan), branch feat/PP-1234, verification
/raven-pr                                                         PR linking PP-1234
/raven-merge                                                      green CI → merge; the ticket is not touched
```

The agent reads the ticket through an available connector or CLI (or asks you to paste it) and never writes to Jira.

## Raven skills — which one to use and when

Install in a project: `npx skills add MateuszKruk1303/raven-workflow`, update: `npx skills update -p -y`.

The skills are in the order they usually appear in work. No stage is mandatory — a small change needs only `/raven-auto-implement`.

| Stage | When you reach for it | Skill | What you get |
| --- | --- | --- | --- |
| **0. I'm lost** | _"I don't know where I am or what's next."_ | [`raven-workflow`](skills/raven-workflow/SKILL.md) | The work stage from the issue, branch, commits and PR, and the next skill. Changes nothing. |
| **1. I have an idea** | _"I have an idea, but it's still vague."_ | [`raven-shape`](skills/raven-shape/SKILL.md) | Problem, audience, MVP and rules in `shape-notes.md`. The conversation can be resumed. |
| | _"I know what I want — make it a proper document."_ | [`raven-prd`](skills/raven-prd/SKILL.md) | `context/foundation/prd.md`: requirements, scope, exclusions. |
| **2. Laying foundations** | _"I want to make the big decisions consciously."_ | [`raven-architecture`](skills/raven-architecture/SKILL.md) | Options with trade-offs and a recommendation in `context/foundation/architecture.md`. |
| | _"I want a working skeleton without manual gluing."_ | [`raven-init-stack`](skills/raven-init-stack/SKILL.md) | Better T Stack + local Postgres; decisions in `tech-stack.md`. |
| | _"I'm building a Medusa shop and it has to run locally."_ | [`raven-medusa-ecommerce-init`](skills/raven-medusa-ecommerce-init/SKILL.md) | Medusa + Next.js monorepo: migrations, seed, admin, storefront. |
| | _"The agent gets lost in the repo or breaks conventions."_ | [`raven-md`](skills/raven-md/SKILL.md) | `AGENTS.md` + `CLAUDE.md` from repo facts, or a scorecard (review mode). |
| | _"I don't want to remember lint and tests before merge."_ | [`raven-hooks`](skills/raven-hooks/SKILL.md) | GitHub Actions: lint, typecheck, tests after a PR. |
| | _"I want to work on tasks in GitHub."_ | [`raven-github-setup`](skills/raven-github-setup/SKILL.md) | Remote, Issues, `in-progress`/`blocked` labels; a Project on request. |
| **3. Building the queue** | _"I have a PRD and don't know where to start."_ | [`raven-roadmap`](skills/raven-roadmap/SKILL.md) | Small changes as GitHub Issues in order; source: PRD or Jira. |
| | _"I remembered one more requirement."_ | [`raven-issue-update`](skills/raven-issue-update/SKILL.md) | The requirement woven into the body and AC of an existing issue. |
| **4. Entering unknown code** | _"I got someone else's repo and don't know what's where."_ | [`raven-repo-map`](skills/raven-repo-map/SKILL.md) | Areas, dependencies, history, risks — a report with evidence. |
| | _"I need to know how this really works."_ | [`raven-research`](skills/raven-research/SKILL.md) | An answer with evidence, options and gaps in `context/changes/<id>/research.md`. |
| **5. Doing a change** | _"The task is risky, the agent can't guess."_ | [`raven-plan`](skills/raven-plan/SKILL.md) | A plan of one change in the real code; plan review on request. |
| | _"Just do it — and prove it works."_ / _"Here's the Jira link, go."_ | [`raven-auto-implement`](skills/raven-auto-implement/SKILL.md) | Instruction, issue or ticket link; commits, `quick`/`standard`/`thorough` verification, acceptance instructions in chat. |
| | _"I want to see it in the browser."_ | [`raven-browser`](skills/raven-browser/SKILL.md) | An isolated Playwright session for other skills; Brave only on instruction. |
| | _"Let someone try to break it."_ | [`raven-manual-qa`](skills/raven-manual-qa/SKILL.md) | Exploration in the UI, defects with reproduction in chat. Fixes nothing. |
| | _"I want a second pair of eyes on this code."_ | [`raven-implement-review`](skills/raven-implement-review/SKILL.md) | Read-only review: requirements, correctness, test effectiveness. |
| | _"I don't want this to break silently."_ | [`raven-test`](skills/raven-test/SKILL.md) | Only the missing tests; before-change before a refactor. |
| **6. Handing off** | _"I'm happy — shipping it."_ | [`raven-pr`](skills/raven-pr/SKILL.md) | Push and a PR linked to the issue or ticket, with a "Verification" section; no merge. |
| | _"CI is green, I accept — let's close."_ | [`raven-merge`](skills/raven-merge/SKILL.md) | Merge after green CI and your consent, issue (if any) closed. |
| **7. Learning from mistakes** | _"The same mistake again."_ | [`raven-lesson`](skills/raven-lesson/SKILL.md) | One rule in `context/foundation/lessons.md`, read by later skills. |
| | _"I'm missing a tool in Raven."_ | [`raven-create-skill`](skills/raven-create-skill/SKILL.md) | A new or changed Raven skill with validation. |

## Skill catalog

| Skill | What it does | Tests | Result |
| --- | --- | --- | --- |
| [raven-architecture](skills/raven-architecture/SKILL.md) | Cross-cutting architecture decisions based on the PRD and code. | Does not write; accounts for testability. | `context/foundation/architecture.md` |
| [raven-auto-implement](skills/raven-auto-implement/SKILL.md) | Carries out an instruction, optionally with an issue, plan or Jira/other ticket link (read-only); a leading agent with optional parallel implementers; a recording on `--recording`. | **Yes:** once at the end, after the feature works; adds flow tests for gaps; `quick`/`standard`/`thorough`. | Commits (no push/PR) and a summary in chat |
| [raven-browser](skills/raven-browser/SKILL.md) | Drives the browser (by default a separate Playwright CLI session) for other skills. | Ad hoc scenarios; does not replace durable E2E. | Observations, screenshots, logs |
| [raven-create-skill](skills/raven-create-skill/SKILL.md) | Designs and changes Raven skills with an independent review. | Doctor, repo tests, behavior forward-test. | Skill package in this repo |
| [raven-github-setup](skills/raven-github-setup/SKILL.md) | Repo, enabled Issues, in-progress/blocked labels; a Project on request. | Not applicable. | GitHub configuration |
| [raven-hooks](skills/raven-hooks/SKILL.md) | GitHub Actions: lint, typecheck and the right tests after a PR. | Runs them in CI; does not write product tests. | CI workflow files |
| [raven-implement-review](skills/raven-implement-review/SKILL.md) | Fresh reviewer: requirements, correctness, architecture, security, test effectiveness. | Assesses; does not fix. | Remarks and verdict in chat |
| [raven-init-stack](skills/raven-init-stack/SKILL.md) | Better T Stack, local Postgres, env. | Checks setup and types. | App skeleton, `tech-stack.md` |
| [raven-issue-update](skills/raven-issue-update/SKILL.md) | Weaves a requirement into the scope and AC of an existing issue. | Not applicable; write readback. | Updated issue body |
| [raven-lesson](skills/raven-lesson/SKILL.md) | Records a recurring project rule on request. | Does not write. | `context/foundation/lessons.md` |
| [raven-manual-qa](skills/raven-manual-qa/SKILL.md) | Exploratory QA of a running feature in the browser. | Does not write or fix. | Defects with reproduction in chat |
| [raven-md](skills/raven-md/SKILL.md) | Creates, updates or assesses AGENTS.md and CLAUDE.md based on repo facts. | Does not write. | `AGENTS.md` + `CLAUDE.md`, or a scorecard |
| [raven-medusa-ecommerce-init](skills/raven-medusa-ecommerce-init/SKILL.md) | Local Medusa + Next.js starter: database, Redis, migrations, seed, admin, storefront. | Checks startup and the basic purchase flow. | Working local monorepo |
| [raven-merge](skills/raven-merge/SKILL.md) | Merge after green CI of the exact head, then closing the GitHub issue (if any). | Reads the CI result. | Merged PR, closed issue (if any) |
| [raven-plan](skills/raven-plan/SKILL.md) | Plan of one outcome in the real code, from an issue or Jira/other ticket; optional plan review by a fresh agent. | Plans; does not write. | `context/changes/<id>/plan.md` |
| [raven-pr](skills/raven-pr/SKILL.md) | Push and create or update the PR linked to the issue or ticket, with a "Verification" section. | Does not run; describes the checks actually done. | PR |
| [raven-prd](skills/raven-prd/SKILL.md) | PRD from shape notes or raw findings. | Does not write; defines behaviors to verify. | `context/foundation/prd.md` |
| [raven-repo-map](skills/raven-repo-map/SKILL.md) | Map of an existing repo: areas, dependencies, history, risks. | Does not write. | `context/foundation/repo-map.md` |
| [raven-research](skills/raven-research/SKILL.md) | Answers to concrete questions about the code or feasibility, with evidence. | Runs them only when that answers the question. | `research.md` |
| [raven-roadmap](skills/raven-roadmap/SKILL.md) | Queue of changes as GitHub Issues, from a PRD or Jira. | Does not write. | Issues with AC and dependencies |
| [raven-shape](skills/raven-shape/SKILL.md) | Conversation structuring a messy idea: problem, audience, MVP, rules. | Does not write. | `context/foundation/shape-notes.md` |
| [raven-test](skills/raven-test/SKILL.md) | Durable test protection: AC → test map, only the missing tests, before-change. | **Yes:** only for named gaps. | Tests in the repo, map in chat |
| [raven-workflow](skills/raven-workflow/SKILL.md) | Manual tutorial: working model and skill map. | Not applicable. | Explanation in the conversation |

<details>
<summary>Installation and maintenance</summary>

The repo is the distribution source. Python 3.10+:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python tools/raven.py doctor
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/python tools/raven.py sync --to <skills-dir>          # preview
.venv/bin/python tools/raven.py sync --to <skills-dir> --apply  # write with backup
.venv/bin/python tools/raven.py doctor --installed <skills-dir>
```

Sync covers only the Raven family. It backs up the affected directories, removes stale files and retired skills. Review the preview, because sync overwrites local modifications of Raven skills.

Doctor checks frontmatter, names, local links and the [catalog](workflow-contract.json): every skill registered and described in the README, and a retired one does not come back — neither as a directory nor as a mention or artifact in skill content (list in `tools/raven.py`). The catalog has no stages, gates, roles or models. A static PASS does not prove agent behavior; check instruction changes with trials on real inputs. [Raven integrity](.github/workflows/integrity.yml) runs these checks in CI.

</details>
