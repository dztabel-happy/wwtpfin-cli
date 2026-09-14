#!/usr/bin/env python3
"""将客户报告中的 Markdown 数值表统一为可读展示格式。"""
from __future__ import annotations

import argparse
from pathlib import Path
import re


NUMBER = re.compile(r"^[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?$")
PERCENT_HINTS = ("率", "比例", "幅度", "FIRR", "IRR")
RATIO_EXCEPTIONS = ("偿债备付率", "利息备付率", "DSCR", "ICR")
GENERIC_VALUE_HEADERS = {"值", "数值", "测算值", "结果"}


def _format_number(value: str, header: str, label: str) -> str:
    text = value.strip()
    if not NUMBER.fullmatch(text):
        return text
    number = float(text)
    ratio_exception = any(hint in header or hint in label for hint in RATIO_EXCEPTIONS)
    header_percent = any(hint in header for hint in PERCENT_HINTS)
    label_percent = any(hint in label for hint in PERCENT_HINTS) and (
        header in GENERIC_VALUE_HEADERS or bool(re.fullmatch(r"\d{4}", header))
    )
    if not ratio_exception and (header_percent or label_percent) and abs(number) <= 2:
        return f"{number * 100:.2f}%"
    if "年" in header and number.is_integer():
        return str(int(number))
    if abs(number) < 0.005:
        number = 0.0
    return f"{number:,.2f}"


def format_markdown(markdown: str) -> str:
    lines = markdown.splitlines()
    output: list[str] = []
    index = 0
    while index < len(lines):
        if not lines[index].lstrip().startswith("|"):
            output.append(lines[index])
            index += 1
            continue
        table: list[str] = []
        while index < len(lines) and lines[index].lstrip().startswith("|"):
            table.append(lines[index])
            index += 1
        if len(table) < 2:
            output.extend(table)
            continue
        headers = [cell.strip() for cell in table[0].strip().strip("|").split("|")]
        output.extend(table[:2])
        for row in table[2:]:
            cells = [cell.strip() for cell in row.strip().strip("|").split("|")]
            label = cells[0] if cells else ""
            for cell_index in range(1, len(cells)):
                header = headers[cell_index] if cell_index < len(headers) else ""
                cells[cell_index] = _format_number(cells[cell_index], header, label)
            output.append("| " + " | ".join(cells) + " |")
    suffix = "\n" if markdown.endswith("\n") else ""
    return "\n".join(output) + suffix


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("markdown", type=Path)
    args = parser.parse_args()
    content = args.markdown.read_text(encoding="utf-8")
    args.markdown.write_text(format_markdown(content), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
