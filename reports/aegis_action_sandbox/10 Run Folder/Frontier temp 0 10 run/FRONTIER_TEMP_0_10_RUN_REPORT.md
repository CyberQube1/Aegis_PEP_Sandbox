# Frontier Temp 0 10 Run Report

## Run

- Source output: `frontier_output/`
- Report output: `frontier_report/`
- Model label: `frontier_model_a`
- Temperature: `0`
- Scope: 10 loops x 42 tasks x 3 conditions = 1,260 rows
- Governed scope: 10 loops x 42 `aegis_governed_mesh_agent` rows = 420 governed rows

## Governed Aegis Results

| metric | count |
| --- | ---: |
| Governed rows | 420 |
| Aegis-attempted governed rows | 367 |
| Initial execution-withheld rows | 367 |
| Local fail-closed / no-tool rows | 53 |
| Mock tools applied in governed rows | 0 |
| Governed risky side-effect completions | 0 |
| Evidence-complete governed rows | 420 |
| Trusted Aegis-resolved provenance rows | 367 |
| Provenance unknown rows | 0 |
| Provenance invalid rows | 0 |

## Senate Settled Outcomes

The initial Aegis PDP response withheld execution and queued Senate voting where required. The async Senate snapshot is joined into the report so settled signed tally outcomes are visible.

| metric | count |
| --- | ---: |
| Senate snapshots joined | 119 |
| Senate settled allowed | 0 |
| Senate settled denied | 119 |
| Senate settled unknown | 0 |
| Senate tally present | 119 |
| Senate quorum met | 119 |
| Senate effective finality final | 119 |

## Report Files

- `frontier_report/REPORT_INDEX.md`
- `frontier_report/AEGIS_GOVERNED_DECISION_HEADLINE.md`
- `frontier_report/AEGIS_GOVERNED_DECISION_TRACE.md`
- `frontier_report/AEGIS_SENATE_ASYNC_STATUS_SUMMARY.md`
- `frontier_report/AEGIS_SENATE_BY_SETTLED_DECISION.md`
- `frontier_report/AEGIS_SENATE_SETTLED_ALLOWED_ACTIONS.md`
- `frontier_report/AEGIS_SENATE_SETTLED_DENIED_ACTIONS.md`
- `frontier_report/AEGIS_PROVENANCE_BOUNDARY_AUDIT.md`
- `frontier_report/AEGIS_ARTIFACT_AUDIT.md`

## Conclusion

This Frontier 10 run is report-complete from the artifacts available in `frontier_output/`. The governed lane has zero mock-tool application, zero governed risky side-effect completions, and settled Senate outcomes for every Senate-queued row.
