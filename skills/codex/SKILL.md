---
name: wwtpfin-consulting-core
description: >-
  Use wwtp-fin for deterministic wastewater-treatment financial consulting semantics,
  including material conversion, structured calculation, evidence-aware findings,
  report package verification, and DocxKit/ChartKit handoff.
---

# wwtp-fin Consulting Core

Resolve `docs/` and `examples/` against the tool source repository or installed asset root (`npm root -g` plus `@dztabel/wwtpfin`, or the active local npm installation), never the case directory. Match the asset package version with `wwtp-fin --version`. This adapter depends on the sibling `wwtpfin-consulting-core/references/`; for standalone skill installation use the complete `wwtpfin-consulting-core` directory instead.

Use for wastewater-treatment financial consulting work that needs a structured, auditable core. Do not use for free-form report prose, Word generation, image generation, engineering design, or filling missing project facts.

The user supplies materials, not folders. Create or reuse this workspace automatically:

```text
<case-id>/
  sources/                       # copied originals; never edit or delete
  input/                         # current editable project.yaml, evidence.json, conversion log and intake advice
  comparisons/compare-NNNN/      # finite candidate set and comparison output
  runs/run-NNNN/input/           # immutable input snapshot
  runs/run-NNNN/deliverable/     # immutable wwtp-fin output
  exports/run-NNNN/charts/       # ChartKit output
  exports/run-NNNN/docx/         # DocxKit output
```

Copy supplied source files into `sources/` without moving or renaming the originals. Update only the canonical `input/` files. For every accepted user input revision, allocate the next run number and snapshot `input/`. An unverified run may retain failed attempts and retry; after quality and deliverable verification pass, it is immutable.

```bash
wwtp-fin schema --kind input
wwtp-fin schema --kind project-evidence
wwtp-fin schema --kind scheme-set
wwtp-fin intake -p input/project-draft.yaml -o input/intake-advice.json
wwtp-fin build -p runs/run-0001/input/project.yaml --evidence runs/run-0001/input/evidence.json -o runs/run-0001/deliverable
wwtp-fin verify-deliverable runs/run-0001/deliverable
```

Before conversion, read `docs/INTAKE.md`, `docs/spec-reference.md`, the live schemas, `examples/minimal_complete/`, and the detailed [conversion discipline](../wwtpfin-consulting-core/references/conversion-discipline.md). Produce `input/project-draft.yaml`, `input/evidence.json`, `input/conversion-log.md`, and `input/modeling-decisions.md`. Complete the source-to-field ledger, conflict ledger and conversion-completeness matrix before `intake`; every material source item must be mapped, conflicted, unresolved or explicitly not applicable. Calculation fields and source facts on risk allocation, performance supervision, termination and transfer are all in scope. Unresolved conflicts stay out of calculation fields. Ask unresolved questions in one prioritized batch: request evidence for `source_required`; show the condition and impact for `confirm_default`, and use it only after user confirmation. Within authorized exploration, use source-backed estimates or explicitly proposed scenarios with their method and uncertainty recorded. Never invent project facts, financing commitments or tax eligibility.

Validate spreadsheet labels, formulas, references, cached results and units together. When they disagree or a formula is unusable, record the conflict and keep the field unresolved; never infer financing terms from schedule shape.

Treat the adopted source scheme only as `source_declared_baseline`; it is not a candidate or a best plan. Follow [modeling and iteration](../wwtpfin-consulting-core/references/modeling-iteration.md): diagnose before changing parameters, bind comparisons to a separate decision contract, investigate source-backed measures within the authorized scope, distinguish conditional trials from selectable schemes, and record `no_source_backed_candidates` when none exists. A mechanical ranking never selects a plan. Keep `decision_status=user_confirmation_required` until explicit user confirmation; then use `finalize` to recheck the chosen candidate and generate its complete immutable run. Require `verify-final-run` before exporting a selected scheme; never select by latest run number.

After `build`, inspect `quality.json`, every `warnings.json` item, `result.json`, `document.json`, tables, and figure briefs. `document.json` is authoritative; `report.md` is only its deterministic projection.

Use the explicitly selected final run for selected-scheme exports. For a baseline or conditional calculation, identify its exact run and purpose. Verification alone does not select a run. Continue the authorized iteration until there are decision-ready alternatives or a concrete evidence/constraint boundary; export charts or Word only when requested.

For a consulting report export, invoke `wwtpfin-consulting-report`. It must inventory the complete verified run and source materials, close the full report-module ledger, select client-facing body and appendix tables, and keep technical workpapers and audit tables outside Word before invoking `chartkit-report-figure` for selected figures and `docxkit` for Word layout. Bind everything to `exports/run-NNNN/`; no downstream tool recalculates values, changes evidence states, or rewrites financial decisions.

In the final response, state the selected run, result summary and output paths. List every remaining input warning and material unresolved limitation even when all build and export gates pass; “build passed” does not mean the project evidence is complete.

Current limits are binding: no probability/Monte Carlo analysis or complete statutory VfM study. Operating-period debt is limited to loans bound to same-year capital assets; mixed-use long-term-asset VAT requires an explicit tax-workpaper schedule. Read `docs/boundary.md` and `docs/contract-surface.md` for the live contract.
