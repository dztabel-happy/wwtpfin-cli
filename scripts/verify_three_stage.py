#!/usr/bin/env python3
"""Run synthetic workflow acceptance against an installed CLI, without core imports."""
import argparse
from copy import deepcopy
import json
import shutil
from pathlib import Path
import subprocess
import sys


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cli", type=Path, required=True)
    parser.add_argument("--assets", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    cli, assets, out = args.cli.resolve(), args.assets.resolve(), args.output.resolve()
    out.mkdir(parents=True, exist_ok=True)
    if any(out.iterdir()):
        parser.error("output must be empty")
    evidence = assets / "examples/minimal_complete/evidence.json"
    contract = assets / "examples/three_stage/decision-contract.yaml"

    def run(*parts, expect=0, error_contains=None):
        command = [str(cli), *map(str, parts)]
        # Windows npm launchers are .cmd; execute the shipped Node wrapper directly.
        if cli.suffix == ".cmd":
            wrapper = cli.parent.parent / "@dztabel/wwtpfin/npm/wwtp-fin.cjs"
            command = ["node", str(wrapper), *map(str, parts)]
        result = subprocess.run(command, cwd=out, capture_output=True, text=True,
                                encoding="utf-8")
        if result.returncode != expect:
            raise RuntimeError(f"{command[1]}: expected {expect}, got {result.returncode}\n"
                               + result.stdout + result.stderr)
        if error_contains is not None:
            assert error_contains in result.stderr, result.stderr
        return result.stdout

    run("compare", "-p", assets / "examples/minimal_complete/project.yaml",
        "--evidence", evidence, "--contract", contract,
        "--schemes", assets / "examples/three_stage/scheme-set.yaml", "-o", out / "comparison")
    comparison = out / "comparison/scheme-comparison.json"
    data = json.loads(comparison.read_text(encoding="utf-8"))
    rows = {row["id"]: row for row in data["candidates"]}
    assert not rows["cash_gap"]["numerically_feasible"]
    assert rows["conditional"]["readiness"] == "conditions_pending"
    assert data["selectable_shortlist"] == ["complete"]
    helper = assets / "skills/wwtpfin-consulting-core/scripts/record-selection.py"
    subprocess.run([sys.executable, str(helper), str(comparison), "complete",
                    str(out / "selection.json"), "--confirmed-by", "synthetic acceptance",
                    "--confirmed-at", "2026-09-11", "--reference", "synthetic://acceptance",
                    "--purpose", "workflow_validation"], check=True, capture_output=True)
    selection = out / "selection.json"
    final = out / "run-0001"
    run("finalize", "--comparison", comparison, "--selection", selection,
        "--contract", contract, "--evidence", evidence, "-o", final)
    run("verify-final-run", final)
    payload = json.loads((final / "deliverable/result.json").read_text(encoding="utf-8"))
    assert payload["selected_scheme"]["selection"]["purpose"] == "workflow_validation"
    assert payload["params"] == rows["complete"]["resolved_params"]
    assert payload["tables"] and "decision_boundaries" in payload["analysis"]
    assert payload["costs"]["schema"] == "wwtp-fin/cost-perspectives/1"
    assert payload["scalars"]["payer_net_outflow_wan"] is None
    run("finalize", "--comparison", comparison, "--selection", selection,
        "--contract", contract, "--evidence", evidence, "-o", final, expect=1)

    # Selecting conditional assumptions preserves pending implementation facts.
    research_selection = out / "research-selection.json"
    research_command = [sys.executable, str(helper), str(comparison), "conditional",
        str(research_selection), "--confirmed-by", "synthetic acceptance",
        "--confirmed-at", "2026-09-14", "--reference", "synthetic://conditional-assumptions",
        "--purpose", "workflow_validation"]
    assert subprocess.run(research_command, capture_output=True).returncode == 2
    assert not research_selection.exists()
    subprocess.run(research_command + ["--selection-scope", "conditional_research"],
                   check=True, capture_output=True)
    research_final = out / "research-final"
    run("finalize", "--comparison", comparison, "--selection", research_selection,
        "--contract", contract, "--evidence", evidence, "-o", research_final)
    run("verify-final-run", research_final)
    research = json.loads((research_final / "deliverable/result.json").read_text(encoding="utf-8"))
    assert research["params"] == rows["conditional"]["resolved_params"]
    assert research["selected_scheme"]["conditions"] == rows["conditional"]["conditions"]
    assert any(c["status"] == "pending" for c in research["selected_scheme"]["conditions"])
    research_report = (research_final / "deliverable/report.md").read_text(encoding="utf-8")
    assert "条件研究选定成果" in research_report
    assert "模拟流程验收成果，不代表真实甲方确认" in research_report
    failed_research = research_command.copy()
    failed_research[3] = "cash_gap"
    failed_research[4] = str(out / "failed-research-selection.json")
    assert subprocess.run(failed_research + ["--selection-scope", "conditional_research"],
                          capture_output=True).returncode == 2

    def save(name, value):
        path = out / name
        path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")
        return path

    # A mapping must not become annual increments by iterating its numeric keys.
    malformed = deepcopy(payload["params"])
    malformed["tariff_escalation"] = {"2": .25}
    malformed["calculation_basis"]["tariff_adjustment"] = "annual_increment_schedule"
    malformed_out = out / "invalid-tariff-array"
    run("run", "-p", save("invalid-tariff-array.json", malformed),
        "--no-sensitivity", "--no-boundaries", "-o", malformed_out,
        expect=1, error_contains="tariff_escalation 必须是数值数组")
    assert not malformed_out.exists()

    params = deepcopy(payload["params"])
    construction = params["capital"]["construction_years"]
    periods = 1 + construction + params["concession_years"]
    params["payer_cashflow"] = {
        "entity": "合成付费主体", "scope": "服务费、补助、另列代收收入", "basis": "合成验收",
        "coverage": "complete", "evidence_refs": ["synthetic://payer"],
        "service_payment_share": 1, "capital_grant_payment_share": 1, "terminal_payment_share": 0,
        "other_cashflows": [{"id": "collection", "label": "代收收入", "direction": "inflow",
            "amounts_wan": [0] * (1 + construction) + [50] * params["concession_years"],
            "basis": "合成固定收款", "evidence_refs": ["synthetic://receipt"]}]}
    payer_params = save("payer-project.json", params)
    run("run", "-p", payer_params, "--no-sensitivity", "--no-boundaries", "--compact", "-o", out / "payer")
    payer_result = json.loads((out / "payer/run.json").read_text(encoding="utf-8"))
    totals = payer_result["scalars"]
    assert abs(totals["payer_net_outflow_wan"] - totals["service_grant_payment_wan"]
               + 50 * params["concession_years"]) < 1e-7
    assert len(payer_result["costs"]["payer"]["known_net_outflow_wan"]) == periods
    params["payer_cashflow"]["coverage"] = "partial"
    run("run", "-p", save("payer-partial.json", params), "--no-sensitivity", "--no-boundaries",
        "--compact", "-o", out / "partial")
    assert json.loads((out / "partial/run.json").read_text(encoding="utf-8"))["scalars"]["payer_net_outflow_wan"] is None

    # A lower tariff funded by a larger grant is more expensive at the common payer scope.
    changed_contract = deepcopy(data["decision_contract"])
    objective = {"metric": "payer_net_outflow_wan", "direction": "min", "basis": "合成收支范围内净支付"}
    changed_contract["objective"] = objective
    changed_contract["comparison_basis"].update(unit="万元", scope="服务费、补助减另列代收收入")
    candidates = [deepcopy(next(c for c in data["scheme_set"]["candidates"] if c["id"] == "complete"))]
    candidates[0].update(id="maintain", overrides={})
    candidates.append(deepcopy(candidates[0]))
    candidates[1].update(id="lower_price", name="单价降低且补助增加", overrides={
        "tariff_blended_gross": payload["params"]["tariff_blended_gross"] - .01,
        "capital": {"funding": {"grant_use_wan": [1000, 0], "debt_ratio_basis": "total_investment",
                                 "evidence_refs": ["synthetic://grant-use"]}},
        "capital_grants": {"recognition": "deferred_income", "output_vat_rate": 0,
            "tranches": [{"period_index": 1, "amount_wan": 1000}],
            "pools": [{"pool_id": "support", "trigger_period_index": 1,
                       "start_period_index": 3, "amortisation_years": 25}]}})
    changed_spec = {"schema": "wwtp-fin/scheme-set/1", "include_base": False,
                    "objective": objective, "hard_constraints": [], "candidates": candidates}
    run("compare", "-p", payer_params, "--contract", save("cost-contract.json", changed_contract),
        "--evidence", evidence, "--schemes", save("cost-schemes.json", changed_spec), "-o", out / "cost-comparison")
    costs = json.loads((out / "cost-comparison/scheme-comparison.json").read_text(encoding="utf-8"))
    assert costs["selectable_shortlist"] == ["maintain", "lower_price"]
    assert abs(costs["candidates"][1]["objective_value"] - costs["candidates"][0]["objective_value"] - 745.4125) < 1e-7
    subprocess.run([sys.executable, str(helper), str(out / "cost-comparison/scheme-comparison.json"),
                    "lower_price", str(out / "cost-selection.json"), "--confirmed-by", "synthetic acceptance",
                    "--confirmed-at", "2026-09-11", "--reference", "synthetic://payer",
                    "--purpose", "workflow_validation"], check=True, capture_output=True)
    run("finalize", "--comparison", out / "cost-comparison/scheme-comparison.json",
        "--selection", out / "cost-selection.json", "--contract", out / "cost-contract.json",
        "--evidence", evidence, "-o", out / "cost-final")
    run("verify-final-run", out / "cost-final")
    cost_final = json.loads((out / "cost-final/deliverable/result.json").read_text(encoding="utf-8"))
    assert cost_final["scalars"]["payer_net_outflow_wan"] == costs["candidates"][1]["objective_value"]
    assert "payer_cashflows" in cost_final["tables"]
    assert "construction_funding" in cost_final["tables"]
    assert cost_final["capital"]["grant_use_wan"] == [1000, 0]
    assert abs(sum(cost_final["capital"]["investment"]) - sum(cost_final["capital"]["debt_draw"])
               - sum(cost_final["capital"]["equity_draw"]) - 1000) < 1e-7
    changed_spec["objective"] = data["objective"]
    run("compare", "-p", payer_params, "--contract", contract, "--evidence", evidence,
        "--schemes", save("proxy-schemes.json", changed_spec), "-o", out / "proxy")
    proxy = json.loads((out / "proxy/scheme-comparison.json").read_text(encoding="utf-8"))
    assert proxy["candidates"][1]["readiness"] == "not_comparable"

    capex_results = {}
    for purpose in ("sustaining", "expansion"):
        for funded in (False, True):
            trial = deepcopy(payload["params"])
            trial["calculation_basis"]["dscr"] = "ebitda_minus_tax_minus_sustaining_capex_over_pd"
            trial["capital"]["replacement_assets"] = [{"name": "运营资产", "operation_year": 3,
                "cost_wan": 12000, "life_years": 20, "residual_rate": 0,
                "kind": "fixed_asset", "depreciable": True, "vat_basis": "tax_inclusive_no_credit",
                "purpose": purpose, "purpose_basis": "synthetic://engineering-scope"}]
            if funded:
                trial["operating_loan_tranches"] = [{"name": "专项贷款", "draw_operation_year": 3,
                    "linked_asset_name": "运营资产", "amount_wan": 12000, "annual_rate": .03,
                    "term_years": 20, "grace_years": 1, "repayment_method": "annuity"}]
            name = purpose + ("-funded" if funded else "-unfunded")
            run("run", "-p", save(name + ".json", trial), "--no-sensitivity", "--no-boundaries",
                "--compact", "-o", out / name)
            capex_results[purpose, funded] = json.loads((out / name / "run.json").read_text(encoding="utf-8"))
    for funded in (False, True):
        a, b = [capex_results[purpose, funded] for purpose in ("sustaining", "expansion")]
        assert a["series"]["CUM_CASH"] == b["series"]["CUM_CASH"]
        assert a["scalars"]["dscr_min"] < 1 < b["scalars"]["dscr_min"]
        assert (b["scalars"]["cum_cash_min"] >= 0) == funded
    # A separate cash example: 100 annual receipts, 200 principal repayments,
    # and 200 non-cash grant income. Book DSCR 1.5 must not pass a cash constraint.
    trial = deepcopy(payload["params"])
    trial.update(concession_years=10, design_capacity_m3d=10000, days_per_year=365,
        vol_segments=[{"year_from": 1, "year_to": 10, "m3d": 10000}],
        tariff_blended_gross=100/365, opex_items=[], operating_loan_tranches=[],
        loan_tranches=[], loan_rate=0, loan_term_years=5, loan_grace_years=0,
        loan_repayment_method="equal_principal", debt_ratio=.5, equity_ratio=.5,
        vat_output_rate=0, vat_relief="none", vat_credit_begin_wan=0, income_tax_rate=0,
        cit_mode="standard", term_comparison_years=[], financial_benchmarks=[])
    trial["capital"] = {"construction_years": 1, "capex_schedule_wan": [3000],
        "capex_components_wan": {"工程": 3000}, "capitalize_interest": True,
        "capex_vat_basis": "tax_inclusive_no_credit",
        "assets": [{"name": "工程", "cost_wan": 3000, "life_years": 10, "residual_rate": 0,
            "kind": "fixed_asset", "depreciable": True, "investment_origin": "construction"}],
        "replacement_assets": [], "funding": {"grant_use_wan": [1000],
            "debt_ratio_basis": "after_grant", "evidence_refs": ["synthetic://cash"]}}
    trial["capital_grants"] = {"recognition": "deferred_income", "output_vat_rate": 0,
        "tranches": [{"period_index": 1, "amount_wan": 1000}],
        "pools": [{"pool_id": "initial", "trigger_period_index": 1,
            "start_period_index": 2, "amortisation_years": 5}]}
    cash_params = save("cash-project.json", trial)
    cash_contract = deepcopy(data["decision_contract"])
    cash_contract["fixed_parameters"] = {"concession_years": 10}
    cash_contract["hard_constraints"] = [{"metric": "cash_dscr_min", "op": ">=",
        "value": 1, "basis": "合成验收：检验当期现金覆盖，不是银行要求"}]
    cash_spec = deepcopy(changed_spec)
    cash_spec["candidates"] = []
    for pid, price in [("book_pass", 100/365), ("cash_pass", .55)]:
        row = deepcopy(candidates[0])
        row.update(id=pid, name=pid, overrides={"tariff_blended_gross": price})
        cash_spec["candidates"].append(row)
    run("compare", "-p", cash_params, "--contract", save("cash-contract.json", cash_contract),
        "--evidence", evidence, "--schemes", save("cash-schemes.json", cash_spec),
        "-o", out / "cash-comparison")
    cash_comparison = out / "cash-comparison/scheme-comparison.json"
    cash = json.loads(cash_comparison.read_text(encoding="utf-8"))
    assert cash["selectable_shortlist"] == ["cash_pass"]
    bad = cash["candidates"][0]
    assert abs(bad["metrics"]["dscr_min"] - 1.5) < 1e-9
    assert abs(bad["metrics"]["cash_dscr_min"] - .5) < 1e-9
    run("solve", "-p", cash_params, "--var", "tariff_blended_gross", "--target", "cash_dscr_min",
        "--value", 1, "-o", out / "cash-solve")
    solved = json.loads((out / "cash-solve/solve.json").read_text(encoding="utf-8"))
    assert solved["converged"] and abs(solved["solution"] - 200/365) < 1e-7
    subprocess.run([sys.executable, str(helper), str(cash_comparison), "cash_pass",
        str(out / "cash-selection.json"), "--confirmed-by", "synthetic acceptance",
        "--confirmed-at", "2026-09-11", "--reference", "synthetic://cash",
        "--purpose", "workflow_validation"], check=True, capture_output=True)
    run("finalize", "--comparison", cash_comparison, "--selection", out / "cash-selection.json",
        "--contract", out / "cash-contract.json", "--evidence", evidence, "-o", out / "cash-final")
    run("verify-final-run", out / "cash-final")
    cash_final = json.loads((out / "cash-final/deliverable/result.json").read_text(encoding="utf-8"))
    assert cash_final["scalars"]["cash_dscr_min"] >= 1
    assert cash_final["capital"]["cash_debt_service"]["status"] == "computed"
    assert "dscr_cash_bridge" in cash_final["tables"]
    assert all(abs(v - 200.75) < 1e-8 for v in cash_final["series"]["CASH_DEBT_AVAILABLE"])
    trial.update(tariff_blended_gross=1, income_tax_rate=.25, vat_output_rate=.06,
                 vat_relief="refund70", vat_refund_ratio=.7, vat_refund_taxable=False)
    run("run", "-p", save("refund-tax-base.json", trial), "--no-sensitivity", "--no-boundaries",
        "--compact", "-o", out / "refund-tax-base")
    refund = json.loads((out / "refund-tax-base/run.json").read_text(encoding="utf-8"))["series"]
    assert refund["OTHER_INCOME"] == refund["VAT_REFUND"]
    assert abs(refund["TAX_BASE_LEVERED"][0] - refund["PBT"][0] + 365/1.06*.06*.7) < 1e-8
    assert max(map(abs, refund["BS_RESIDUAL"])) < 1e-8
    # Fractional durations must survive the actual shipped CLI and selected-run path.
    trial = deepcopy(payload["params"])
    trial["concession_years"] = 24.5
    trial["time_basis"] = {"project_start_month": 1, "annual_amounts_basis": "period_totals",
                           "evidence_refs": ["synthetic://half-year-periods"]}
    trial["capital"]["construction_years"] = 1.5
    for asset in trial["capital"]["assets"]:
        asset["life_years"] = 24.5
    fractional_contract = deepcopy(data["decision_contract"])
    fractional_contract["fixed_parameters"] = {"concession_years": 24.5}
    fractional_spec = deepcopy(data["scheme_set"])
    complete = deepcopy(next(c for c in fractional_spec["candidates"] if c["id"] == "complete"))
    complete["overrides"] = {}
    fractional_spec.update(include_base=False, candidates=[complete])
    run("compare", "-p", save("fractional-project.json", trial),
        "--contract", save("fractional-contract.json", fractional_contract),
        "--schemes", save("fractional-schemes.json", fractional_spec), "--evidence", evidence,
        "-o", out / "fractional-comparison")
    fractional_comparison = out / "fractional-comparison/scheme-comparison.json"
    compared = json.loads(fractional_comparison.read_text(encoding="utf-8"))
    assert compared["selectable_shortlist"] == ["complete"]
    subprocess.run([sys.executable, str(helper), str(fractional_comparison), "complete",
        str(out / "fractional-selection.json"), "--confirmed-by", "synthetic acceptance",
        "--confirmed-at", "2026-09-12", "--reference", "synthetic://half-year-periods",
        "--purpose", "workflow_validation"], check=True, capture_output=True)
    run("finalize", "--comparison", fractional_comparison,
        "--selection", out / "fractional-selection.json", "--contract", out / "fractional-contract.json",
        "--evidence", evidence, "-o", out / "fractional-final")
    run("verify-final-run", out / "fractional-final")
    fractional = json.loads((out / "fractional-final/deliverable/result.json").read_text(encoding="utf-8"))
    axis, series = fractional["period"]["time_axis"], fractional["series"]
    assert axis["construction_period_years"] == [1, .5]
    assert axis["operation_period_years"] == [.5] + [1] * 24
    assert axis["cashflow_times_years"] == [0, 1, 1.5] + list(range(2, 27))
    assert "time_axis" in fractional["tables"]
    expected_volume = trial["vol_segments"][0]["m3d"] * trial["days_per_year"] / 2
    assert abs(series["VOL_TREATED_M3Y"][0] - expected_volume) < 1e-7
    actual_npv = sum(v / (1 + trial["discount_rate"]) ** t for v, t in
                     zip(series["CF_TIMED_TOTAL_AFTERTAX"], axis["cashflow_times_years"]))
    assert abs(fractional["scalars"]["npv_total_aftertax"] - actual_npv) < 1e-7
    # A current case must not silently deliver a historically valid obsolete plan.
    case = out / "current-case"
    inputs = case / "input"
    inputs.mkdir(parents=True)
    current_params = deepcopy(data["base_params"])
    save("current-case/input/project.json", current_params)
    save("current-case/input/evidence.json", json.loads(evidence.read_text(encoding="utf-8")))
    save("current-case/input/decision-contract.json", data["decision_contract"])
    old_comparison = case / "comparisons/first/scheme-comparison.json"
    spec_path = save("current-case/input/scheme-set.json", data["scheme_set"])
    run("compare", "-p", "current-case/input/project.json", "--evidence", inputs / "evidence.json",
        "--contract", inputs / "decision-contract.json", "--schemes", spec_path,
        "-o", old_comparison.parent)
    assert json.loads(old_comparison.read_text(encoding="utf-8"))["base_source"] == str(inputs / "project.json")
    selection = out / "current-case-selection.json"
    subprocess.run([sys.executable, str(helper), str(old_comparison), "complete", str(selection),
        "--confirmed-by", "synthetic acceptance", "--confirmed-at", "2026-09-14",
        "--reference", "synthetic://current-case", "--purpose", "workflow_validation"],
        check=True, capture_output=True)
    message, response = case / "user.md", case / "response.md"
    message.write_text("请比较现有条件下的方案。", encoding="utf-8")
    response.write_text("本轮比较及完整约束已检查；保留选择理由。", encoding="utf-8")
    run("case", "checkpoint", case, "--stage", 2, "--message", message,
        "--response", response, "--kind", "comparison", "--artifact", old_comparison,
        "--schemes", spec_path)
    assert json.loads(run("case", "status", case))["state"] == "current"
    message.write_text("确认现有 complete 候选，请完整重算；仅为模拟验收。", encoding="utf-8")
    response.write_text("已收到选择，绑定当前比较并开始完整重算。", encoding="utf-8")
    run("case", "checkpoint", case, "--stage", 3, "--message", message,
        "--response", response, "--kind", "comparison", "--artifact", old_comparison,
        "--schemes", spec_path)
    selected = case / "runs/selected"
    run("finalize", "--comparison", old_comparison, "--selection", selection,
        "--contract", inputs / "decision-contract.json", "--evidence", inputs / "evidence.json",
        "-o", selected)
    run("case", "checkpoint", case, "--stage", 3, "--message", message,
        "--response", response, "--kind", "selected", "--artifact", selected)
    run("verify-final-run", selected, "--case", case)
    report_scripts = assets / "skills/wwtpfin-consulting-report/scripts"

    def report_tool(script, *parts, expect=0):
        result = subprocess.run([sys.executable, str(report_scripts / script),
            *map(str, parts), "--cli", str(cli)], capture_output=True, text=True, encoding="utf-8")
        if result.returncode != expect:
            raise RuntimeError(f"{script}: expected {expect}, got {result.returncode}\n"
                               + result.stdout + result.stderr)
        return result.stdout + result.stderr

    report_plan = out / "current-report-plan.json"
    report_tool("init_report_plan.py", selected / "deliverable", report_plan,
                "--source-run", selected.name, "--case", case)
    plan = json.loads(report_plan.read_text(encoding="utf-8"))
    assert "模拟流程验收" in plan["required_notice"]
    # Resolve content routing so a later failure isolates source currentness.
    for section in ("modules", "blocks", "warnings", "unresolved"):
        for item in plan[section]:
            item["disposition"] = "body"
    for item in plan["tables"]:
        if item["report_role"] == "body":
            item["section"] = "财务评价"
        elif item["report_role"] == "appendix":
            item.update(disposition="appendix", section="财务附表", reason="合成验收复核")
    for item in plan["figures"]:
        item.update(disposition="not_applicable", reason="本轮仅验证报告来源，不渲染")
    report_plan.write_text(json.dumps(plan, ensure_ascii=False), encoding="utf-8")
    report_tool("check_report_plan.py", selected / "deliverable", report_plan)
    current_params["opex_items"][0]["base_wan"] *= 10
    save("current-case/input/project.json", current_params)
    stale = json.loads(run("case", "status", case))
    assert stale["state"] == "needs_update" and stale["current_artifact"] is None
    run("verify-final-run", selected)  # historical package remains intact
    run("verify-final-run", selected, "--case", case, expect=1)
    assert "报告来源校验失败" in report_tool(
        "check_report_plan.py", selected / "deliverable", report_plan, expect=1)
    stale_plan = out / "stale-report-plan.json"
    report_tool("init_report_plan.py", selected / "deliverable", stale_plan,
                "--source-run", selected.name, expect=1)
    assert not stale_plan.exists()
    historical_plan = out / "historical-report-plan.json"
    report_tool("init_report_plan.py", selected / "deliverable", historical_plan,
                "--source-run", selected.name, "--purpose", "historical")
    assert "历史成果报告" in json.loads(historical_plan.read_text(encoding="utf-8"))["required_notice"]
    run("finalize", "--comparison", old_comparison, "--selection", selection,
        "--contract", inputs / "decision-contract.json", "--evidence", inputs / "evidence.json",
        "-o", case / "runs/stale", expect=1)
    external_stale = out / "outside-case-stale"
    external_comparison = out / "copied-case-comparison.json"
    shutil.copy2(old_comparison, external_comparison)
    run("finalize", "--comparison", external_comparison, "--selection", selection,
        "--contract", inputs / "decision-contract.json", "--evidence", inputs / "evidence.json",
        "-o", external_stale, expect=1)
    assert not external_stale.exists()
    run("case", "checkpoint", case, "--stage", 1, "--message", message, "--response", response)
    pending = json.loads(run("case", "status", case))
    assert pending["state"] == "in_progress" and pending["current_artifact"] is None
    assert (case / "CURRENT.md").is_file()
    print("three-stage installed acceptance passed: numeric-array input rejection, constraints, conditions, explicit conditional research selection, full run, "
          "immutable output, payer ledger, incomplete coverage, misleading price proxy, grant funding, "
          "operating capex classification, cash gaps, cash/book bridge, cash solve, selected constraints "
          "refund accounting/tax separation fractional-time selected full run, current-case invalidation, "
          "external-output source gate, report source gate and explicit historical preservation")


if __name__ == "__main__":
    main()
