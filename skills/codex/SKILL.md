---
name: wwtpfin-consulting-core
description: >-
  Use wwtp-fin for deterministic wastewater-treatment financial consulting semantics,
  including material conversion, structured calculation, evidence-aware findings,
  report package verification, and DocxKit/ChartKit handoff.
---

# wwtp-fin Consulting Core

Use for wastewater-treatment financial consulting work that needs a structured, auditable core. Do not use for free-form report prose, Word generation, image generation, engineering design, or filling missing project facts.

The user supplies materials, not folders. Create or reuse this workspace automatically:

```text
<case-id>/
  sources/                       # copied originals; never edit or delete
  input/                         # current editable project.yaml, evidence.json, conversion log and intake advice
  runs/run-NNNN/input/           # immutable input snapshot
  runs/run-NNNN/deliverable/     # immutable wwtp-fin output
  exports/run-NNNN/charts/       # ChartKit output
  exports/run-NNNN/docx/         # DocxKit output
```

Copy supplied source files into `sources/` without moving or renaming the originals. Update only the canonical `input/` files. For every accepted user input revision, allocate the next run number and snapshot `input/`. An unverified run may retain failed attempts and retry; after quality and deliverable verification pass, it is immutable.

```bash
wwtp-fin schema --kind input
wwtp-fin schema --kind project-evidence
wwtp-fin intake -p input/project-draft.yaml -o input/intake-advice.json
wwtp-fin build -p runs/run-0001/input/project.yaml --evidence runs/run-0001/input/evidence.json -o runs/run-0001/deliverable
wwtp-fin verify-deliverable runs/run-0001/deliverable
```

Before conversion, read `docs/INTAKE.md`, `docs/spec-reference.md`, the live schemas, and `examples/minimal_complete/`. Produce `input/project-draft.yaml`, `input/evidence.json`, and `input/conversion-log.md`. Run `wwtp-fin intake` before `build`. Ask unresolved questions in one prioritized batch: request evidence for `source_required`; show the condition and impact for `confirm_default`, and use it only after user confirmation. Never suggest project-specific numbers or invent financing, tax eligibility, benchmarks, values, or a conclusion.

After `build`, inspect `quality.json`, every `warnings.json` item, `result.json`, `document.json`, tables, and figure briefs. `document.json` is authoritative; `report.md` is only its deterministic projection.

The latest run is the highest-numbered run whose `quality.json` passes and whose `verify-deliverable` command succeeds now. Failed or merely newest runs are ineligible. Stop after verification unless the user requests rendered charts or a Word report.

For exports, bind everything to `exports/run-NNNN/`. When figures are needed, invoke `chartkit-report-figure` first with selected figure briefs and matching CSV data; render only materially useful figures and require its quality gate to pass. Then invoke `docxkit` with the selected run's authoritative `document.json`, tables and final chart assets. DocxKit owns Word layout and numbering; ChartKit owns image rendering. Neither downstream tool recalculates values, changes evidence states, or rewrites financial decisions. Report the source run number with every export.

In the final response, state the selected run, result summary and output paths. List every remaining input warning and material unresolved limitation even when all build and export gates pass; “build passed” does not mean the project evidence is complete.

Current limits are binding: no probability/Monte Carlo analysis, mixed-use long-term-asset VAT adjustment, non-capitalized construction interest, operating-period new long-term debt, generic multi-scheme scenario-group orchestration, or complete statutory VfM study. Read `docs/boundary.md` and `docs/contract-surface.md` for the live contract.
