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
<settled decisions, affected modules, API/data contracts, order of steps, migration or rollback if needed>

## Steps
1. <step, affected areas, tests with it>
2. <only if needed>

## Verification
<which tests and which path in the running app to check; risks to watch>
````
