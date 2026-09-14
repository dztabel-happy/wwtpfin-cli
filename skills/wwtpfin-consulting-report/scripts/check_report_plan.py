#!/usr/bin/env python3
"""Validate report-plan coverage against one wwtp-fin deliverable."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from init_report_plan import COMMON_MODULES, MODE_MODULES, source_binding
from report_source import verify_source


ALLOWED = {"body", "appendix", "chart_source", "workpaper_only", "audit_only",
           "user_required", "not_applicable"}
MODULE_ALLOWED = {"body", "appendix", "user_required", "not_applicable"}


def _load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def _unique(items, key, label, errors):
    values = [item.get(key) for item in items]
    if any(not value for value in values):
        errors.append("%s 存在空标识" % label)
    duplicates = sorted({value for value in values
                         if value and values.count(value) > 1})
    if duplicates:
        errors.append("%s 重复：%s" % (label, "、".join(duplicates)))
    for item in items:
        if item.get("disposition") not in ALLOWED:
            errors.append("%s %s disposition 非法" % (label, item.get(key)))
    return set(values)


def validate(deliverable: Path, plan_path: Path, *, cli: str = "wwtp-fin", case=None):
    plan = _load(plan_path)
    try:
        if plan.get("deliverable") != str(deliverable.resolve()):
            raise ValueError("报告计划绑定的成果目录与校验来源不一致")
        recorded_case = (plan.get("source_context") or {}).get("case")
        if case and recorded_case and Path(case).resolve() != Path(recorded_case).resolve():
            raise ValueError("指定案例与报告计划绑定案例不一致")
        verified_source = verify_source(deliverable, plan.get("report_purpose"),
                                        cli=cli, case=case or recorded_case)
        if any(plan.get(key) != value for key, value in verified_source.items()):
            raise ValueError("报告用途、来源身份或必留标签与来源成果不一致")
    except (OSError, ValueError, KeyError) as error:
        return [str(error)]
    document = _load(deliverable / "document.json")
    table_index = _load(deliverable / "tables" / "index.json")
    figure_index = _load(deliverable / "figures" / "index.json")
    warning_document = _load(deliverable / "warnings.json")
    evidence = _load(deliverable / "evidence.json")
    errors = []
    if plan.get("source_binding") != source_binding(deliverable):
        errors.append("报告来源成果、参数或选择已经变化；必须重新建立编排计划")
    if plan.get("schema") != "wwtpfin/report-plan/4":
        errors.append("report-plan schema 非法")
    if plan.get("report_kind") != "full_consulting_report":
        errors.append("report_kind 必须为 full_consulting_report")

    result = _load(deliverable / "result.json")
    expected_mode = str((result.get("params") or {}).get("mode") or "")
    if plan.get("transaction_mode") != expected_mode:
        errors.append("transaction_mode 与源运行不一致")

    modules = plan.get("modules") or []
    module_ids = [item.get("module_id") for item in modules]
    if not module_ids or any(not value for value in module_ids):
        errors.append("报告模块存在空标识")
    duplicates = sorted({value for value in module_ids
                         if value and module_ids.count(value) > 1})
    if duplicates:
        errors.append("报告模块重复：%s" % "、".join(duplicates))
    expected_module_ids = {
        module_id for module_id, _title in
        COMMON_MODULES + MODE_MODULES.get(expected_mode, ())}
    actual_module_ids = set(module_ids)
    missing_modules = sorted(expected_module_ids - actual_module_ids)
    extra_modules = sorted(actual_module_ids - expected_module_ids)
    if missing_modules:
        errors.append("报告模块未处置：%s" % "、".join(missing_modules))
    if extra_modules:
        errors.append("报告模块不存在：%s" % "、".join(extra_modules))
    for item in modules:
        disposition = item.get("disposition")
        if disposition not in MODULE_ALLOWED:
            errors.append("报告模块 %s disposition 非法" % item.get("module_id"))
        if disposition in {"user_required", "not_applicable"} and not item.get("reason"):
            errors.append("报告模块缺少处置理由：%s" % item.get("module_id"))
        if plan.get("mode") == "final" and disposition == "user_required":
            errors.append("最终报告不得保留 user_required 模块：%s" % item.get("module_id"))

    expected_blocks = {
        "document.json#/sections/%d/blocks/%d" % (section_index, block_index)
        for section_index, section in enumerate(document.get("sections") or [])
        for block_index, _block in enumerate(section.get("blocks") or [])}
    expected_tables = {item["table_id"] for item in table_index.get("tables") or []}
    expected_figures = {item["figure_id"] for item in figure_index.get("figures") or []}
    expected_warnings = {
        "warnings.json#/warnings/%d" % index
        for index, _item in enumerate(warning_document.get("warnings") or [])}
    expected_unresolved = {
        "evidence.json#/unresolved/%d" % index
        for index, item in enumerate(evidence.get("unresolved") or [])
        if item.get("kind") != "required_user_input"}
    expected_required_inputs = {
        "evidence.json#/items/%d" % index
        for index, item in enumerate(evidence.get("items") or [])
        if item.get("kind") == "required_user_input"}

    actual_blocks = _unique(plan.get("blocks") or [], "source_ref", "语义块", errors)
    actual_tables = _unique(plan.get("tables") or [], "table_id", "表格", errors)
    actual_figures = _unique(plan.get("figures") or [], "figure_id", "图表", errors)
    actual_warnings = _unique(
        plan.get("warnings") or [], "source_ref", "警告", errors)
    actual_unresolved = _unique(
        plan.get("unresolved") or [], "source_ref", "未决事项", errors)
    actual_required_inputs = _unique(
        plan.get("required_inputs") or [], "source_ref", "用户待补", errors)
    for label, expected, actual in (
            ("语义块", expected_blocks, actual_blocks),
            ("表格", expected_tables, actual_tables),
            ("图表", expected_figures, actual_figures),
            ("警告", expected_warnings, actual_warnings),
            ("未决事项", expected_unresolved, actual_unresolved),
            ("用户待补", expected_required_inputs, actual_required_inputs)):
        missing = sorted(expected - actual)
        extra = sorted(actual - expected)
        if missing:
            errors.append("%s 未处置：%s" % (label, "、".join(missing)))
        if extra:
            errors.append("%s 不存在：%s" % (label, "、".join(extra)))

    _unique(plan.get("supplements") or [], "source", "补充材料", errors)
    for item in plan.get("required_inputs") or []:
        if item.get("disposition") not in {"user_required", "not_applicable"}:
            errors.append("用户待补只能标为 user_required 或 not_applicable：%s" % (
                item.get("source_ref")))

    indexed = {item["table_id"]: item for item in table_index.get("tables") or []}
    planned = {item.get("table_id"): item for item in plan.get("tables") or []}
    client_tables = []
    appendix_tables = []
    for table_id in sorted(expected_tables & actual_tables):
        table = indexed[table_id]
        item = planned[table_id]
        role = table.get("report_role")
        disposition = item.get("disposition")
        if role not in {"body", "appendix", "workpaper", "audit"}:
            errors.append("表格报告角色非法：%s" % table_id)
        if role == "audit" and disposition != "audit_only":
            errors.append("审计表只能保留为审计材料：%s" % table_id)
        if table.get("report_role") in {"body", "appendix"} and \
                disposition in {"audit_only", "workpaper_only"}:
            errors.append("客户表不得隐藏为底稿或审计材料：%s" % table_id)
        if role == "workpaper" and disposition == "audit_only":
            errors.append("技术底稿不得伪装为审计材料：%s" % table_id)
        if role != "workpaper" and disposition == "workpaper_only":
            errors.append("只有技术底稿可标为 workpaper_only：%s" % table_id)
        if disposition == "not_applicable" and not item.get("reason"):
            errors.append("表格缺少排除理由：%s" % table_id)
        if disposition in {"body", "appendix", "chart_source"} and \
                not item.get("section"):
            errors.append("报告表格缺少落点章节：%s" % table_id)
        if disposition == "appendix" and not item.get("reason"):
            errors.append("附表缺少客户用途说明：%s" % table_id)
        if role == "workpaper" and disposition in {"body", "appendix"} and \
                not item.get("reason"):
            errors.append("技术底稿进入客户报告缺少理由：%s" % table_id)
        if disposition in {"body", "appendix"}:
            client_tables.append(table_id)
            if disposition == "appendix":
                appendix_tables.append(table_id)
            required = {column["id"] for column in table.get("columns") or []
                        if not column.get("display_ready")}
            supplied = set((item.get("localized_columns") or {}).keys())
            if required - supplied:
                errors.append("表格缺中文展示列：%s.%s" % (
                    table_id, "、".join(sorted(required - supplied))))
    if len(client_tables) > 32:
        errors.append("客户报告选表过多：%d，最多 32" % len(client_tables))
    if len(appendix_tables) > 12:
        errors.append("客户附表过多：%d，最多 12" % len(appendix_tables))
    return errors


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("deliverable", type=Path)
    parser.add_argument("report_plan", type=Path)
    parser.add_argument("--case", help="核对案例目录与计划绑定一致")
    parser.add_argument("--cli", default="wwtp-fin", help="用于来源校验的匹配 CLI 可执行文件")
    args = parser.parse_args()
    errors = validate(args.deliverable, args.report_plan, cli=args.cli, case=args.case)
    if errors:
        for error in errors:
            print("ERROR: %s" % error)
        raise SystemExit(1)
    print("report plan: OK")


if __name__ == "__main__":
    main()
