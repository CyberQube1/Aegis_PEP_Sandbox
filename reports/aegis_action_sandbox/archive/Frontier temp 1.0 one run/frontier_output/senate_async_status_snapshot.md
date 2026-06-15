# Senate Async Status Snapshot

This file is generated after the matrix run and before paper reports are exported.
It joins async Senate voting path outcomes back to governed rows by escalation ID.

| Metric | Value |
| --- | ---: |
| total_escalation_ids | 9 |
| snapshot_rows | 9 |
| terminal_rows | 9 |
| incomplete_rows | 0 |
| tally_present_rows | 9 |
| quorum_met_rows | 9 |
| source_citation_rows | 9 |

## Status Counts

```json
{
  "denied": 9
}
```

## Decision Counts

```json
{
  "deny": 9
}
```

## Notes

- Initial PDP rows may say `pending`; settled verdicts are the Senate status rows in this snapshot.
- Report generation reads this artifact and emits settled allowed/denied Senate tables.
- Client/PEP citations are not used to satisfy provenance completeness.
