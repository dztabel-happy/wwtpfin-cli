#!/usr/bin/env python3
"""Create an explicit, initially unassigned report-plan ledger."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


COMMON_MODULES = (
    ("executive_summary", "执行摘要"),
    ("project_overview", "项目概况与编制基础"),
    ("necessity_feasibility", "必要性与可行性"),
    ("transaction_structure", "特许经营模式与交易结构"),
    ("investment_financing", "投资、融资与资产安排"),
    ("volume_tariff_cost_tax", "水量、收入、成本与税务"),
    ("financial_evaluation", "财务评价、偿债与敏感性"),
    ("compliance", "合法合规与政策依据"),
    ("performance_supervision", "绩效考核与监督管理"),
    ("risk_allocation", "风险分配与保障机制"),
    ("exit_handover", "退出、终止与移交"),
    ("conclusions_actions", "结论与实施建议"),
    ("unresolved_inputs", "未决事项与待补资料"),
    ("financial_appendices", "财务附表"),
)

MODE_MODULES = {
    "TOT": (
        ("asset_inventory_condition", "存量资产范围、权属与状况"),
        ("valuation_transfer", "资产估值与转让安排"),
        ("historical_operations_transition", "历史运营与交接安排"),
    ),
    "O&M": (
        ("service_scope_kpi", "运维服务边界与绩效要求"),
        ("historical_operations_transition", "历史运营与交接安排"),
    ),
    "BOT": (
        ("construction_scope_schedule", "建设范围、进度与验收"),
        ("ramp_up_acceptance", "运营爬坡与达产条件"),
    ),
    "BOOT": (
        ("construction_scope_schedule", "建设范围、进度与验收"),
        ("ownership_transfer", "特许期权属与期末转让"),
    ),
    "DBFOT": (
        ("design_construction_scope", "设计、建设范围与变更责任"),
        ("ramp_up_acceptance", "运营爬坡与达产条件"),
    ),
    "BOO": (
        ("construction_scope_schedule", "建设范围、进度与验收"),
        ("ownership_exit", "项目权属与退出安排"),
    ),
    "ROT": (
        ("asset_inventory_condition", "存量资产范围、权属与状况"),
        ("rehabilitation_scope", "改造范围、投资与验收"),
        ("historical_operations_transition", "历史运营与交接安排"),
    ),
    "TOT+BOT": (
        ("asset_inventory_condition", "存量资产范围、权属与状况"),
        ("construction_scope_schedule", "新增建设范围、进度与验收"),
        ("existing_new_interface", "存量与新增设施接口"),
    ),
    "改扩建": (
        ("asset_inventory_condition", "存量资产范围、权属与状况"),
        ("rehabilitation_scope", "改扩建范围、投资与验收"),
        ("existing_new_interface", "存量与新增设施接口"),
    ),
}


def _load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def source_binding(deliverable: Path):
    result = _load(deliverable / "result.json")
    def digest(value):
        return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True,
                                        separators=(",", ":"), allow_nan=False).encode()).hexdigest()
    return {
        "manifest_sha256": hashlib.sha256((deliverable / "manifest.json").read_bytes()).hexdigest(),
        "params_sha256": digest(result["params"]),
        "selection_sha256": digest((result.get("selected_scheme") or {}).get("selection")),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("deliverable", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--source-run", required=True)
    parser.add_argument("--mode", choices=("draft", "final"), default="draft")
    args = parser.parse_args()

    document = _load(args.deliverable / "document.json")
    result = _load(args.deliverable / "result.json")
    tables = _load(args.deliverable / "tables" / "index.json")["tables"]
    figures = _load(args.deliverable / "figures" / "index.json")["figures"]
    warnings = _load(args.deliverable / "warnings.json").get("warnings") or []
    evidence = _load(args.deliverable / "evidence.json")
    required_inputs = [
        (index, item) for index, item in enumerate(evidence.get("items") or [])
        if item.get("kind") == "required_user_input"]
    unresolved = [
        (index, item) for index, item in enumerate(evidence.get("unresolved") or [])
        if item.get("kind") != "required_user_input"]
    transaction_mode = str((result.get("params") or {}).get("mode") or "")
    modules = COMMON_MODULES + MODE_MODULES.get(transaction_mode, ())
    plan = {
        "schema": "wwtpfin/report-plan/4",
        "report_kind": "full_consulting_report",
        "source_run": args.source_run,
        "source_binding": source_binding(args.deliverable),
        "deliverable": str(args.deliverable.resolve()),
        "mode": args.mode,
        "transaction_mode": transaction_mode,
        "modules": [
            {"module_id": module_id, "title": title,
             "disposition": "unassigned"}
            for module_id, title in modules],
        "blocks": [
            {"source_ref": "document.json#/sections/%d/blocks/%d" % (i, j),
             "type": block.get("type"),
             "topic_id": block.get("topic_id"),
             "topic_role": block.get("topic_role"),
             "disposition": "unassigned"}
            for i, section in enumerate(document.get("sections") or [])
            for j, block in enumerate(section.get("blocks") or [])],
        "tables": [
            {"table_id": table["table_id"],
             "title": table.get("title"),
             "report_role": table.get("report_role"),
             "disposition": ({"body": "body", "appendix": "unassigned",
                              "workpaper": "workpaper_only",
                              "audit": "audit_only"}
                             .get(table.get("report_role"), "unassigned"))}
            for table in tables],
        "figures": [
            {"figure_id": figure["figure_id"],
             "title": figure.get("title"),
             "disposition": "unassigned"}
            for figure in figures],
        "warnings": [
            {"source_ref": "warnings.json#/warnings/%d" % index,
             "warning_id": item.get("id"),
             "path": item.get("path"),
             "message": item.get("message"),
             "disposition": "unassigned"}
            for index, item in enumerate(warnings)],
        "unresolved": [
            {"source_ref": "evidence.json#/unresolved/%d" % index,
             "evidence_id": item.get("evidence_id"),
             "label": item.get("label"),
             "reason": item.get("reason"),
             "disposition": "unassigned"}
            for index, item in unresolved],
        "required_inputs": [
            {"source_ref": "evidence.json#/items/%d" % index,
             "evidence_id": item.get("evidence_id"),
             "label": item.get("label"),
             "reason": item.get("reason"),
             "disposition": "user_required"}
            for index, item in required_inputs],
        "supplements": [],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(plan, ensure_ascii=False, indent=2) + "\n",
                           encoding="utf-8")


if __name__ == "__main__":
    main()
