# Modeling, measures and selected results

## Stage 1: establish the starting point

Create `input/modeling-decisions.md`. Separate source facts and mandatory rules, design choices, negotiable arrangements, bounded estimates/scenarios and missing information. Record the source locator, evidence state, current value, supported alternatives and decision owner. A preliminary study is a starting point; its proposed numbers are not automatically fixed facts.

When the materials contain a source calculation, retain it as `baseline_status=source_declared_baseline`. If there is no complete source model, create an authorized conditional research baseline from known facts, supported estimates and proposed design choices. Preserve the source gaps; do not require a nonexistent source model to run first. Any estimate or correction changes the basis and requires a new, clearly labelled run.

Create `input/decision-contract.yaml` using `wwtp-fin schema --kind decision-contract`. Record the objective metric/direction and its basis, cost perspective, unit, included/excluded cash flows, service boundary, comparison period and discount basis. Record numeric hard constraints and fixed parameter paths using canonical `Params` values, plus required implementation conditions and responsible parties. Do not equate a service tariff with total cost when subsidy, volume, period or service changes. Do not equate fiscal collection/transfer with fiscal net expenditure. First check the existing cost metrics and input mappings. If the exact requested scope is unsupported, document the missing mechanism; a separately verified workpaper can explain a bound, but is not a completed CLI comparison or selected deliverable. Do not invent CLI schema names or metrics for such workpapers, and never relabel a different metric.

Do not require all decisions before useful work can begin. Within an authorized exploration, construct transparent estimates from engineering quantities, applicable quotas, regional prices, quotations or explicit proposal ranges. Record region, edition/date, units, taxes, uncertainty and replacement evidence. Missing workbooks need not block this work. Keep missing facts unresolved; do not infer lending commitments or tax eligibility.

## Stage 2: discover measures, calculate and improve combinations

Diagnose the baseline, then connect every proposed measure through:

**Effective source → project applicability → real action → linked parameter changes → financial impact → cost/responsibility/implementation conditions.**

Sources can be policy, contract alternatives, engineering studies, quotations or cost estimates. A numerical sensitivity boundary does not prove a measure achievable. Policy existence does not prove project eligibility. An open measure register is a working aid, not a finite product capability list.

- **Representable:** build a supported scenario and calculate it.
- **Needs upstream calculation:** calculate the engineering/tax workpaper with sources before mapping the result.
- **Approximation or bound:** explain what the calculation can decide and what it cannot; retain pending conditions.
- **Unrepresentable:** register the exact unsupported mechanism and affected results; do not imitate it with a different cash flow.

Use `sensitivity` and `solve` to identify influential variables and boundaries. `solve` currently supports transfer consideration, blended tariff and operating duration (a month grid when time_basis is provided); other choices use explicitly constructed scenarios. CLI does not automatically select a plan or establish a “best” scheme.

Do not request permission again for individual trials within already authorized exploration. Present concrete choices after calculating them. If no source-backed alternative exists, record `no_source_backed_candidates` and investigate or request the missing evidence rather than inventing a candidate.

For every comparison, pass the same decision contract and exact evidence snapshot. The contract's hard constraints are inherited even if absent from the scheme set. Changing the objective or fixed boundary requires revising the contract and restarting comparison on that basis. Condition entries use `pending`, `satisfied` or `not_applicable`; satisfied/not-applicable entries require actual references and an explanation, not a trial result. Their status is a responsible-party declaration, not independent CLI legal/technical certification.

Read the complete constraints, fixed-parameter changes, comparability, `model_limits` and conditions, not only `shortlist`. `numerically_feasible` covers numerical and fixed-boundary checks; `feasible` also requires comparable cost/payment scope. `selectable_shortlist` additionally requires no unresolved model limits and recorded implementation conditions. A successful command or complete deliverable is not project approval. Empty selectable results require further iteration or condition resolution.

Use `docs/FUNDING_STRUCTURE.md` to declare construction-grant allocation, debt/equity bases and engineering-backed operating-capex purpose. Never infer expansion from a favorable DSCR result. Check all capital outflows and cash gaps even when a DSCR basis excludes expansion. A grant used to reduce borrowing or equity cannot also be counted as shareholder income. Where a minimum equity share applies, constrain `construction_equity_ratio_actual`, not just the proposed input ratio. Classifications, grant use and financing may be conditional proposals; preserve their evidence state. Legacy reproduction with material unresolved funding or investment scope cannot be selected for finalization.

Use `docs/COST_PERSPECTIVES.md` to choose investment/operating outlay, project cash cost, service/grant payments or an explicitly scoped payer net outflow. Keep nominal and present values separate. Missing payer receipts are unknown: use partial coverage and a source-backed conditional scenario, not zero receipts disguised as fiscal net burden. Compare new measures against the same baseline and discount/service scope; an invalid starting-price proxy must be replaced by a complete payment metric. Inspect the per-period ledger and investment VAT basis before interpreting savings.

Keep declared `dscr_min`, cash-generation `cash_dscr_min` and `cum_cash_min` separate. The cash ratio excludes book grant income and new financing, deducts sustaining investment and working-capital injections, and includes all modeled debt service. A sub-1 period calls for analysis of opening cash, financing and risk margin; it is not an automatic bank rejection. Inspect `dscr_cash_bridge` and `capital.cash_debt_service` for scope and unavailable reasons. Use `solve` and a decision-contract constraint when cash coverage is required, with an explicitly justified threshold rather than assuming a universal lender minimum. Income-tax exclusion of a VAT refund does not remove its accounting income; tax eligibility remains a separate condition.

Recompute each complete combination; never add independent savings as the combination value. Test uncertainties that can change the decision, especially volume, investment/operating cost and conditional preferences. Organize a small set of complete plans for the client, with common baseline, whole-life effects, financing/cash closure, responsibilities and the fallback if a material condition fails. Reasoned recommendations are allowed within this evaluated set; the user chooses.

## Stage 3: explicit selection and complete calculation

Keep `decision_status=user_confirmation_required` until a choice is actually made. Only after explicit confirmation, record a selection using `scheme-selection`: exact comparison content hash, candidate ID, canonical parameter hash, confirmation identity/time/reference and purpose. Use the bundled [selection-record helper](../scripts/record-selection.py) to bind these values without transcribing hashes. Do not hand-copy rounded prices into the selected input.

`purpose=workflow_validation` is mandatory for synthetic/simulated acceptance; never represent it as a real client decision. `purpose=selected_scheme` records an actual decision. These records bind content; they do not authenticate the human or replace the referenced confirmation.

```bash
wwtp-fin compare -p input/project.yaml --contract input/decision-contract.yaml --evidence input/evidence.json --schemes comparisons/compare-0001/scheme-set.yaml -o comparisons/compare-0001/output
wwtp-fin finalize --comparison comparisons/compare-0001/output/scheme-comparison.json --selection selections/selection-NNNN.json --contract input/decision-contract.yaml --evidence input/evidence.json -o runs/run-NNNN
wwtp-fin verify-final-run runs/run-NNNN
```

`finalize` rechecks the contract, evidence, software, full parameters, numerical constraints and implementation-condition records, then runs the existing complete calculation/build chain. Changed inputs, evidence, software or decisions require a new comparison and confirmation. Failed runs remain staging; successful runs are immutable.

The selected run is the sole financial source for exports. New evidence discovered during report writing that affects a calculation returns to modeling/iteration. Never choose the newest trial as the final run. A client can request a report of an explicitly identified baseline or conditional run; clearly label that purpose and preserve its limitations.

## 非整年项目

建设与运营实际期限按原文分别登记，不能向上取整。先读取包内 `docs/TIME_AXIS.md`；声明项目开始月份、期间金额口径和依据，按时间轴的分期数转换数组。开始月份缺失时可登记条件提案并试算，不能标作原始事实。期限改变后须重新核对水量爬坡、设备/融资/拨付事件及显式金额覆盖，不能把旧年度数组当作已转换。确认成果包含实际期间表，并复核总期限、首末期收支和折现时点。
