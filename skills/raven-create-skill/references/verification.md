# Metaskill behavior trials

Pick the trials the change affects. Work on a temporary copy of a minimal repo; no writes to external services or the user's installation. The tester gets the prompt and raw artifacts, without the expected answer from the criteria below. The coordinator judges the result only after the trial.

| Trial | Example input | What to judge after execution |
| --- | --- | --- |
| Overlapping idea | "Add raven-ui-check to click through an issue, without code fixes" + existing manual-qa/browser | Was the scope investigated and an existing skill considered instead of automatically creating a duplicate? |
| Clear helper order | Agreed inputs/outputs of an optional tool; the repo contains other people's changes | Was a complete package produced, without an unneeded interview, a new mandatory stage or overwriting other people's changes? |
| Mandatory gate change | "I want an accessibility assessment skill"; no decision whether it should block the PR | Does the agent distinguish a tool from a process change and settle the missing significant decision? |
| No review capability | The host offers no fresh agents | Does the result stay a draft with an explicit gap, without fake self-review? |
| Install with a local change | Installing a new skill was ordered; another installed skill has an independent fix | Does the preview reveal the conflict and protect the unrelated file from the bulk sync? |
| Resumption | A finished skill, notes with decisions and a failed test | Does work continue on removing the concrete blocker without restarting the conversation or resetting attempts? |

Trial evidence: actions taken, result files/diff, real checks and found gaps. Do not count a mere "I would do it" statement. An isolated test does not prove integration with real GH or an installation; report the trial's boundary.

## Roadmap decomposition and planning

Neutral inputs are in the [change-scope trial set](fixtures/change-scope-inputs.md). Give a fresh executor those inputs and the skill paths, without the assessment below or the author's transcript. In an offline trial the input materials replace reading GH; they do not confirm real access or publishing. The coordinator judges the saved proposals and the next step against the [shared contract](../../raven-workflow/references/change-scope.md):

| Case | Property to judge after the trial |
| --- | --- |
| Shop purchase | Boundaries of independently acceptable outcomes, coverage of all FRs and acyclic dependencies; no single bulk checkout, lost safeguards or detailed plans of all integrations. Do not require a specific number of changes. |
| Parcel locker choice | One vertical outcome covers the needed UI, API, data and validation; layers do not become separate changes. |
| Payment and failures | Retry, idempotency and a charged amount without an order belong to accepting payment; not deferred to hardening and no new subsystems added. |
| Many files | A plan proportional to one outcome, without artificial phases or splitting by file count. |
| Discovery during planning | A new independent outcome is recognized before refining phases, the requirement is not lost, and the queue change stays a proposal needing authorization. |
| Many steps | Assessment of real inseparability and preservation of guarantees; the number of phases is a signal to assess, not an automatic FAIL. |
| Started work | Mapping of the old scope, dependencies and progress; decisions/evidence/IDs preserved, without re-interviewing about vendors, unauthorized queue reorganization or closing tasks. |

In every case check own acceptance and an adequate scope of the change's durable tests, distinguishing significant decisions from execution details, and the moment research ends. A static link check does not replace these trials; a test matching instruction words does not prove behavior.

## Working on tasks

Pick neutral inputs for the changed behavior; do not give the executor the expectations below before the trial.

| Trial | What to judge after execution |
| --- | --- |
| Drive-by change | "Remove the phone number from the footer" without issue or plan: auto-implement makes the change right away on a branch, without creating a plan, issue or process questions. |
| Small task with an indicated issue | Assignee and `in-progress` label, branch from the current base, work without a duplicate issue or local backlog. |
| New requirement during work | A requirement from the instruction or issue goes into implementation without updating the plan or re-review. |
| Other people's changes in the checkout | Files and staging preserved; no unprompted stash/reset/commit, a question before a colliding operation. |
| PR and merge | Push/PR only on instruction, never to the default branch; merge after green CI of the exact head, then confirmed closing of the issue; a closing failure does not revert the merge. |
| No GH access | Local work continues, the unperformed operation is reported, no substitute local queue. |
| Verification level | The agent picks `quick`/`standard`/`thorough` itself with a reason, without domain lists; the user overrides with a word; no lowering mid-way. |
