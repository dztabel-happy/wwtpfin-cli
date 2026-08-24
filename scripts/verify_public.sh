#!/usr/bin/env bash
# 公开仓自检:核心源码零泄漏、案例专属词零命中、npm 打包干跑。任一失败即非零退出。
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"; cd "$ROOT"
PAYLOAD=(package.json npm skills examples docs README.md README.zh-CN.md)
fail=0
# 1) 核心源码/私有路径泄漏
if grep -R -n -E 'src/wwtpfin|wushuichuli|caseadapters|benchmarks-work' "${PAYLOAD[@]}" 2>/dev/null; then
  echo "✗ 发现核心源码/私有路径引用"; fail=1
else echo "✓ 无核心源码泄漏"; fi
# 2) 案例专属词
if grep -R -n -E '亳州|滨江|霍邱|太湖|天门山|下浮' "${PAYLOAD[@]}" 2>/dev/null; then
  echo "✗ 发现案例专属词"; fail=1
else echo "✓ 案例专属词零命中"; fi
# 3) npm 打包干跑
npm pack --dry-run > /dev/null 2>&1 && echo "✓ npm pack 干跑通过" || { echo "✗ npm pack 失败"; fail=1; }
exit $fail
