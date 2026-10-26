# Plan template

Adapt to the size of the change; delete empty sections. The plan is a working document: do not add checkpoints, statuses, test results or change history. Translate the headings when the plan is written in another language.

````markdown
# <id> — <outcome>

- Issue: <URL> (or Ticket: <KEY> and its link, if known)
- Goal: <observable outcome for the user>

## Acceptance criteria
- AC1: <condition → behavior → what is visible>
- AC2: <significant error or boundary>

## Scope
<what is in; what is consciously out of scope>

## Decisions and approach
<technology/vendor and architecture decisions with the chosen alternative and why (who decided); affected modules, API/data contracts, events, migration or rollback if needed>

## Slices
1. <vertical slice: ACs it delivers; contract (types, interfaces); affected areas; depends on: — / slice N>
2. <only if needed>

## Verification
<which path in the running app to check; which flow tests to add or reuse; technical criteria such as lint, CI, migrations; risks to watch>
````
