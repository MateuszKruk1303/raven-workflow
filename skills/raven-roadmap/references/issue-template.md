# Issue template

The issue holds what to achieve and the business rules, never how to build it. Every technical decision (technology, vendor, architecture, contracts, data, events, tests, CI) belongs to the plan made with `raven-plan`. Translate the headings when the issue is written in another language; delete empty optional sections.

````markdown
## Outcome
<what the customer, admin or business gains, in domain language>

## Business rules
- <rule or parameter agreed with the user or stated in the source>

## Scope
<behaviors included>

## Out of scope
<behaviors excluded, including rules the user consciously left unhandled>

## Acceptance criteria
- [ ] <observable behavior from the customer, admin or shop perspective: situation → what happens → what they see>

## Open questions (optional)
- <business rule the user could not answer yet; raven-plan settles it with the user>

## Dependencies
<issues that must be delivered first, or "none">

## Sources
- <PRD section, Jira ticket with ID and update date, user's description>
- Client's technical hint, to settle in the plan: <hint given by the user, verbatim and only if they gave one>
- Technical decision recorded in <source and section>: <one line, only if the user's PRD, ticket or decision record already settles it, e.g. an approved vendor>
````

## Never in the issue body

- Code-level names (identifiers) of libraries, packages, versions, files, paths, endpoints, events, workflows, hooks, tables or fields. Domain words such as "order placed" or "delivery address" are fine.
- A technology or vendor choice, except one of the two Sources lines above: a hint from the user or a decision their source already records.
- Tests, lint, CI, build or migrations as acceptance criteria. They live in the plan's Verification.
- An "Assumptions" section or any business rule the agent made up. A rule nobody settled goes to Out of scope or Open questions.
- Technical findings from reading the code. The code only prevents duplicates, conflicts and wrong dependencies.

## Check every sentence

Would this sentence still be true if the change were built a different way (another library, module, data model or vendor)? If not, it does not belong in the issue: cut it, or rephrase it as the behavior the user observes.
