---
name: raven-shape
description: "Refine an idea for a new product or a significant change to an existing system in a structured conversation about the problem, users and product scope. Write and resume shape-notes.md for Raven skills before the PRD. Use for shaping the vision, MVP scope, requirements and business rules; not for implementing a single bug."
---

# Raven Shape

Take the user from an idea to notes good enough to write a PRD. Result: `context/foundation/shape-notes.md`, matching the input of `/raven-prd`. Explicitly given older notes may be used as a source, without automatically carrying over history. Keep one canonical notes document.

## Start and resume

1. Read local instructions and the given description or files. Keep the original description and its source. Check existing notes, PRD and README; treat earlier documents from outside this stage as sources to read, without automatic migration or modification.
2. Recognize greenfield or brownfield from the intent and project content. A starter manifest alone does not mean an existing product. For brownfield check only the code and documents needed to understand the change; distinguish observed from declared behavior.
3. If `context/foundation/` is missing, create only the needed directory.
4. Read the whole existing `shape-notes.md` and the [notes format](references/shape-notes.md). Resume from the checkpoint; if earlier notes have no checkpoint, determine progress from their content. Keep sections, sources and decisions the new format does not define. Do not restart the interview without a reason.
5. Briefly summarize known findings and move on to the most important unknown. Establish the project name (`project`) if it is missing — the PRD does not invent it. When no idea was given and none is in the sources, ask for a short description of the user, the problem and the intended change.

## Conversation style

- Talk to the user in their language, and write the notes in it. Usually ask one concrete question or a small set of closely related questions. Do not ask about the number of rounds or about information already available.
- The topic order below is a default, not a mandatory questionnaire. One answer may close several topics. Do not require separate approval of every step.
- Format requirements based on what the user said and on sources. Mark the agent's proposals explicitly; do not present them as user decisions. No answer is an unknown, not agreement.
- After a significant answer, persist the checkpoint, decisions and open questions. Save a useful draft also on interruption or a skipped topic.

## Discovery topics

### 1. Problem, vision and users

Establish who has the problem, how they solve it today, why the current workaround is not enough and what change will bring value. Separate the target vision from the first pilot. For brownfield describe the current system, the expected difference and the behaviors that must survive.

### 2. Access and roles

Establish how users enter the product, the roles, data owners and visibility boundaries. Do not assume accounts or multiple roles are needed. In an existing system distinguish current permissions from planned changes. Ask about experience and permissions, not about choosing an auth library.

### 3. Smallest complete flow and success

Go from the user's entry to reaching value. Establish what makes the smallest useful version, which manual operations are acceptable and how to reach the first users. Record the value hypothesis and an observable signal of success or failure; do not invent thresholds or deadlines.

If the scope grows, name the concrete costly elements and propose limiting or deferring them. Relate the cost to the user's real time and budget. Do not impose a limit of weeks or steps; a consciously larger scope is a valid decision.

### 4. Requirements and scenarios

From the flow derive draft FRs with durable IDs `FR-001`, actor, capability, priority `pilot` or `later` and source. For brownfield mark `new`, `modified` or `preserved`. Do not renumber existing requirements when editing and do not reuse deleted IDs.

Record the main scenario and significant exceptions as observable criteria, e.g. Given/When/Then. Challenge costly or non-obvious assumptions: what speaks for removing the requirement, what happens on failure, why is it needed in the pilot? Record a challenged assumption and its resolution next to the FR. Do not force a separate counter-argument round for every FR.

### 5. Business rules, data and quality

Establish the real rules of decisions, validation, calculations or state transitions: input, result and exceptions. If the product is a simple record-keeping tool, check its value against the current solution; do not invent extra logic just to go beyond CRUD.

Record significant data and constraints needed to understand the rules, without designing a database schema. Establish adequate quality requirements: privacy, availability, data loss, response time or supported devices. Numeric targets need a source or marking as a proposal. For brownfield include integrations, data compatibility and regression risk; a pure infrastructure change does not need a new domain rule.

### 6. Boundaries and constraints

Record out of scope, future ideas, product type, initial scale and known time and cost constraints. Do not lead the stack choice. Keep the existing technology and voluntarily given preferences as context for later preparation, not as a new approved architecture.

## Check and hand off

Check completeness of the problem and user, flow, access, requirements, rules, success signal and exclusions; for brownfield also the behaviors to preserve. For every real gap record the name, consequence and open question. `Not applicable` with a justification is a valid result.

When a product-changing decision is missing, ask concretely. The user may finish with gaps: record `warned`, not a fictional agreement. Without gaps set `complete`; during an ongoing conversation `in_progress`. In the summary give the file, the most important unknowns and the next step `/raven-prd`. Shape alone does not run the PRD, build, tests or publishing.

Do not edit the existing PRD, roadmap, code or archives. If new findings change an earlier PRD or existing roadmap issues, describe the discrepancy in the notes and point to the update needed through `raven-prd`, `raven-roadmap` or `raven-issue-update`.
