# Brownfield reports in Git

A map of the whole repo has one place: `context/foundation/repo-map.md`. A map limited to the area of one change goes to `context/changes/<id>/repo-map.md`. Do not create artifact issues, comment snapshots or a second copy of the report.

The report contains the goal/scope, sources and versions, HEAD/branch/dirty state, time of the investigation, path:line evidence, method, uncertainties and the next step. Use real metadata; mark unknowns. Distinguish facts, interpretations and decisions. Update the file with a readable diff; Git keeps the history.

Confidential materials belong in the approved artifacts repo, which may differ from the code repo. Record the mapping explicitly; do not copy to a personal remote. A private Project does not make a public repo private. No access to a source is a gap, not permission for a substitute publication.

When resuming, read the current report and only the sources needed for the gap. Do not fetch the whole issue history. Historical GH artifacts stay in place; migration needs a separate request.
