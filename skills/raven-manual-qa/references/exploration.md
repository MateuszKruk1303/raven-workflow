# Exploratory QA heuristics

Pick probes for the feature, the available data and the risk. First establish what effect the user wants and what must not be lost, duplicated or exposed. From each relevant category pick a distinguishing case; skip the irrelevant ones. These are inspirations, not a mandatory matrix of all combinations.

| Area | Probe ideas | Observed effect |
| --- | --- | --- |
| Data boundaries | Empty field, spaces only, zero, negative value, the limit and just past it, long text, Unicode, pasting | Validation, readable message, valid fields not lost |
| Collections | No records, one, many of reasonable size, duplicates, similar names, missing optional fields | Empty states, selecting the right record, sorting and pagination |
| Dates and numbers | End of month, from/to range, same date, decimal separator, time zone within the feature's scope | View matches the saved result and the agreed rule |
| Order of actions | Save twice, Enter and click, cancel and reopen, go back a step | Duplicates, button locking, leftover state |
| Navigation | Refresh halfway, Back/Forward, direct link, new tab, re-entry | Data loss, wrong routing, inconsistent state |
| Concurrency | The same own record in two tabs, saving a stale form after a change in the other | Overwritten changes, no conflict message, fake success |
| Filters and search | No results, clearing, combined filters, changing a filter on a later page | Lost selection, wrong counters, stale results |
| Permissions | Available test accounts with different roles, allowed organization switch, old link to own record | Data exposure, action not allowed by the contract |
| Files and import | Allowed file, empty file, wrong format, duplicate, aborted selection; realistic small samples | Partial write, misleading success, no error information |
| Interruption | Cancel, connection loss in a controlled session, retry after an error | Regaining control, no duplicated operation, data preserved |
| UI handling | Tab/Shift+Tab, Enter/Escape, focus after a dialog, a reasonable small screen, zoom | Blocked action, invisible error, covered controls |
| Persistence and integration | Reopen, check list and details, read after re-entry | Mismatch between write and view, stale summary |

Combine two related probes when they reveal a new risk: e.g. filter + pagination, two tabs + edit, failed save + retry. Change one thing at a time while narrowing a reproduction.

Do not confuse creativity with random clicking. Every probe has a hypothesis and an observable result. "The user does silly things" means a realistic mistake, repetition, wrong order or using data contrary to what the form expects. It does not mean DoS, mass sending, real purchases or testing other people's accounts.

If a scenario needs a tool capability that is not available (e.g. network simulation), check another feasible variant or record the limitation. Do not claim a simulation was run based on code analysis alone.
