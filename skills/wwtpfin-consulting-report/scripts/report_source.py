"""Verify report source identity with the chosen installed wwtp-fin CLI."""
from __future__ import annotations

import json
from pathlib import Path
import shutil
import subprocess


PURPOSES = ("current", "historical", "baseline", "conditional_research")


def _cli(executable: str, *args: str):
    launcher = Path(shutil.which(executable) or executable)
    command = [str(launcher), *map(str, args)]
    if launcher.suffix.lower() == ".cmd":
        # npm local .bin and Windows global installations use different layouts.
        wrappers = [launcher.parent.parent / "@dztabel/wwtpfin/npm/wwtp-fin.cjs",
                    launcher.parent / "node_modules/@dztabel/wwtpfin/npm/wwtp-fin.cjs"]
        wrapper = next((path for path in wrappers if path.is_file()), None)
        if wrapper is None:
            raise ValueError("无法定位 npm CLI 的 Node 入口：%s" % launcher)
        command = ["node", str(wrapper), *map(str, args)]
    try:
        result = subprocess.run(command, capture_output=True, text=True,
                                encoding="utf-8", check=False)
    except OSError as error:
        raise ValueError("无法执行来源校验 CLI：%s" % error) from error
    if result.returncode:
        raise ValueError("报告来源校验失败：%s" % (
            (result.stderr.strip() or result.stdout.strip()) or "CLI 未通过"))
    return result.stdout


def verify_source(deliverable: Path, purpose: str, *, cli: str = "wwtp-fin",
                  case: str | None = None):
    if purpose not in PURPOSES:
        raise ValueError("必须明确声明报告用途：current/historical/baseline/conditional_research")
    deliverable = deliverable.resolve()
    discovered = next((path for path in (deliverable, *deliverable.parents)
                       if (path / "case.json").is_file()), None)
    case_root = Path(case).resolve() if case else discovered
    if discovered and case_root != discovered:
        raise ValueError("指定案例与来源成果所属案例不一致")
    # Validate the package before trusting its source/selection metadata.
    _cli(cli, "verify-deliverable", str(deliverable))
    result = json.loads((deliverable / "result.json").read_text(encoding="utf-8"))
    selected = result.get("selected_scheme") or {}
    run = deliverable.parent
    scope = selected.get("selection_scope", "implementation") if selected else None
    if selected:
        if deliverable.name != "deliverable":
            raise ValueError("选定报告必须使用完整运行内的 deliverable 目录")
        _cli(cli, "verify-final-run", str(run))
    if purpose == "baseline":
        if selected:
            raise ValueError("基准报告不能使用已选定成果")
        if case_root:
            current = json.loads(_cli(cli, "case", "status", str(case_root)))
            artifact = current.get("current_artifact") or {}
            if (current.get("state") != "current" or artifact.get("kind") != "baseline"
                    or Path(artifact.get("path", "")).resolve() != deliverable):
                raise ValueError("该基准不是案例当前有效基准；旧成果须显式声明 historical")
    elif purpose in ("current", "conditional_research"):
        if not selected:
            raise ValueError("当前或条件研究报告必须使用已选定的完整运行；基准请显式声明 baseline")
        if purpose == "conditional_research" and scope != "conditional_research":
            raise ValueError("条件研究报告必须绑定 conditional_research 选择范围")
        if not case_root and purpose == "current":
            raise ValueError("当前报告需要案例；请提供 --case，或显式声明独立报告用途")
        if case_root:
            _cli(cli, "verify-final-run", str(run), "--case", str(case_root))

    notices = {
        "current": "本报告使用案例当前登记的选定成果；报告内容完成不代表实施已获批准。",
        "historical": "本报告为历史成果报告，仅说明对应历史依据和结果，不代表当前案例结论。",
        "baseline": "本报告为基准测算报告，不代表选定实施方案。",
        "conditional_research": "本报告为条件研究报告，不代表实施已获批准。",
    }
    notice = notices[purpose]
    pending = sum(item.get("status") == "pending" for item in selected.get("conditions", []))
    if scope == "conditional_research":
        notice += "本成果属于选定条件研究，待落实实施条件 %d 项；未将待落实条件认定为已满足。" % pending
    selection_purpose = (selected.get("selection") or {}).get("purpose")
    if selection_purpose == "workflow_validation":
        notice += "本报告为模拟流程验收，不代表真实甲方确认。"
    return {
        "report_purpose": purpose,
        "source_context": {"case": str(case_root) if case_root else None,
                           "run": str(run), "selection_scope": scope,
                           "selection_purpose": selection_purpose,
                           "pending_conditions": pending},
        "required_notice": notice,
    }
