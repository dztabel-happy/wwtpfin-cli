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
                    "maintain", str(out / "cost-selection.json"), "--confirmed-by", "synthetic acceptance",
                    "--confirmed-at", "2026-09-11", "--reference", "synthetic://payer",
                    "--purpose", "workflow_validation"], check=True, capture_output=True)
    run("finalize", "--comparison", out / "cost-comparison/scheme-comparison.json",
        "--selection", out / "cost-selection.json", "--contract", out / "cost-contract.json",
        "--evidence", evidence, "-o", out / "cost-final")
    run("verify-final-run", out / "cost-final")
    cost_final = json.loads((out / "cost-final/deliverable/result.json").read_text(encoding="utf-8"))
    assert cost_final["scalars"]["payer_net_outflow_wan"] == costs["candidates"][0]["objective_value"]
    assert "payer_cashflows" in cost_final["tables"]
    changed_spec["objective"] = data["objective"]
    run("compare", "-p", payer_params, "--contract", contract, "--evidence", evidence,
        "--schemes", save("proxy-schemes.json", changed_spec), "-o", out / "proxy")
    proxy = json.loads((out / "proxy/scheme-comparison.json").read_text(encoding="utf-8"))
    assert proxy["candidates"][1]["readiness"] == "not_comparable"
    print("three-stage installed acceptance passed: constraints, conditions, selection, full run, "
          "immutable output, payer ledger, incomplete coverage, misleading price proxy")


if __name__ == "__main__":
    main()
