# `## Progress` Section Reference

The `## Progress` section in `plan.md` defines the execution state rendered from GitHub task progress. This document defines the shared format used by Raven planning, implementation, testing, and review.

## Where it lives

At the bottom of `context/changes/<change-id>/plan.md`, after `## References`. Exactly one `## Progress` heading per plan.

## Structure

```markdown
## Progress

> Convention: `- [ ]` pending, `- [x]` done. Append ` — <commit sha>` when a step lands. Do not rename step titles.

### Phase 1: <phase name>

#### Automated

- [ ] 1.1 <step title>
- [x] 1.2 <step title> — abc1234

#### Manual

- [ ] 1.3 <step title>

### Phase 2: <phase name>

#### Automated

- [ ] 2.1 <step title>
```

## Rules

- **One `## Progress` heading**, at the bottom of the file (after `## References`).
- **One `### Phase N: <name>`** per phase, in order, matching the descriptive `## Phase N:` or `## Faza N:` headers earlier in the plan **by phase number**. The descriptive heading language is not a consistency defect; keep Polish `Faza` headings. Progress retains its canonical `### Phase N:` headings.
- **Per-phase Automated/Manual subdivision**:
  - `#### Automated` lists steps verifiable without human action (commands, tests, type checks).
  - `#### Manual` lists steps that require a human to look at the result (UI, smoke tests, eyeball checks).
  - A phase may have only `#### Automated`, only `#### Manual`, or both. Omit empty subsections.
- **Step format**: `- [ ] <phase>.<index> <title>` (pending) or `- [x] <phase>.<index> <title> — <sha>` (done).
- **Step indices** are 1-based and unique within their phase. They are assigned at planning time and **never renumbered**. New steps added later get the next available index; deleted steps leave gaps (acceptable).
- **Step titles are immutable** once the plan is reviewed. If a step's intent changes, leave the title and add a brief inline note in the relevant Phase block above — do not rewrite the Progress entry.
- **Commit SHA suffix** is appended to a step when the work lands (` — <sha>`). The SHA is the short form (7+ chars) of the commit that closed the step. Multiple commits per step → list the closing commit only.

## Mutation surface

- Implementation and test execution update `[ ]` → `[x]` per completed step and append the closing commit SHA at phase end. Manual and auto modes use the same format. Mid-phase, completed rows may have `[x]` without a SHA suffix. Manual checks remain pending until confirmed by the user.
- Review reads Progress as evidence; it does not mark execution steps complete.
- `/raven-plan` writes the Progress section once at planning time, with all steps as `[ ]` and no SHA suffixes.

## Parsing contract for tooling

Skills that need to derive state from Progress:

- **Next pending step** = first `- [ ]` line in document order.
- **Completion** = `count([x]) / count([ ] + [x])`.
- **Current phase** = phase containing the first `- [ ]`, or last phase if all done.
- **Drift detection**:
  - If `change.md.status = implementing` but Progress has 0 `[x]` → warn (no progress recorded).
  - If `change.md.status = implementing` but all items are `[x]` → warn (status should be `implemented`).
  - If `change.md.status = planned` but Progress has any `[x]` → warn (status should be `implementing`).

## What is NOT in Progress

- **No state file sidecar**: Progress is the single source of execution state — no JSON cache anywhere.
- **No `<!-- PLAN STATUS -->` / `<!-- PLAN COMPLETED -->` markers**: removed. Status lives in `change.md` frontmatter, completion is derived from Progress.
- **No nested checkboxes**: a step is one bullet. Sub-tasks belong in the Phase block as Success Criteria, not as Progress sub-items.
- **No estimates, owners, due dates**: scope creep. Add them via PR description if needed; not here.
- **No descriptive prose between phases or subsections**: the Progress section is parsed by tooling. Keep it strictly headings + bullets.
