# Senate Async Status Snapshot

This file is generated after the matrix run and before paper reports are exported.
It joins async Senate voting path outcomes back to governed rows by escalation ID.

| Metric | Value |
| --- | ---: |
| total_escalation_ids | 12 |
| snapshot_rows | 12 |
| terminal_rows | 12 |
| incomplete_rows | 0 |
| tally_present_rows | 12 |
| quorum_met_rows | 12 |
| source_citation_rows | 12 |

## Status Counts

```json
{
  "denied": 12
}
```

## Decision Counts

```json
{
  "deny": 12
}
```

## Notes

- Initial PDP rows may say `pending`; settled verdicts are the Senate status rows in this snapshot.
- Report generation reads this artifact and emits settled allowed/denied Senate tables.
- Client/PEP citations are not used to satisfy provenance completeness.
