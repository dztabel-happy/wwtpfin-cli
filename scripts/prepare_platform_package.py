#!/usr/bin/env python3
"""Stage a PyInstaller onedir bundle in an npm platform package."""
from __future__ import annotations

import argparse
import json
import re
import shutil
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
BINARIES = {
    "darwin-arm64": "wwtp-fin",
    "linux-x64": "wwtp-fin",
    "win32-x64": "wwtp-fin.exe",
}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--platform", choices=sorted(BINARIES), required=True)
    parser.add_argument("--bundle-dir", type=Path, required=True)
    args = parser.parse_args(argv)

    binary_name = BINARIES[args.platform]
    source_binary = args.bundle_dir / binary_name
    source_internal = args.bundle_dir / "_internal"
    if not source_binary.is_file() or not source_internal.is_dir():
        raise SystemExit(f"Incomplete PyInstaller bundle: {args.bundle_dir}")

    package_root = PROJECT_ROOT / "npm" / "platform-packages" / args.platform
    manifest_path = package_root / "package.json"
    manifest = _read_json(manifest_path)
    main_version = _read_json(PROJECT_ROOT / "package.json")["version"]
    manifest["version"] = main_version
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    destination_binary = package_root / binary_name
    destination_internal = package_root / "_internal"
    destination_binary.unlink(missing_ok=True)
    if destination_internal.exists():
        shutil.rmtree(destination_internal)
    shutil.copy2(source_binary, destination_binary)
    shutil.copytree(source_internal, destination_internal)
    destination_binary.chmod(destination_binary.stat().st_mode | 0o755)
    _verify_bundle_boundary(destination_internal)
    print(f"{args.platform} {main_version}")
    return 0


def _read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _verify_bundle_boundary(internal: Path) -> None:
    private = re.compile(
        r"src/wwtpfin|wushuichuli|caseadapters|benchmarks-work|"
        r"亳州|滨江|霍邱|太湖|天门山|下浮",
        re.IGNORECASE,
    )
    for path in internal.rglob("*"):
        if path.is_dir():
            continue
        if path.name == "direct_url.json" or path.suffix == ".py":
            raise SystemExit(f"Platform bundle exposes build metadata or source: {path}")
        if path.suffix in {".json", ".txt"} or path.name == "METADATA":
            text = path.read_text(encoding="utf-8", errors="ignore")
            if private.search(text):
                raise SystemExit(f"Platform bundle exposes private content: {path}")


if __name__ == "__main__":
    raise SystemExit(main())
