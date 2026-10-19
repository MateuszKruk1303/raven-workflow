---
name: raven-architecture
description: "Interactively settle cross-cutting architecture decisions and create or update context/foundation/architecture.md from the PRD, documentation, code and roadmap. Guides through options, recommendations and trade-offs; does not replace the plan of a single change."
---

# Raven Architecture

Build with the user an understandable picture of the whole product's architecture: responsibilities of system parts, flows, where data is stored, integration boundaries and operational rules. The result is `context/foundation/architecture.md`, not an implementation, a list of libraries or a roadmap. Talk to the user in their language; write the document in the user's language unless the project already uses another.

## Scope and permissions

The invocation authorizes reading sources and writing the document together with a short link in the relevant existing AGENTS.md (or CLAUDE.md when the project has no AGENTS.md). Do not change the PRD, code, service configuration, issues, Project statuses, other agent instructions or global preferences on the side. Do not commit, push, deploy or run the next skill without a separate request. Treat a foreign repo or one restricted by instructions according to where writing is allowed; do not install your own workflow there on your own.

Requirements and explicit user decisions are constraints, not suggestions to replace. Architecture describes facts and the agreed direction; it does not grant proposals the status of decisions. An existing stack is not an invitation to replace it. Do not introduce services, microservices, queues, caches, multi-tenancy or infrastructure for unagreed future needs.

## 1. Rebuild sources and the decision map

Distinguish a first draft, a resumed conversation and an update of a specific part. Read the existing architecture.md before writing anything. Keep untouched decisions, their IDs, justifications and sources.

Go through the repo's documentation inventory: instructions, README, the full current PRD/shape, stack/infrastructure documents, ADRs, security, testing, integration docs and lessons. Read all materials relevant to architecture; show missing sources and contradictions. Do not treat an archive as a current requirement. Do not read secrets or generated directories to fill in documentation.

Read the roadmap in GitHub Issues, only the needed changes/dependencies and local plans/research/decisions. Do not read the whole GH history and do not create a second queue. Name a source you cannot access while continuing with independent findings. Do not run setup on the side. A missing PRD in brownfield does not block the work if the goal and scope follow from other reliable materials; agree on genuinely missing requirements.

Check the areas of code and configuration relevant to decisions. Load available domain skills when analyzing their technology. Distinguish "exists and verified", "declared in documentation", "target, agreed" and "proposal". Writing "S3" in a document does not prove S3 is deployed.

Show a short starting point and the list of discussion areas that follow from the product. Separate already settled decisions from questions; do not ask the user about facts available in the repo or again about an accepted choice. Present a contradiction with the code as a current/target difference, not a reason to silently change a decision.

## 2. Lead the conversation from general to specific

Start with system boundaries, main flows and responsibilities. Then move to data, files, communication, integrations and maintenance. Adapt the order to decision dependencies and risk. The user does not need to know technology names.

Usually ask 1–3 related questions per round, with the `AskUserQuestion` tool or in chat. Every question should contain:
- the need that follows from a specific requirement or flow;
- 2–3 genuinely sensible options, including keeping the current solution if it meets the need;
- a recommendation with a justification for this project;
- benefits, costs/operational responsibility, limitations and significant consequences of each option;
- what the decision unblocks and what can be settled later.

Do not create fake alternatives just for the number of options. With one feasible option, explain the constraint and agree on the direction. Do not hide vendor costs or maintenance work. Verify prices, limits, compliance and service capabilities in current official sources before recommending. Also verify uncertain technical claims. Without access to sources, mark them as unverified instead of promising they work.

Wait for answers before settling dependent choices. No answer is not consent. After a round, briefly summarize decisions, their consequences and remaining areas. If a new answer changes an earlier choice, show the impact and agree only on the conflicting elements. Do not impose a number of questions or end the conversation after an arbitrary limit.

Example question type: "Where should user and product images go? Files are currently local. For the planned hosting I recommend object storage, because files must survive instance replacement. The alternative is a durable disk with its own backup. In both variants we need to define which references and metadata the database stores and how access works." This is an example of reasoning, not a universal ban on storing binaries in the database or an imposed vendor.

## 3. Build one document during the conversation

Read the [document format](references/architecture-document.md). Record agreed decisions and questions in the same architecture.md, marking it as a draft. Writing the draft needs no extra approval; it does not, however, mean accepting proposals. Do not create a separate conversation register or local change status next to it. When resuming, return to unsettled points without repeating the whole interview.

Every decision has a stable ID, status, source, justification and consequences for implementation. For a "later" decision, record a conscious deferral, the condition for returning to it and the affected changes. Deferring a vendor choice may be correct if the storage, access and durability contract is already defined. Do not defer on the user's behalf a decision needed to understand the architecture.

Write rules concretely enough for an agent to know where to put a responsibility, data or integration. Do not design every table, endpoint, function or execution phase; that is the scope of planning a change. If research blocks a choice, name the precise question and propose `/raven-research` for the right change; do not run it automatically and do not invent a result.

## 4. Complete the picture and hand off

Check coverage of all significant requirements and changes: every cross-cutting area has a decision, an explicit "not applicable" with a reason, or an agreed deferral. In particular check that the diagram matches the tables, responsibility boundaries, data in the database vs files, local/production differences, access and durability, and the effects of integration failures. A feature absent from the product needs no architecture chapter.

Show the user the full concise picture: components and flows, key decisions with reasons, current/target differences, costs and open points. Ask for acceptance of this specific document, unless the current version was already explicitly accepted. Set `accepted` only for the approved version and agreed deferrals. With an unsettled fundamental decision keep `draft`, name exactly what is missing and continue the conversation. Acceptance is not permission to implement or buy services.

Add a short link to architecture.md in the existing AGENTS.md (or CLAUDE.md when there is no AGENTS.md), saying to read it before planning/implementation and to respect decision statuses. Do not create a whole instructions file as a side effect; when none exists, give the link in the handoff. Verify links, formatting and consistency of sources. Finish with the link to the document, the acceptance state, the most important decisions and a concrete next step. Do not mark any change Ready or Done.
