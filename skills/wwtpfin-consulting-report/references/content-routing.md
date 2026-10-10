# Content routing for a full report

The deliverable is complete source material, not a page sequence. Inventory all artifacts, then select.

| Source | Default use |
| --- | --- |
| `document.json` semantic blocks | Main source for conclusions, analysis, qualifications and recommendations. |
| `tables/index.json` with `report_role:body` | Client-facing decision or fact table. Keep it in the body or move it to an appendix with a stated reason; never hide it as audit material. |
| `report_role:appendix` | Candidate client schedule. Include it only when the reader needs it to understand, use or review a stated conclusion. |
| `report_role:workpaper` | Technical detail retained in the verified run. Keep it outside Word unless a specific client decision requires promotion. |
| `report_role:audit` | Verification only; never place in the client report. |
| `figures/index.json` | Candidate figures; render only when a visual materially clarifies a trend, boundary or comparison. |
| `warnings.json` | Route each warning separately; disclose material effects, retain technical-only warnings outside the manuscript, and never silently discard one. |
| `evidence.json#/unresolved` | Route each unresolved item separately to the relevant limitation, appendix, user request or justified exclusion. |
| Required user inputs | Keep as `user_required`; omit the unsupported module from the manuscript and consolidate the request once unless the user explicitly asks for a skeleton. |

## Table rules

- Preserve the CSV for traceability, but display the title and `columns[].label` from the table index.
- Do not expose machine IDs, implementation switches, residual formulas, check expressions or workbook-like intermediate schedules to the reader.
- Prefer a concise summary table in the body. Select only the schedules needed by the client; leave duplicate variants, exhaustive annual ledgers and model intermediates in the verified run.
- Wide period tables should be summarized or split by analytical purpose; never shrink an unreadable full-period table into a page.
- Do not include both wide and long variants of the same schedule. Do not convert one source table into repeated appendix segments merely to achieve artifact coverage.

## Disposition rules

- `body`: directly supports a section conclusion or necessary fact pattern.
- `appendix`: useful supporting detail that interrupts the main argument.
- `chart_source`: used to render a selected figure; the source table need not also appear.
- `workpaper_only`: complete technical material retained in the run but intentionally absent from the client Word.
- `audit_only`: reserved for artifacts whose indexed `report_role` is `audit`.
- `user_required`: material section or fact that cannot be produced from the verified run; it stays in the ledger and consolidated request list, not as a filled or empty client chapter.
- `not_applicable`: intentionally excluded with a concise reason.

Every artifact gets exactly one disposition. Every client-facing artifact gets a visible destination or a specific exclusion reason. Workpapers and audit material remain available in the run without being copied into Word.
