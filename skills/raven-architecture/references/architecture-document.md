# architecture.md format

Default location: `context/foundation/architecture.md`. Fit the length and headings to the product; a full picture does not mean a mandatory multi-page specification. Do not leave empty templates.

Frontmatter:
- `status`: draft or accepted;
- `revision`: the next number on a substantive change;
- `updated`: the real date;
- `accepted_revision`: the number of the explicitly accepted version, if any. Do not carry acceptance over to a changed version.

## Goal and boundaries

A short description of the product, requirement sources, constraints and what the document settles. Links to the PRD, shape, the current roadmap or the given tracker and relevant research/decisions. Do not copy the whole roadmap or task statuses.

## Current and target system

Components with responsibilities and sources of truth. A simple Mermaid diagram if it helps understanding. Mark existing elements and those only agreed. For the most important flows show the request/data path and trust boundaries.

## Cross-cutting decisions

Pick the areas for the product:
- frontend/backend split, domains, where business logic lives;
- durable data, files/media, references and metadata, retention/deletion;
- authentication, authorization, secrets and access to resources;
- integrations, APIs, webhooks, confirmation sources, retries and idempotency;
- cache, queues and background jobs, if needed;
- local/test/production environments, processes, deployment and storage;
- error detection, backup/restore, maintenance owner and costs;
- technology constraints, extensions vs own mechanisms, scaling consistent with requirements.

For data/files explain: what we store, where, who owns it, who has access, how it is created/removed and how durability is ensured. Avoid a bare "S3" or "Postgres" label. Do not write secrets or connection values.

For every significant decision give:

| Field | Content |
| --- | --- |
| ID | Stable A-001, A-002 etc.; do not renumber |
| Status | settled / proposal / to be decided / deferred / superseded |
| Decision | An unambiguous rule plus its scope and environment |
| Reason and alternatives | Why it fits the requirements; the most significant trade-off of rejected options |
| Consequences | Constraints on code, integrations and maintenance; cost without fictional estimates |
| Source | User decision and date, document/issue or code evidence |

Short subsections may be used instead of repeating tables. A fact from the code is not automatically an accepted rule for the future. A changed decision keeps its identity and points to its replacement; do not rewrite the history of approvals.

## Open points and consequences for changes

Every unsettled topic: question, impact, needed evidence/decision maker, when to settle it and a link to the affected change, if any. A conscious deferral does not block accepting the document if the user accepted its boundaries. Do not turn this into a second roadmap or execution plan.

## Sources and updates

Give the inspected HEAD/dirty state, links to documents and the dates vendor sources were checked. Do not present existing code as verified runtime without evidence. When a change plan violates an established rule, it needs an explicit resolution, and after an accepted change, an update of the document.
