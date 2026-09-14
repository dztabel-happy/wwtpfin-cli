---
name: wwtpfin-consulting-core
description: >-
  Convert wastewater-treatment project materials into verified structured financial consulting
  semantics with wwtp-fin, then hand the deliverable to DocxKit and ChartKit. Use for污水处理财务测算、
  特许经营财务评价、BOT/TOT/ROT/BOOT/DBFOT/O&M 项目咨询内容包、财务可行性与项目材料转化。
---

# wwtp-fin Consulting Core

Use this CLI when the task needs deterministic wastewater-project financial calculation, checks, evidence-aware findings, structured report content, tables, or figure briefs. Do not use it to write an unconstrained narrative, make a Word file, draw a chart, infer missing facts, or replace an engineering/design study.

## Project workspace

The user supplies materials, not folders. Before conversion, create or reuse one case directory and place files according to [workspace management](references/workspace.md). Copy source files into `sources/`; never move, rename, edit, or delete the user's originals.

Use the same-version package skill assets; a machine-global copy may be stale even when the skill name matches.

Maintain one editable input set under `input/`. Every accepted input revision gets a numbered run containing an input snapshot and the CLI deliverable. A run becomes immutable after quality and deliverable verification pass. Downstream exports must be bound to the exact verified run that produced them.

## Workflow

Resolve the tool's asset root before reading `docs/` or `examples/`: use the source repository when working there, otherwise locate `@dztabel/wwtpfin` under `npm root -g` (or the active local npm installation). These paths are relative to that asset root, not the case directory. Compare its `package.json` version with `wwtp-fin --version`; update mismatched CLI and skill assets before using new commands. The installed CLI schemas remain authoritative.

1. Create or resume the case workspace. Copy the supplied Word, Excel, PDF and other source files into `sources/` while preserving their names.
2. Read `wwtp-fin --help`, the current input and evidence schemas, `docs/INTAKE.md`, and `examples/minimal_complete/`.
3. Convert `sources/` into `input/project-draft.yaml`, `input/evidence.json`, and `input/conversion-log.md`. Preserve source wording, locator, date and evidence state. Complete the source-to-field ledger, conflict ledger and conversion-completeness matrix before continuing.
4. Run `wwtp-fin intake -p input/project-draft.yaml -o input/intake-advice.json` after recording the disposition of material source items. Keep conflicting facts unresolved. Missing workbooks do not prevent authorized, source-backed estimates or conditional scenarios: record the method, source, uncertainty and intended use; do not represent an estimate as a fact. Ask one prioritized batch only for information that actually blocks useful work. Product defaults remain proposals, not evidence.
5. Once ready, save the canonical parameters as `input/project.yaml` and build the source-declared baseline run. Diagnose the result before proposing any change; a baseline is not a candidate or a best plan.
6. For iteration, follow [modeling and iteration](references/modeling-iteration.md). Establish a separate decision contract, actively investigate supported measures within the user's authorized scope, calculate conditional scenarios and complete combinations, and distinguish numerical feasibility from implementation readiness. Give reasoned recommendations within the evaluated set; final choice stays with the user. If no source-backed measure exists, record `no_source_backed_candidates` and identify the evidence needed to continue.
7. Create the next `runs/run-NNNN/`, copy the accepted `input/` into its `input/` snapshot, and build into its empty `deliverable/` directory.
8. Inspect every `warnings.json` item and `quality.json`, then run `verify-deliverable`. Read `document.json` / `report.md`, `result.json`, checks, decisions, tables and figure briefs together; never promote a warning, missing input, or unverified benchmark into a conclusion.
9. After an explicit scheme choice, use `finalize` to generate a new complete run and `verify-final-run` to validate its binding. Never select a final scheme by run number or modification time. For a standalone calculation, identify it as baseline or conditional work. Produce Word or rendered charts only when requested, using the explicitly selected verified run and [downstream handoff](references/handoff.md).

```bash
wwtp-fin schema --kind input
wwtp-fin schema --kind project-evidence
wwtp-fin schema --kind scheme-set
wwtp-fin schema --kind decision-contract
wwtp-fin schema --kind scheme-selection
wwtp-fin intake -p input/project-draft.yaml -o input/intake-advice.json
wwtp-fin compare -p input/project.yaml --contract input/decision-contract.yaml --evidence input/evidence.json --schemes comparisons/compare-0001/scheme-set.yaml -o comparisons/compare-0001/output
wwtp-fin build -p runs/run-0001/input/project.yaml --evidence runs/run-0001/input/evidence.json -o runs/run-0001/deliverable
wwtp-fin verify-deliverable runs/run-0001/deliverable
```

## Current work and return paths

For interactive cases, use package `docs/CASE_WORKFLOW.md`. Record each user request verbatim and the business response with reasons; `case checkpoint` stores the input/evidence snapshot and current artifact. At receipt of a material change, record work in progress before further research, so an old recommendation is not presented as current. At every response, resumed session and export, run `case status` and direct the user to `CURRENT.md` plus the exact artifact. Return to any earlier stage when new facts or preferences require it; preserve old rounds and selections.

Record a comparison with its actual scheme-set path, not just the result JSON. Record the selected final run after verification. `current` means consistent with current inputs, not approved or optimal. A stale or in-progress state must not fall back to a historical result. Before exporting a selected scheme, use `verify-final-run RUN --case CASE`; historical file integrity alone cannot establish current validity.

## Required conversion discipline

- Preserve missing financing as unresolved in the source baseline. With authorization to explore alternatives, use explicitly proposed loan scenarios with recorded sources or estimation methods; these are not commitments, approval or confirmed terms.
- The source-declared baseline may reproduce explicit terms and assumptions that the supplied scheme actually uses, even when their evidence state is `proposed_not_binding`. Preserve that state and say the run reproduces the source scheme; never call those terms binding, verified, recommended or optimal. Proposed alternatives not used by the source calculation stay unresolved.
- For explicit `opex_items[].annual_amounts_wan`, do not invent formula-only `base_wan`, `scales_with_volume` or `annual_growth_rate`. `price_adj_group` is required only when tariff adjustment is active; `vat_scope` is required only when by-product revenue exists.
- A spreadsheet formula is usable only after its references, cached result, units and labels agree. Record any contradiction as unresolved; never infer financing terms from schedule shape.
- Conversion is incomplete until calculation fields and source material on risk allocation, performance supervision, termination and transfer are each mapped, unresolved or explicitly not applicable.
- Never invent project facts or derive tax eligibility from a favorable result. Distinguish fact, design choice, estimate, negotiation proposal and missing information. Supported assumptions may be calculated within an authorized exploration; final decisions must disclose their conditions. A product default is a labeled proposal, not a fact.
- Do not elevate evidence state, turn a table into prose, serialize raw JSON into the report, or use a shared rule catalog as project evidence.
- Record full material qualifications in `declared_basis`; retain declared totals and targets in `declared_scalars`.
- Keep pre-tax, after-tax and target bases distinct. A financial benchmark must record its source, date, provider and evidence state.
- Ask the grouped `profit_distribution_policy` question once; do not split it back into three prompts or fill any ratio with 0 or 100%.
- When a binding source gives cumulative water thresholds and tariff multipliers, map them to `revenue.marginal_volume_tiers`. The last tier must have `up_to_m3d: null`. A proposed clause may be used only to reproduce a source-declared baseline that demonstrably applies it; otherwise it stays unresolved and must not activate tiered billing.
- Review `D7-*` warnings individually. A successful exit code does not erase a warning.

Read [conversion discipline](references/conversion-discipline.md) before material conversion.

## Read the result correctly

- `quality.json`: whether the completed content package passed its quality gate.
- `warnings.json`: input-shape information requiring correction, an explicit limitation, or an unresolved registration.
- `result.json`: calculation, checks, analysis, decisions, evidence and downstream data.
- `document.json`: complete authoritative machine semantics for downstream selection.
- `report.md`: deterministic financial consulting core only: calculation basis, key metrics, financial analysis, decisions, risks and required inputs. It is not a complete project report.

## Final response

State the selected run number, result summary, and output paths. List every remaining input warning and material unresolved limitation, even when build, quality, charts, and Word QA pass. Never let “build passed” imply that project evidence or input assumptions are complete.

For command exit meanings and output contract, use `docs/contract-surface.md`. For current implementation limits, use `docs/boundary.md`; do not present probability/Monte Carlo analysis or a complete statutory VfM study as available. Operating-period debt is limited to loans bound to same-year capital assets; mixed-use long-term-asset VAT requires an explicit tax-workpaper schedule.
