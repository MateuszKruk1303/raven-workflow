---
name: raven-test
description: "Provide durable test protection for a change, bugfix or refactor: reuse existing tests, add only the missing ones, and before a risky change lock in current behavior (before-change)."
argument-hint: "[change | before-change <module> | reproduce <bug>]"
---

# Raven Test

Follow [working on GitHub tasks](../raven-workflow/references/git-workflow.md) and [execution discipline](references/implementation-discipline.md). Respect `context/foundation/lessons.md` if present. Talk to the user in their language.

The only skill for durable tests. On request: closing regression gaps after a change, a separate testing task, or protection before a change. `raven-auto-implement` adds the tests its own change needs; this skill is for additional or separate needs.

## Steps

1. **Map.** For every AC (from the issue, ticket, plan or instruction) and significant risk, establish which existing test protects it and with which assertion. No such test is a named gap. Derive Expected from the requirements, not from implementation output.
2. **Gaps.** Add tests only for named gaps. Good existing protection stays unchanged and without duplicates. The cheapest effective layer: unit for logic, integration for DB/service/API boundaries, E2E for a real flow in the UI. Do not add a framework or layers in advance.
3. **E2E.** When needed, read only what is needed: [Playwright setup](references/procedures/e2e-setup/procedure.md) and [writing tests](references/procedures/e2e/procedure.md). For new behavior driven by tests: [TDD](references/procedures/tdd/procedure.md).
4. **Effectiveness.** Every new test must be able to fail: independent Expected, a meaningful assertion of the effect, isolation and cleanup, mocks only at external boundaries. When unsure, make a controlled perturbation of the code and always revert it. Do not weaken assertions for a green result.
5. **Run.** New and changed tests plus dependent regressions. The full suite only for a concrete reason.

## Before-change

Before an unprotected refactor: a characterization test locks in deliberately protected behavior, not an accidental bug. For a bugfix, a test on the old code may end in `EXPECTED_RED`: give the assertion, the observed failure and the source of the expectation. A runner or environment error does not prove reproduction.

## Product defect

Fix a detected defect within the requested scope proportionately and give current acceptance instructions in chat. Report an out-of-scope defect without fixing it.

## Final message

In chat: AC → test map, closed and open gaps, commands run with results. **Finishing without new tests is correct** when the map shows sufficient protection. Commit tests in logical steps. Do not publish a PR from a testing request alone.
