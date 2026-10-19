---
name: raven-prd
description: "Generate context/foundation/prd.md from shape-notes.md or raw notes, following the PRD schema (greenfield 10 sections, brownfield 11). A document generator, not an author: gaps go into Open Questions. Use after raven-shape when the notes are ready (\"create the PRD\", \"write the PRD\")."
argument-hint: "[notes path]"
---

# Raven PRD

Turn the agreed notes into `context/foundation/prd.md` conforming to the [PRD schema](references/prd-schema.md). The schema is the only source of section names, their order and frontmatter keys; read it before generating. The input format is described by the [shape-notes format](../raven-shape/references/shape-notes.md). Talk to the user in their language; section headings stay as the schema defines them, the content uses the language of the notes.

The skill is a generator, not an author. It does not invent business rules, success criteria, stories, FR priorities, access control or non-goals. What is missing from the input goes into `## Open Questions`.

Skip it when the user has no notes yet (point to `raven-shape`) or wants precise edits to an existing PRD — the skill writes whole files.

## Steps

1. **Input.** The path from the argument (without a leading `@`) or by default `context/foundation/shape-notes.md`. Read the file in full. When it is missing, offer: `raven-shape` first (recommended), pasting raw notes, or cancelling.
2. **Context.** `context_type` from the notes' frontmatter. When it is missing, judge the intent and product state (README, code, history; a starter or lockfile alone does not mean brownfield) and confirm the result with the user.
3. **Assess the input.** Judge meaning, not headings: accept Polish and English sections, FRs in tables or lists, scenarios without formal Given/When/Then. Keep existing requirement IDs and sources. Map shape priorities: `pilot` → `must-have`, `later` → `nice-to-have`. The shape checkpoint helps resume work but does not prove completeness. Ask only about decisions needed to settle scope; produce a requested draft from incomplete notes without asking again.
4. **Generate in memory.**
   - Frontmatter per the schema: `status: draft` (never higher), `version: 1`, `created` from `date +%Y-%m-%d` (on overwrite keep the original `created`). A missing field: `# TODO: <field> — see Open Questions` and an Open Questions entry. No stack fields (`team_profile`, `tech_preferences`, `deployment_constraint`).
   - `##` sections exactly per the schema for the given `context_type`, in its order. No sections outside the schema (data model, implementation decisions, tests, CI/CD).
   - Content: faithfully restate the user's words, changing only the shape the schema requires. Partial content ends with a TODO; no content is a heading with a TODO. Every TODO has a numbered Open Questions entry with the consequence of the gap. Record an explicitly justified absence of a rule or change as such, not as a gap.
   - Brownfield describes the difference, not the whole system: behaviors to keep go into `## Scope of Change` as preserved, not into Non-Goals.
5. **Check before writing.** Compare headings and frontmatter keys with the schema and check the Success Criteria subsections. Review the content (except brownfield `## Current System Overview`) for implementation leakage: vendors and services, schema/ORM notation, execution location (client/server/edge), enforcement mechanism (per IP, token bucket), UI elements in NFRs, protocols, domain rules described through a component ("the database stores…"). The name of a product the user named as inspiration or a required integration is allowed with its role and source. On structural drift or leakage **do not write**: show the concrete hits and propose rephrasing as an observable property, or leaving the detail in the notes for a later stage.
6. **Write.** The current PRD is always `context/foundation/prd.md` — later skills read it. When the file already exists, ask: overwrite (recommended; Git history keeps the previous version, `version` = previous + 1) or abort. Do not create `prd-vN.md` files.

## Final message

In chat: the path, `context_type`, sections filled and marked TODO, the number of Open Questions and the technical details from the notes left outside the PRD for architecture or stack. Propose the next step based on the project's real state (usually `/raven-architecture`; in brownfield, whatever is actually missing). Do not run the next skill — a human reviews the PRD first.
