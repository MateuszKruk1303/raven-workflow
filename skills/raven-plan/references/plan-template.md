# Plan template

A section earns its place only when it changes what the implementer does or what a reviewer checks. Always write the core sections — TLDR, Acceptance criteria, Scope, Proposed solution, Edge cases and failures, Verification; add a conditional one (marked "only when") only when its condition holds, and never fill a section to make it look complete. The plan is a working document: do not add checkpoints, statuses, test results or change history. With an issue, do not restate its problem or business rules: link it. With an external ticket or a plain description, write out the business side the implementer needs, since nothing else holds it. Translate the headings when the plan is written in another language.

````markdown
# <id> — <outcome>

- Issue: <URL> (or Ticket: <KEY> and its link, if known; or Source: the request as given)

## TLDR
<2–3 sentences: the current behavior in the code, the observable behavior after the change, why this approach>

## Acceptance criteria
<with an issue: refer to its ACs by a short quoted phrase and add only those settled while planning; otherwise list them>
- AC1: <condition → behavior → what is visible>
- AC2: <significant error or boundary>

## Scope
<what is in; what is consciously out of scope>

## Proposed solution
<the approach in the real code: affected modules and the project primitives it reuses; each decision with a real alternative: the chosen option, the rejected ones, why, who decided>

```
<a small tree of only the files the change creates or edits, each marked (new) or (changed) with a one-line role; paths confirmed in the code or following the project's convention, never the full structure; one line when a single file changes>
```
Paths are indicative: the implementer may adjust them and reports the deviation.

## Data model
<only when the schema changes: entities, fields, relations, migration and its rollback; sensitive data and how it is protected>

## API contracts
<only when a contract used by someone else changes (public API, event, module boundary): request/response shapes, validation, compatibility>

## UI/UX
<only when the change adds UI states or flows: those unique to it — loading, empty, error, permissions; never standard CRUD>

## Edge cases and failures
<what can break — boundaries, concurrency, external calls, partial failures — and what the user sees then; one line when nothing beyond the ACs can break>

## Risks and reversibility
<only when something is hard to undo: destructive migration, changed defaults, new dependency or vendor, breaking contract; impact, rollback limits>

## Slices
<only when there are two or more slices>
1. <vertical slice: ACs it delivers; contract (types, interfaces); affected areas; depends on: — / slice N; leaves the app working>
2. <…>

## Verification
<which path in the running app to check; which flow tests to add or reuse; technical criteria such as lint, CI, migrations; risks to watch>
````
