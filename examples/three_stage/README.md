# 三阶段流程验收示例

本例使用 `../minimal_complete/` 合成项目，不包含真实案例。三个候选分别验证现金缺口、条件未落实和可以进行模拟确认。高单价只用于验收，不代表投资建议或真实项目报价。

从仓库根目录执行，输出必须是新的空目录：

```bash
wwtp-fin compare -p examples/minimal_complete/project.yaml --evidence examples/minimal_complete/evidence.json --contract examples/three_stage/decision-contract.yaml --schemes examples/three_stage/scheme-set.yaml -o out/three-stage/comparison
python3 skills/wwtpfin-consulting-core/scripts/record-selection.py out/three-stage/comparison/scheme-comparison.json complete out/three-stage/selection.json --confirmed-by "合成验收" --confirmed-at 2026-09-11 --reference "synthetic://workflow-example" --purpose workflow_validation
wwtp-fin finalize --comparison out/three-stage/comparison/scheme-comparison.json --selection out/three-stage/selection.json --contract examples/three_stage/decision-contract.yaml --evidence examples/minimal_complete/evidence.json -o out/three-stage/run-0001
wwtp-fin verify-final-run out/three-stage/run-0001
```

预期：`cash_gap` 不满足数值约束；`conditional` 数值通过但条件待落实；只有 `complete` 进入 `selectable_shortlist`。最终结果明确标记 `workflow_validation`，不是甲方确认。

最终运行包含 `input/`、`deliverable/` 和 `final-run.json`。修改任何已登记文件后，验证失败；再次写入同一运行目录也会失败。

普通 `build` 仍用于基准或条件试算。对真实项目进行方案迭代时，合同中的固定参数应覆盖实际固定的服务、投资和评价边界；本例只展示最小接口，不充当项目条件清单。
