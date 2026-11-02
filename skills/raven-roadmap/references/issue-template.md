# Issue template

The issue holds what to achieve and the business rules, never how to build it. Every technical decision (technology, vendor, architecture, contracts, data, events, tests, CI) belongs to the plan made with `raven-plan`. Translate the headings when the issue is written in another language; delete empty optional sections. Keep it short.

````markdown
## Outcome
<what the customer, admin or business gains, in domain language>

## Business rules
- <rule or parameter agreed with the user or stated in the source>

## Scope
<behaviors included>

## Out of scope
<behaviors the source or the user excluded, including rules the user consciously left unhandled>

## Acceptance criteria
- [ ] <observable behavior from the customer, admin or shop perspective: situation → what happens → what they see>

## Open questions (optional)
- <business rule the user could not answer yet; raven-plan settles it with the user>

## Dependencies
<issues that must be delivered first, one `#N` per line (also set as "blocked by" relations), or "none">

## Sources
- <PRD section, Jira ticket with ID and update date, user's description>
- Client's technical hint, to settle in the plan: <hint given by the user, verbatim and only if they gave one>
- Technical decision recorded in <source and section>: <one line, only if the user's PRD, ticket or decision record already settles it, e.g. an approved vendor>
````

## Epic

An epic holds only what its issues deliver together; business rules, scope and AC stay in the issues. Its sub-issues are attached on GitHub, not listed in the body.

```markdown
## Outcome
<what the group of outcomes gives the customer, admin or business, one or two sentences>

## Sources
- <PRD section, Jira epic with ID and update date, user's description>
```

## Never in the issue body

- Code-level names (identifiers) of libraries, packages, versions, files, paths, endpoints, events, workflows, hooks, tables or fields. Domain words such as "order placed" or "delivery address" are fine.
- A technology or vendor choice, except one of the two Sources lines above: a hint from the user or a decision their source already records.
- Tests, lint, CI, build or migrations as acceptance criteria. They live in the plan's Verification.
- An "Assumptions" section or any business rule the agent made up. A rule nobody settled goes to Open questions; to Out of scope only when the user chose to leave it unhandled.
- A scope item, exclusion or acceptance criterion the agent derived without the user agreeing to it (extra edge cases, message wording, admin views). Ask about it or leave it out.
- Technical findings from reading the code. The code only prevents duplicates, conflicts and wrong dependencies.

## Check every sentence

1. Would this sentence still be true if the change were built a different way (another library, module, data model or vendor)? If not, it does not belong in the issue: cut it, or rephrase it as the behavior the user observes.
2. Can you point to where the source or the user said it? If not, cut it, or ask the user before writing. Answers given in the interview count.
