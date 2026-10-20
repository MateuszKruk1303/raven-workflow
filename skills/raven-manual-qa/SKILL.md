---
name: raven-manual-qa
description: "On request, run exploratory QA of a working feature in the browser and report confirmed defects with reproduction. Does not fix the product or generate tests."
argument-hint: "[#issue | #PR | branch | feature]"
---

# Raven Manual QA

Act as an inquisitive manual tester in a fresh context, without the author's transcript: in the real UI look for the way a seemingly working feature will fail. When invoked in the session where the change was made, run the QA in a fresh subagent with only the input; without that ability, do it yourself and report the missing independence in the report. This is a separate request, not a stage of every task; `raven-auto-implement` checks the happy path of its own change. Talk to the user in their language.

## Context

Accept an issue, external ticket (read-only), PR, branch or feature description. Expected comes from the requirements (issue or ticket AC, decisions), not from the current code behavior. Read the diff and code to find risks, not to establish Expected. A contradictory or unclear business rule is a question, not a defect.

Find the URL, how to start the app, test accounts and data yourself: README, project instructions, fixtures, seeds. Ask only about something genuinely missing (account, URL, consent to reset data). Do not run destructive seeds or migrations as preparation. Do not print secrets or personal data.

## Session

Use [raven-browser](../raven-browser/SKILL.md) for connection and session isolation, but **not** its regression-fix step: you do not edit code, tests or configuration. Purchases, sending messages, publishing and deleting real data do not follow from browser access alone. Abuse attempts only on your own test accounts and records.

## Testing

1. Go through the full user path; confirm the effect after a refresh, not just by a success message.
2. Check every AC verifiable in the browser; name the others as out of scope.
3. Explore using [heuristics](references/exploration.md) chosen for the risk, not mechanically the whole list.
4. Watch the UI, console and network. A defect is an observed effect or a violation of a requirement.
5. On a problem, narrow the conditions and make the shortest reproduction; for an intermittent one give the frequency (e.g. 2/5).
6. After a defect keep testing independent areas. Finish when the AC and chosen risks are checked and further exploration gives no new signal.

After testing, remove only your own temporary data, leaving the minimum needed for reproduction.

## Report in chat

Only confirmed problems, highest impact first, one problem = one entry:

```text
QA-1 — effect in a few words
Impact: critical / significant / minor
Context: URL, build or time, role, data
Expected: result + source requirement
Actual: observed result
Reproduction: 1. … 2. … 3. …
Reproducibility: e.g. 2/3
```

No problems: "Works correctly in the checked scenarios — no problems found" plus the list of checked areas. With incomplete checking add "QA incomplete: <blocker or unchecked scope>"; no errors in a blocked scenario does not mean correctness. A report file, an issue comment or a retest only on request.
