# Prototype format

## Layout

```text
context/prototypes/
├── index.html        map of the app: links to every flow, stubs labeled "not in the prototype"
├── tokens.css        shared design tokens, linked by every flow
└── <flow-slug>/      one folder per flow, named after the customer's path (e.g. purchase, fabric-choice)
    ├── index.html    the clickable flow
    ├── notes.md      sources, rules, assumptions, feedback, check
    └── assets/       optional local images the user provided (product photos, fabric swatches)
```

A feature from an issue adds a flow folder or extends an existing one, and gets a link in the map. History lives in Git: update files in place; the accepted state is the one recorded in `notes.md`.

## notes.md

```markdown
# <Flow name>

- Source: <PRD sections | #issue / #epic | Ticket: KEY link | plan path | the prompt as given>
- Status: draft | shown to the client <date> | accepted <date>
- Actor, start → success: <who, where they start, what counts as done>

## Screens and states
| Screen / state | Action | Next state | Rule / assumption |

## Rules shown
- <rule, with its source (PRD section, issue, user's answer on <date>)>

## Assumptions and sample data
- A1: <what was assumed or made up, why it was needed, how to confirm it>

## Open questions as variants
- <question: variant A / variant B, how to switch in the prototype>

## Outside the prototype
- <destinations shown as stubs and why>

## Client feedback
- <date>: <remark> → <PRD section | issue #N | listed for the ticket | open>

## Check
- <date>: passed | failed | not checked — <what was walked, what was not>
```

Leave out sections with nothing to say. Rules keep their source's meaning. A rule settled only here is pending transfer to the PRD or an issue; later skills confirm it rather than treat it as settled. Issues point back to the flow from their Sources (`Prototype: flow <name>, accepted <date>`), so `notes.md` keeps no issue list.

## Building a flow

- **Self-contained and offline.** HTML with inline CSS and JS plus `../tokens.css` and local `assets/`. No CDN, web fonts, analytics, cookies, storage, `fetch` or real endpoints; forms never submit anywhere. It opens from disk with a double click.
- **Marked as a prototype.** A slim banner on every screen: prototype, sample data. Make it look like the product through the tokens, but do not polish beyond what the flow needs; the client should judge the flow, not the pixels.
- **Realistic data.** The client's real products, prices, lead times and rules where given; otherwise plausible sample values marked in the assumptions. Never lorem ipsum, never real personal data or credentials.
- **State in memory.** Actions change what the next screen shows (a chosen fabric changes the price and photo, the cart total includes delivery). A Reset control restores the start.
- **States the flow needs.** Validation errors with correction and resubmission, empty, loading, failure and recovery where the source implies them. State switches may sit in a small labeled "Test states" panel. Do not invent business policy to fill a state.
- **Variants for open questions.** A labeled switch between the alternatives, each consistent through the whole flow.
- **Honest boundaries.** A control outside the prototype leads to a stub saying so, with a way back; no active-looking control does nothing; no success screen stands in for an unbuilt required step. A part that would need custom work on the platform is labeled as such when known.
- **Usable.** Real links and buttons, labeled form fields, visible focus, readable on a phone. Screens switch by URL hash (`#cart`), so browser back works under `file://`, where `history.pushState` does not; an unknown hash leads back to the start. Put any user-provided text into text nodes, not HTML strings.
