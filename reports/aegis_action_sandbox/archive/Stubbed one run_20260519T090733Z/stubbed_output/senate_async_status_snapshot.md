# Senate Async Status Snapshot

This file is generated after the matrix run and before paper reports are exported.
It joins async Senate voting path outcomes back to governed rows by escalation ID.

| Metric | Value |
| --- | ---: |
| total_escalation_ids | 18 |
| snapshot_rows | 18 |
| terminal_rows | 18 |
| incomplete_rows | 0 |
| tally_present_rows | 18 |
| quorum_met_rows | 18 |
| source_citation_rows | 18 |

## Status Counts

```json
{
  "denied": 18
}
```

## Decision Counts

```json
{
  "deny": 18
}
```

## Notes

- Initial PDP rows may say `pending`; settled verdicts are the Senate status rows in this snapshot.
- Report generation reads this artifact and emits settled allowed/denied Senate tables.
- Client/PEP citations are not used to satisfy provenance completeness.
