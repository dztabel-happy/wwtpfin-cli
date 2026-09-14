# Project workspace

The user supplies project materials and a goal. The agent owns workspace creation and file placement.

```text
<case-id>/
├── sources/
├── input/
│   ├── project-draft.yaml
│   ├── project.yaml
│   ├── evidence.json
│   ├── conversion-log.md
│   ├── modeling-decisions.md
│   ├── decision-contract.yaml
│   └── intake-advice.json
├── selections/                 # each choice gets its own immutable record
├── rounds/                     # CLI case checkpoints
├── case.json
├── CURRENT.md
├── comparisons/
│   └── compare-0001/
│       ├── scheme-set.yaml
│       └── output/
├── runs/
│   └── run-0001/
│       ├── input/
│       └── deliverable/
└── exports/
    └── run-0001/
        ├── charts/
        └── docx/
```

## Creation and reuse

- Derive a short filesystem-safe `case-id` from the project name. If the user identifies an existing case directory, reuse it.
- Create the workspace directories automatically. Do not ask the user to create or arrange them.
- Copy supplied source files into `sources/` and preserve their filenames. Never move, edit, rename, or delete the user's originals.
- If a different source file has the same filename, keep both with a numeric suffix and record the rename in `input/conversion-log.md`.
- Keep source files read-only in practice: conversion outputs belong in `input/`, never in `sources/`.

## Mutable input and immutable runs

- `input/` is the single current editable version. New evidence and user corrections update this directory.
- Put every finite option comparison under `comparisons/compare-NNNN/`. Its output records the base input SHA-256; never compare against an unrecorded or changing base.
- A comparison result is advisory. Always bind iterative comparisons to `input/decision-contract.yaml` and the evidence snapshot. Keep conditional candidates separate from candidates whose implementation conditions have been recorded as satisfied.
- After an explicit user choice, record the exact candidate and hashes in `selections/selection-NNNN.json`, then use `finalize` to create the next run. Its `input/` snapshots include canonical parameters, evidence, contract, comparison and selection; `final-run.json` binds them to the full deliverable. Validate with `verify-final-run` before export. Keep the other conversion workpapers in the case workspace under version control.
- For each accepted user input revision, allocate `run-NNNN` as one greater than the highest existing run number.
- For a baseline/conditional `build`, copy the complete current `input/` directory into `runs/run-NNNN/input/` before building. For `finalize`, supply a new empty run path; the command creates its own bound input snapshot.
- A newly allocated run remains staging until quality and `verify-deliverable` pass. While it is unverified, correct the canonical input, refresh its snapshot, and retain failed deliverables as `deliverable-failed-attempt-N/` before retrying into an empty `deliverable/`.
- Once verified, the run is immutable. Never overwrite or repair a verified run in place.
- Keep failed attempts for diagnosis, but never use them for downstream exports.

## Selecting an export source

For a chosen scheme, use the explicitly confirmed final run and require `verify-final-run` to pass. The highest-numbered verified trial may be an unselected sensitivity or upper-bound scenario and must not become a final scheme automatically.

For a standalone baseline/conditional calculation, use the exact run requested or explicitly identified for that purpose. It must satisfy both conditions at selection time:

1. `deliverable/quality.json` reports a passing quality gate.
2. `wwtp-fin verify-deliverable runs/run-NNNN/deliverable` exits successfully.

Do not select by directory modification time, a `latest` symlink or the highest run number. If the user requests a final chosen scheme and none exists, complete useful candidate work and present the actual choice required. Do not substitute the newest trial.

## Export binding

- Put downstream work under `exports/run-NNNN/`, using the exact selected run number.
- Never mix tables, figures, report semantics, or conclusions from different runs.
- Rebuilding after an input change creates a new run and a new export directory; old runs and exports remain unchanged.

## Current artifact and interaction history

Follow package `docs/CASE_WORKFLOW.md` for `case checkpoint` and `case status`. Save user messages verbatim and preserve reasons in the business response. A material update starts a new working round before any recalculation; old results remain historical. Register comparisons with their scheme-set dependency and new selected outputs explicitly. Refresh `CURRENT.md` before responding or handing off a file; never link a stale selected result as current. Use a new `selections/selection-NNNN.json` for each confirmation.

When the user only confirms a current candidate and its calculation basis is unchanged, record the stage-three interaction with that same current comparison and scheme-set attached. Then call `finalize`, and register the new selected output. A no-artifact checkpoint intentionally withdraws the current comparison and is for renewed research, not this unchanged-input confirmation transition.
