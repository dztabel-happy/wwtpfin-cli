#!/usr/bin/env python3
"""Run synthetic workflow acceptance against an installed CLI, without core imports."""
import argparse
from copy import deepcopy
import json
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

    def run(*parts, expect=0):
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

    def save(name, value):
        path = out / name
        path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")
        return path

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
    print("three-stage installed acceptance passed: constraints, conditions, selection, full run, "
          "immutable output, payer ledger, incomplete coverage, misleading price proxy, grant funding, "
          "operating capex classification, cash gaps, cash/book bridge, cash solve, selected constraints "
          "and refund accounting/tax separation")


if __name__ == "__main__":
    main()
