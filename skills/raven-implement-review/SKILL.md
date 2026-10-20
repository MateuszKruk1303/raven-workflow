---
name: raven-implement-review
description: "Independent review of a change: fit with requirements, code correctness and test effectiveness. Read-only; result in chat."
argument-hint: "[branch | #PR | #issue]"
---

# Raven Implement Review

Follow [working on GitHub tasks](../raven-workflow/references/git-workflow.md). Talk to the user in their language.

The review is done by a fresh agent without the author's transcript. When invoked in the session where the change was made, run the review in a fresh subagent and give it only the input below; without that ability, do the review yourself and report the missing independence in the result. It does not edit product code or tests. Respect `context/foundation/lessons.md` if present.

## Input

The issue, external ticket or instruction, the plan (if any), the branch or PR. Establish the actual diff scope: base, head, uncommitted changes. The scope may cover the whole change or only the given tests.

## Assessment

1. **Requirements.** Every AC has coverage in code and evidence (test, check). Mark missing evidence as NOT VERIFIED.
2. **Correctness.** Rules, error paths, edge cases, races. Trace critical paths from input to effect.
3. **Architecture.** Fit with existing patterns and module boundaries.
4. **Security and data.** Permissions, input validation, data loss or overwrite.
5. **Tests.** Would they catch a regression: independent Expected (not copied from the implementation), meaningful assertions, isolation and cleanup, adequate mocks. The author's tests are evidence, not an oracle.

Run the check that settles a doubt. Do not report style or hypothetical out-of-scope problems as blockers.

## Result

In chat: scope (base..head), checks run with results, findings with severity (critical/warning/suggestion), `file:line` location, scenario and recommendation, and a verdict. A report file only at the user's request. The review is not acceptance and not consent to merge.
