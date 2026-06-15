# Senate Async Status Snapshot

This file is generated after the matrix run and before paper reports are exported.
It joins async Senate voting path outcomes back to governed rows by escalation ID.

| Metric | Value |
| --- | ---: |
| total_escalation_ids | 119 |
| snapshot_rows | 119 |
| terminal_rows | 119 |
| incomplete_rows | 0 |
| tally_present_rows | 119 |
| quorum_met_rows | 119 |
| source_citation_rows | 119 |

## Status Counts

```json
{
  "denied": 119
}
```

## Decision Counts

```json
{
  "deny": 119
}
```

## Notes

- Initial PDP rows may say `pending`; settled verdicts are the Senate status rows in this snapshot.
- Report generation reads this artifact and emits settled allowed/denied Senate tables.
- Client/PEP citations are not used to satisfy provenance completeness.
