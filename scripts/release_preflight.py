#!/usr/bin/env python3
"""Build, pack, install, and smoke-test the local release pair."""
from __future__ import annotations

import argparse
import json
import os
import platform
import subprocess
import sys
import tempfile
from pathlib import Path


PUBLIC_ROOT = Path(__file__).resolve().parents[1]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--core-repo",
        type=Path,
        default=PUBLIC_ROOT.parent / "wushuichuli",
    )
    parser.add_argument("--skip-core-gates", action="store_true")
    parser.add_argument("--skip-binary-build", action="store_true")
    args = parser.parse_args(argv)
    core = args.core_repo.resolve()
    target = _current_platform()
    core_python = _core_python(core)

    _run([str(PUBLIC_ROOT / "scripts" / "verify_public.sh"), "--core-repo", str(core)])
    if not args.skip_core_gates:
        _run(["make", "test", "check", "cleaninstall", "benchmark"], cwd=core)
    if not args.skip_binary_build:
        _run([str(core_python), "scripts/build_binary.py"], cwd=core)

    bundle = core / "dist" / "wwtp-fin"
    _run([
        sys.executable,
        "scripts/prepare_platform_package.py",
        "--platform",
        target,
        "--bundle-dir",
        str(bundle),
    ])

    with tempfile.TemporaryDirectory() as tmp:
        temp = Path(tmp)
        main_pack = _pack(PUBLIC_ROOT, temp)
        platform_pack = _pack(PUBLIC_ROOT / "npm" / "platform-packages" / target, temp)
        install = temp / "install"
        _run(["npm", "install", "--prefix", str(install), str(main_pack), str(platform_pack)])
        binary = install / "node_modules" / ".bin" / (
            "wwtp-fin.cmd" if os.name == "nt" else "wwtp-fin"
        )
        _run([str(binary), "--version"])
        _run([str(binary), "schema", "--kind", "input"], capture=True)
        output = temp / "deliverable"
        _run([
            str(binary),
            "build",
            "-p",
            str(PUBLIC_ROOT / "examples" / "showcase" / "project.yaml"),
            "--evidence",
            str(PUBLIC_ROOT / "examples" / "showcase" / "evidence.json"),
            "-o",
            str(output),
        ])
        _run([str(binary), "verify-deliverable", str(output)])
    print("release preflight passed")
    return 0


def _current_platform() -> str:
    key = (sys.platform, platform.machine().lower())
    targets = {
        ("darwin", "arm64"): "darwin-arm64",
        ("linux", "x86_64"): "linux-x64",
        ("win32", "amd64"): "win32-x64",
    }
    if key not in targets:
        raise SystemExit(f"Unsupported release platform: {key[0]}/{key[1]}")
    return targets[key]


def _core_python(core: Path) -> Path:
    candidate = core / ".venv" / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
    return candidate if candidate.exists() else Path(sys.executable)


def _pack(package_root: Path, destination: Path) -> Path:
    result = _run(
        ["npm", "pack", "--json", "--pack-destination", str(destination)],
        cwd=package_root,
        capture=True,
    )
    payload = json.loads(result.stdout)
    return destination / payload[0]["filename"]


def _run(
    command: list[str],
    *,
    cwd: Path = PUBLIC_ROOT,
    capture: bool = False,
) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(command, cwd=cwd, text=True, capture_output=capture)
    if result.returncode:
        if capture:
            print(result.stdout, end="")
            print(result.stderr, end="", file=sys.stderr)
        raise SystemExit(result.returncode)
    return result


if __name__ == "__main__":
    raise SystemExit(main())
