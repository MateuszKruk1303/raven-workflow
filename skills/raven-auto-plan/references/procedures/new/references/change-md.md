# `change.md` Reference

Each `context/changes/<change-id>/change.md` is the change's lifecycle identity file. Tiny — frontmatter + an optional `## Notes` body.

## File shape

```markdown
---
change_id: <kebab-case-id> # required, must match folder name
title: <human-readable title> # required
status: <status> # required, see allowed values below
created: YYYY-MM-DD # required, set at /raven-plan time
updated: YYYY-MM-DD # required, last lifecycle skill write
Status, historyczne dowody i finalizację obsługuje kontrakt GitHub; ta procedura nie archiwizuje ani nie zamyka change.
---

## Notes

<!-- Free-form notes for this change: links, ad-hoc context, decisions that don't belong in research/frame/plan. -->
```

## Allowed `status` values

`new`, `preparing`, `planned`, `plan_reviewed`, `implementing`, `implemented`, `impl_reviewed`, `archived`, `blocked`

### Transitions

| From            | To              | Triggered by                                         |
| --------------- | --------------- | ---------------------------------------------------- |
| (none)          | `new`           | `/raven-plan`                                           |
| `new`           | `preparing`     | first of `/raven-research` or `/raven-frame`             |
| `preparing`     | `planned`       | `/raven-plan`                                          |
| `new`           | `planned`       | `/raven-plan` (when research/frame skipped)            |
| `planned`       | `plan_reviewed` | `/raven-plan-review`                                   |
| `plan_reviewed` | `implementing`  | `/raven-implement` (first phase)                       |
| `planned`       | `implementing`  | `/raven-implement` (when plan-review skipped)          |
| `implementing`  | `implemented`   | `/raven-implement` (last phase complete)               |
| `implemented`   | `impl_reviewed` | `/raven-implement-review`                                   |
| `implementing`  | `impl_reviewed` | `/raven-implement-review` (when running mid-implementation) |
| any             | `blocked`       | manual (user edit)                                   |
| `blocked`       | previous        | manual (user edit)                                   |
Status, historyczne dowody i finalizację obsługuje kontrakt GitHub; ta procedura nie archiwizuje ani nie zamyka change.
Status, historyczne dowody i finalizację obsługuje kontrakt GitHub; ta procedura nie archiwizuje ani nie zamyka change.

## Update semantics

Skills update `change.md` on every lifecycle-changing run (`status`, `updated`). The file is record-only — nothing enforces transition rules. A status alone does not prove completion: verify the corresponding artifacts and decisions in GitHub according to the workflow contract.

## What is NOT in change.md

By design:

- No `artifacts.*` block — derive from `ls` of the change folder.
- No `implementation.{total_phases,completed_phases,current_phase}` — derive from the `## Progress` section in `plan.md`.
- No `requires` / `blocked_by` — out of scope.
