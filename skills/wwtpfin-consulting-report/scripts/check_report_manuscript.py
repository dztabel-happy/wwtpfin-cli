#!/usr/bin/env python3
"""Reject mechanically assembled client manuscripts before Word rendering."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Optional


MAX_TABLES = 40
MIN_NARRATIVE_CHARS_PER_TABLE = 250
MACHINE_ID = re.compile(r"\b[a-z][a-z0-9]*(?:_[a-z0-9]+)+\b")
IMAGE_PATH = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")
ALLOWED_REPORT_ROOT = {"report.md", "report-plan.json", "charts", "docx"}
PLACEHOLDER = re.compile(r"\[待(?:用户)?补充[^\]]*\]")


def validate(path: Path, allow_placeholders: bool = False,
             plan_path: Optional[Path] = None):
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    errors = []
    metadata = {}
    body = []
    in_frontmatter = False
    frontmatter_closed = False
    in_fence = False
    table_count = 0
    previous_table_line = False
    narrative_chars = 0
    bridge_count = 0

    for line in lines:
        stripped = line.strip()
        if not frontmatter_closed and stripped == "---":
            if not in_frontmatter:
                in_frontmatter = True
            else:
                in_frontmatter = False
                frontmatter_closed = True
            continue
        if in_frontmatter:
            if ":" in line:
                key, value = line.split(":", 1)
                metadata[key.strip()] = value.strip()
            continue
        if stripped.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        body.append(line)
        is_table_line = line.lstrip().startswith("|")
        if is_table_line and not previous_table_line:
            table_count += 1
        previous_table_line = is_table_line
        if not is_table_line and not stripped.startswith(("#", "![")):
            narrative_chars += len(stripped)
        if "该表保持经验证成果包的数值口径" in line:
            bridge_count += 1

    if not metadata.get("title"):
        errors.append("Word 稿缺少 title")
    if metadata.get("document_mode") != "report":
        errors.append("Word 稿必须声明 document_mode: report")
    if table_count > MAX_TABLES:
        errors.append("Word 稿表格过多：%d，最多 %d" % (table_count, MAX_TABLES))
    if table_count and narrative_chars / table_count < MIN_NARRATIVE_CHARS_PER_TABLE:
        errors.append("Word 稿分析密度不足：每表 %.1f 个叙事字符，至少 %d" % (
            narrative_chars / table_count, MIN_NARRATIVE_CHARS_PER_TABLE))
    machine_ids = sorted(set(MACHINE_ID.findall("\n".join(body))))
    if machine_ids:
        errors.append("客户稿暴露机器标识：%s" % "、".join(machine_ids[:12]))
    if bridge_count > 3:
        errors.append("机械表格过渡语重复：%d 处" % bridge_count)
    placeholders = PLACEHOLDER.findall("\n".join(body))
    if placeholders and not allow_placeholders:
        errors.append("来源支撑稿不得保留待补章节占位：%d 处" % len(placeholders))
    headings = [re.sub(r"^#+\s+(?:\d+(?:\.\d+)*\s+)?", "", line.strip())
                for line in body if line.lstrip().startswith("#")]
    if plan_path:
        plan = json.loads(plan_path.read_text(encoding="utf-8"))
        omitted = {str(item.get("title") or "").strip()
                   for item in plan.get("modules") or []
                   if item.get("disposition") == "user_required"}
        leaked = sorted(item for item in omitted if item and item in headings)
        if leaked and not allow_placeholders:
            errors.append("用户待补模块不得进入来源支撑稿：%s" % "、".join(leaked))
    unexpected = sorted(
        item.name for item in path.parent.iterdir()
        if item.name not in ALLOWED_REPORT_ROOT)
    if unexpected:
        errors.append("报告目录混入过程文件：%s" % "、".join(unexpected))
    chart_root = path.parent / "charts"
    if chart_root.is_dir():
        selected = {
            parts[1]
            for match in IMAGE_PATH.findall(text)
            for parts in [Path(match).parts]
            if len(parts) >= 3 and parts[0] == "charts"
        }
        actual = {item.name for item in chart_root.iterdir() if item.is_dir()}
        extras = sorted(actual - selected)
        if extras:
            errors.append("图表目录含未使用版本：%s" % "、".join(extras))
    return errors, table_count, narrative_chars


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("report", type=Path)
    parser.add_argument("--plan", type=Path)
    parser.add_argument("--allow-placeholders", action="store_true")
    args = parser.parse_args()
    errors, table_count, narrative_chars = validate(
        args.report, allow_placeholders=args.allow_placeholders,
        plan_path=args.plan)
    if errors:
        for error in errors:
            print("ERROR: %s" % error)
        raise SystemExit(1)
    print("report manuscript: OK (%d tables, %d narrative chars)" % (
        table_count, narrative_chars))


if __name__ == "__main__":
    main()
