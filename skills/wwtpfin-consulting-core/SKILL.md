---
name: wwtpfin-consulting-core
description: >-
  Convert wastewater-treatment project materials into verified structured financial consulting
  semantics with wwtp-fin, then hand the deliverable to DocxKit and ChartKit. Use for污水处理财务测算、
  特许经营财务评价、BOT/TOT/ROT/BOOT/DBFOT/O&M 项目咨询内容包、财务可行性与项目材料转化。
---

# wwtp-fin Consulting Core

Use `wwtp-fin` as a professional calculation and decision workspace. The agent interprets sources, finds measures, proposes methods and explains tradeoffs; the CLI calculates, checks numerical consistency and comparability, and binds evidence, decisions and results. A passed check does not certify source meaning, policy eligibility, exhaustive research or global optimality.

The user supplies materials, goals and feedback. Within one continuing case, actively research, calculate and improve the advice before asking for a choice. Do not require financial expertise, policy names or another fresh session from the user. A stronger agent may discover better methods or new measures; the workflow must preserve and explain that progress.

## Start or resume

- Resolve the active CLI's asset root: the source checkout when developing, otherwise the active `@dztabel/wwtpfin` installation. Use its skills, schemas, docs and examples together; a same-name global skill may be stale. Relative documentation paths below are under that root.
- Create or reuse a case workspace; copy originals into `sources/`. Use [workspace management](references/workspace.md) for current input, immutable rounds and exports. Run `case status` on resumption and before presenting a current result.
- Read command help and relevant schemas when constructing inputs; consult the matching reference for a specific modeling or review issue. `examples/minimal_complete/` and `examples/three_stage/` show shapes, not project facts or recommended assumptions.

## Three reversible stages

| Stage | Work and output | Tool path |
|---|---|---|
| Establish a starting point | Source meanings, conflicts, supported estimates and a calculable baseline; a decision contract expressing the user's actual cost goal and boundaries. Discuss important interpretations and opportunities. | `intake`, then `build`; [conversion discipline](references/conversion-discipline.md), `docs/INTAKE.md`, `docs/COST_PERSPECTIVES.md` |
| Research and improve | Discover measures, calculate actual combinations and uncertain conditions, explain alternatives and support a recommendation. | `solve`, `sensitivity`, `compare`; [modeling and iteration](references/modeling-iteration.md) |
| Fix the selected plan | Record the user's concrete choice, fully recompute and verify, then hand off the exact run. Preserve pending conditions for a selected conditional study. | Bundled `scripts/record-selection.py`, `finalize`, `verify-final-run --case`; [workspace management](references/workspace.md), `docs/CASE_WORKFLOW.md` |

New facts, goals or methods return to the relevant stage. Record actual user requests and reasons; update the current artifact while retaining history. The product handles version binding, not an assumption that the last or highest-numbered run is selected.

## Professional judgments the tools cannot make

1. **Meaning before mapping.** Retain scope, period, units, tax basis and qualifiers. Design capacity is not annual average demand; a total may include a listed subset; an accounting amount need not be a cash payment. Tie conclusions to the exact source passage and explain normalization.
2. **Facts, estimates and proposals have different roles.** A forecast in a report remains an estimate. Missing workbooks do not block an authorized, supported estimate. State its method and uncertainty; do not convert the first trial value into a user-fixed boundary. Conflicts remain visible.
3. **Clarify the cost goal.** Construction and operating total cost, project cash cost and a payer's expenditure answer different questions. Use the appropriate scope and common service period; do not substitute the lowest starting tariff. Explain primary/secondary objectives and any tolerance before using them to recommend.
4. **Research is open.** Service, investment/renewal, operations, tax/support, financing/payment and delivery are coverage prompts, not a closed menu. Read the CLI's model-derived study items, then investigate additional relevant opportunities. A label or completed form is not evidence that the work was sufficient.
5. **Connect a measure to an action.** Establish source → project applicability → action → parameter change → cost and responsible party. Read full policy provisions and exceptions. Challenge exclusions that could change the decision. A sensitivity result does not prove an engineering measure achievable.
6. **Recompute combinations and meaningful uncertainty.** Do not add isolated savings or borrow a fallback's savings from another combination. Test competing plausible methods where they matter; a percentage around one method does not test another method. When a ranking reverses, explain the condition or required evidence.
7. **Separate cash feasibility from implementation.** Read the period cash-source/use ledger and `financing_review`. A cumulative deficit is real within the stated assumptions; a separate payer budget does not fund it. A low period DSCR with accumulated cash available requires financing terms and cash-availability analysis, not a claim that the bank will approve or reject.
8. **Own the recommendation.** Use `decision-brief.md/json` as the numerical backbone. Read research/decision issues and `ranking_explanation`: a winner selected within tolerance may cost more on the primary measure. Explain why that tradeoff is appropriate; never call a rule-dependent result universally best. Conditional assumptions and implementation readiness remain distinct.

## Efficient tool use

- `parameter_basis` binds the values and methods actually used. Reuse unchanged baseline bases; bind changed candidate values through `candidate_bases`. Do not rewrite evidence merely to make a changed input pass. See `docs/RESEARCH_REVIEW.md` for exact fields.
- If the intended pricing method is the supported shared cash-floor rule, register `research.pricing_rules` and use `price-schemes` once. It generates separate parameter/scheme drafts and price deltas with the existing solver. Inspect changes and affected evidence, then `compare`; do not write a duplicate candidate-by-scenario solver loop. A cash floor is not an investor-return price or a default commercial objective. Use `solve` or explicit proposals for other methods.
- Fix reported numerical or binding issues at their actual source. Pure display metadata does not need financial variants, and `material` is optional descriptive metadata rather than permission to skip an actual estimate. `unassessed_domain_prompts` are investigative prompts; they do not force fake candidates.
- Calculate freely within authorized research. Batch questions only for missing information that blocks useful progress. If the model cannot represent a mechanism, state that specific limitation and its consequence; an upstream engineering workpaper may supply inputs but cannot impersonate completed CLI finance.

```bash
wwtp-fin intake -p input/project-draft.yaml -o input/intake-advice.json
wwtp-fin price-schemes -p input/project.yaml --schemes comparisons/compare-0001/scheme-set.yaml -o comparisons/pricing-0001
wwtp-fin compare -p input/project.yaml --contract input/decision-contract.yaml --evidence input/evidence.json --schemes comparisons/compare-0001/scheme-set.yaml -o comparisons/compare-0001/output
```

After calculation, read `quality.json`, `warnings.json`, checks and the applicable reviews; run `verify-deliverable` or `verify-final-run` for the artifact type. Respond with the recommendation and reasons, baseline/cost scope, assumptions that could change it, outstanding limitations, current run and paths. A successfully built package is not proof of a verified business premise.

For fractional periods use `docs/TIME_AXIS.md`; for different contract lengths and complete continuation service use `docs/COST_PERSPECTIVES.md`. For unsupported capabilities and exit statuses use `docs/boundary.md` and `docs/contract-surface.md`. Export Word or charts only when requested, from the verified run through [downstream handoff](references/handoff.md) and the report skill.
