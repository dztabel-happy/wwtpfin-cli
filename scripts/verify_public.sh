#!/usr/bin/env bash
# 公开仓自检：包边界、版本/平台元数据、工作流和 npm 打包形制。任一失败即非零退出。
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CORE_REPO=""
if [ "${1:-}" = "--core-repo" ]; then
  CORE_REPO="${2:?--core-repo requires a path}"
fi
cd "$ROOT"

PAYLOAD=(
  package.json
  npm/wwtp-fin.cjs
  npm/platform-packages/darwin-arm64/package.json
  npm/platform-packages/linux-x64/package.json
  npm/platform-packages/win32-x64/package.json
  skills examples docs README.md README.zh-CN.md DOMAIN_CONTRACT.md CHANGELOG.md
)
if grep -R -n -E 'src/wwtpfin|wushuichuli|caseadapters|benchmarks-work' "${PAYLOAD[@]}" 2>/dev/null; then
  echo "发现核心源码或私有路径引用" >&2
  exit 1
fi
if grep -R -n -E -i 'huoqiu|taihu|tianmenshan|bozhou|binjiang|zhujiaqiao|亳州|滨江|霍邱|太湖|天门山|朱家桥' "${PAYLOAD[@]}" 2>/dev/null; then
  echo "发现案例专属词" >&2
  exit 1
fi

node <<'NODE'
const fs = require("node:fs");
const main = JSON.parse(fs.readFileSync("package.json", "utf8"));
const platforms = {
  "darwin-arm64": ["@dztabel/wwtpfin-darwin-arm64", "darwin", "arm64", "wwtp-fin"],
  "linux-x64": ["@dztabel/wwtpfin-linux-x64", "linux", "x64", "wwtp-fin"],
  "win32-x64": ["@dztabel/wwtpfin-win32-x64", "win32", "x64", "wwtp-fin.exe"],
};
for (const [folder, [name, os, cpu, binary]] of Object.entries(platforms)) {
  const manifest = JSON.parse(fs.readFileSync(`npm/platform-packages/${folder}/package.json`, "utf8"));
  if (manifest.name !== name || manifest.version !== main.version ||
      main.optionalDependencies[name] !== main.version ||
      JSON.stringify(manifest.os) !== JSON.stringify([os]) ||
      JSON.stringify(manifest.cpu) !== JSON.stringify([cpu]) ||
      !manifest.files.includes(binary) || !manifest.files.includes("_internal")) {
    throw new Error(`platform manifest mismatch: ${folder}`);
  }
}
const wrapper = require("./npm/wwtp-fin.cjs");
for (const [, [name, os, cpu]] of Object.entries(platforms)) {
  if (wrapper.platformPackageName(os, cpu) !== name) {
    throw new Error(`launcher platform mismatch: ${os}/${cpu}`);
  }
}
NODE

if grep -q 'TODO' .github/workflows/release.yml; then
  echo "发布工作流仍含 TODO" >&2
  exit 1
fi
grep -q 'core_ref:' .github/workflows/release.yml
grep -q 'CORE_DEPLOY_KEY' .github/workflows/release.yml
grep -q 'NPM_TOKEN' .github/workflows/release.yml
test "$(grep -Fc 'ref: ${{ inputs.core_ref }}' .github/workflows/release.yml)" -eq 1
test "$(grep -Fc 'ref: ${{ needs.resolve-core-ref.outputs.core_sha }}' .github/workflows/release.yml)" -eq 2
grep -q 'core_sha=$(git rev-parse HEAD)' .github/workflows/release.yml

if [ -n "$CORE_REPO" ]; then
  python3 "$CORE_REPO/scripts/sync_public_assets.py" "$ROOT" --check
  core_version="$(python3 -c 'import re,sys; text=open(sys.argv[1], encoding="utf-8").read(); match=re.search(r"(?ms)^\[project\].*?^version\s*=\s*\"([^\"]+)\"", text); print(match.group(1) if match else "")' "$CORE_REPO/pyproject.toml")"
  public_version="$(node -p "require('./package.json').version")"
  if [ "$core_version" != "$public_version" ]; then
    echo "版本不一致: core=$core_version public=$public_version" >&2
    exit 1
  fi
fi

npm pack --dry-run --json | node -e '
let input = "";
process.stdin.on("data", chunk => input += chunk);
process.stdin.on("end", () => {
  const files = JSON.parse(input).flatMap(pack => pack.files.map(file => file.path));
  const unexpected = files.filter(path => /(^|\/)__pycache__(\/|$)|\.py[co]$/.test(path));
  if (unexpected.length) throw new Error("Python cache files in npm package: " + unexpected.join(", "));
});'
echo "public package verification passed"
