# shape-notes.md format

Target file: `context/foundation/shape-notes.md`. For a new document use the frontmatter below. Dates use ISO format; unknown values stay `null`.

```yaml
---
workflow: raven
project: null
context_type: greenfield
created: YYYY-MM-DD
updated: YYYY-MM-DD
checkpoint:
  status: in_progress
  current_topic: problem
  topics_completed: []
  frs_drafted: 0
  next_question: null
---
```

- `project`: the project name the user gave; `/raven-prd` copies it into the PRD.
- `context_type`: `greenfield` or `brownfield`; `null` while the context is unsettled.
- `status`: `in_progress`, `complete` (topics settled or justified as irrelevant), `warned` (finished with explicit gaps at the user's request).
- Checkpoint topics: `problem`, `access`, `flow`, `requirements`, `rules`, `scope`, `cross_check`; on completion `current_topic: null`.
- `frs_drafted` counts active FRs; it does not determine the next ID number.

Organize the content into sections (translate the headings when the notes are in another language):

1. Sources and original idea — the user's description, links, origin of adopted findings.
2. Current system — brownfield only: current behavior, planned difference, state confirmed in sources.
3. Vision, problem and users — the workaround for the problem and the product's value.
4. Access and roles — data and permission boundaries, or a conscious absence of accounts.
5. Hypothesis and validation — reaching users, the result signal, the threshold or the unknown.
6. Pilot scope and flows — the full path to value, scenarios and exceptions.
7. Functional requirements — durable ID, priority (`pilot`/`later`), source, criteria and optional change category.
8. Business rules and data — rules, constraints, exceptions.
9. Quality requirements and behavior to preserve — observable guarantees.
10. Out of scope and accepted simplifications — including manual operations and the later vision.
11. Constraints and technical context — time, costs, scale, existing stack and preferences for a later stage.
12. Decisions, assumptions and open questions — distinguish a user decision, evidence from a source and an agent proposal.
13. Completeness check — concrete gaps and consequences, the next step when resuming.

Do not fill sections with invented content. Mark unknown information as unsettled. Keep extra sections of existing Raven notes and their findings; the format does not require rewriting the document just to match headings. These are input notes for the PRD, not a finished PRD or implementation plan.
