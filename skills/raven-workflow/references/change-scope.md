# Change boundaries and decomposition

Shared rules for the roadmap and planning. They add no new stage, status or scoring.

## Unit of work

A **change** delivers one bounded outcome that can be implemented, verified and merged on its own. It does not have to enable a product launch by itself; a full user journey may need several changes. Do not force feature flags just to justify a split. A **task/phase** is an execution step of that one outcome. A part with its own independent acceptance is a candidate for a separate change, not automatically another task.

Keep the scope vertical: the UI, API, data model and validation the outcome needs belong to it. Do not split by layer, and do not merge independent features because they share a model, screen or process. A dependency between outcomes describes order; it does not justify gluing them together.

Safeguards required for a feature to be correct stay with it. For example, payment retry, no double charge and handling of a captured amount without an order are not later "hardening". Needing a safeguard does not, however, authorize building unrequested subsystems.

A technical change is justified by a demonstrated problem or a named outcome it unblocks. If the work fits naturally into its first consumer, do it there; potential reuse does not justify separate infrastructure "for the future".

## Boundary check

Before publishing a change in the roadmap and while planning, check:

1. Does the description name one outcome, or a list of features under a general title?
2. Can the parts be shown and accepted independently once their dependencies are met?
3. Does a part need its own vendor choice, integration contract or risk decision? That signals a possible separate boundary, not an automatic split.
4. Should a failure of one part block acceptance and merge of the others? Distinguish the required guarantees of one feature from independent outcomes.
5. Do the acceptance criteria check one feature with its errors and exceptions, or several separate demos?

A change typically has one main outcome and 1–2 significant implementation phases. Tests belong to the change (flow tests in the plan's Verification); an extra testing activity is not an independent outcome. Three or more implementation phases or several integrations are a warning to re-evaluate the boundary, not a limit. Do not create roadmap tasks just to count them. Number of files, FRs, checkboxes or estimates do not measure the right size of a change. More tasks do not fix a scope that is too wide.

A larger change is acceptable when a short factual justification names an inseparable guarantee or a concrete consequence of splitting that would make the parts impossible to accept on their own. "It's checkout" or "shared model" alone is not enough. Record the justification in the existing scope/approach description, without a new form.

## Roadmap

When asked to create or update the roadmap, split sensible independent outcomes on your own. Ask when a proposal changes requirements or priorities or defers required behavior; an ordinary sequence of dependent changes is not such a deferral. A request for the status or plan of a single issue does not authorize reorganizing the queue.

Cover the whole agreed PRD: every requirement has an assigned outcome, evidence of earlier delivery, or an explicitly approved deferral. Describe later changes by outcome, boundaries, sources, dependencies and observable acceptance criteria. Do not settle details of future integrations now. Keep the dependency graph acyclic (DAG). Milestones are optional grouping; do not add epics or another mandatory hierarchy.

## Planning one change

After reading the requirements, existing decisions and progress, **before detailed research and interviewing**, apply the boundary check. The existence of an issue does not prove the split is right. Gather just enough context to judge the outcome; do not investigate every integration only to discover afterwards that the scope is too large.

When the scope is too wide, present a short reason, the proposed outcomes and dependencies, the mapping of existing requirements, and the recommended first change. Do not plan all parts in detail. Planning may propose a split; writing changes to the existing queue requires user authorization covering that reorganization. Until you have it, wait for the decision before reorganizing the queue or planning the chosen new scope in detail.

Run the second check before refining the phase structure. A new independent outcome discovered during research goes back to the split proposal instead of becoming another phase. When a discovery requires a significant extension of the current outcome, show the impact and get the user's decision. A new extension is not a routine plan addition.

**No open questions** means the requirements, boundaries and significant architecture decisions of this change are settled. It does not require designing future changes or every implementation decision. Leave details to the implementer when the contract, constraints and verification are known. Every extra investigation must answer a concrete gap that could change scope, feasibility, contract or acceptance criteria; stop once that gap is settled.

Every change has its own acceptance and a fitting scope of durable tests. Do not defer all verification to the end of a multi-step product process. A small change gets a proportionate plan, without artificial tasks or a duty to test every layer.

## Splitting existing work

Preserve history, identifiers, decisions, sources, evidence and progress. The proposal shows the mapping of the old scope onto new outcomes and the impact on existing tasks and dependencies. Do not re-ask about agreed vendors or business rules; investigate only a real new gap or contradiction.

After authorization, update only the issues it covers. Keep links to historical plans. Do not close or delete issues/tasks without a separate explicit instruction. Planning, regenerating a description or updating Raven instructions does not migrate existing roadmaps.
