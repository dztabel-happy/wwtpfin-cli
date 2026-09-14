# 当前工作与历史判断

三阶段可以往返。项目资料、研究目标、政策依据或用户偏好变化并需要重新研究时，先登记新的工作轮次；新结果完成前，当前入口显示正在更新，旧结论保留为历史。仅确认已有候选时，明确绑定该候选所在的当前比较，按下文的选择步骤继续。

## 各阶段的输入、输出和约束

| 阶段 | 使用的输入 | 本轮应交付什么 | 不能越过的约束 |
|---|---|---|---|
| 1 建立起点 | 用户材料、成本目标、已知要求及本轮交互 | 可计算基准或明确阻塞项；事实/估算/冲突台账；研究方向；决策合同 | 不把初稿当定论，不虚构来源或把缺失成本当零；有依据估算和条件情景可以继续 |
| 2 研究与迭代 | 当前基准、合同、实施条件、找到的依据、用户取舍 | 单项和组合测算；保留/排除理由；成本与责任；不确定性；限定已研究范围的建议 | 新政策须核适用条件；组合须重算；目标/服务边界改变先更新合同；数值排序不代替选择 |
| 3 选定与复核 | 用户明确选择、对应比较、完整参数、证据与条件记录 | 选定方案全量重算、检查和绑定成果；剩余边界 | 选择必须绑定当前比较并声明确认范围；条件研究可保留待落实项，不能改成已满足；新事实影响结果时返回前阶段 |

每一阶段都可以产生有用的中间成果。菜单不是阶段二的终点；没有可行方案应继续研究或解释需要改变的边界。阶段三的完整计算也不是项目获得审批或融资承诺的证明。

## 一份当前入口与逐轮记录

案例根目录使用以下文件：

- `input/`：当前工作输入，包括规范化参数、证据、决策合同和转换/判断底稿。规范化参数、证据和合同各保留一个当前版本；备份放入轮次记录，不能同时摆放两个同名不同扩展名的当前版本。
- `sources/`：用户原始材料；新版本使用新文件名，原件保留，来源登记表说明本轮采用哪一版。变更也进入当前性检查；轮次保存来源哈希，不重复复制大型原件。
- `rounds/round-NNNN/`：每轮用户原话、agent答复、输入快照及来源哈希，不覆盖历史。
- `case.json`：显式记录当前轮次与登记产物，不能按文件修改时间推断。
- `CURRENT.md`：业务人员查看当前进展、有效产物及历史索引的入口。
- `selections/selection-NNNN.json`：每次选择独立保存，便于后续撤回或重新选择而不覆盖旧确认。

原话文件与业务答复由agent写入案例目录。答复应说明采用、保留或排除某项建议的理由。命令会保存文件原文，不能用agent的概括替换用户原话，也不能把模拟交互写成真实甲方确认。

```bash
# 新材料/目标/取舍需要重新研究时，先登记本轮工作，尚未完成时不带artifact。
wwtp-fin case checkpoint CASE --stage 1 --message CASE/responses/user-001.md --response CASE/responses/working-001.md

# 第一阶段基准通过后，登记确切的完整成果目录。
wwtp-fin case checkpoint CASE --stage 1 --message CASE/responses/user-001.md --response CASE/responses/round-001.md --kind baseline --artifact CASE/runs/run-0001/deliverable

# 第二阶段比较：同时绑定实际使用的方案集文件，条件编辑也会被检测。
wwtp-fin case checkpoint CASE --stage 2 --message CASE/responses/user-002.md --response CASE/responses/round-002.md --kind comparison --artifact CASE/comparisons/compare-0001/output/scheme-comparison.json --schemes CASE/comparisons/compare-0001/scheme-set.yaml

# 每次回复、恢复工作和交付前刷新当前入口。
wwtp-fin case status CASE
```

返回第一阶段并不删除第二阶段成果。无新产物的轮次显示 `in_progress`；已登记产物与当前依据不一致时显示 `needs_update`。两种情况下都不将旧结果作为当前产物。只有校验通过的登记产物为 `current`，这个词表示与当前输入一致，不表示项目条件已经落实或方案最优。

## 定稿和导出前同时检查两件事

`verify-final-run RUN` 检查历史文件及选择绑定是否完整。它在用户更改当前资料后仍可能通过，这是正确的历史校验结果。

案例内的 `finalize` 自动检查当前登记比较、基准参数、证据、合同、方案集及输入/来源是否变化。

收到用户对当前候选的明确选择且计算依据未改变时，将选择记录保存到新的 `selections/selection-NNNN.json`。选择范围与是否模拟分别记录：

- `selection_scope=conditional_research`：用户明确选定这组研究假设，允许实施条件继续为 `pending`，完整重算并保留责任方、前置条件与失败退路。数值约束、固定边界、可比口径和模型边界必须通过。成果是选定条件研究，不是已批准实施。
- `selection_scope=implementation`（旧记录缺省同此）：沿用全部实施条件已有核验登记的门禁；CLI仍不代替外部资格与审批认证。
- `purpose=workflow_validation`：模拟验收用途，与上述范围独立；不能据此跳过任何约束或伪造条件满足。

使用选择记录helper的 `--selection-scope conditional_research` 时，必须有对应的明确用户选择原话；不能为了绕过条件门禁自行改变确认范围。

记录“收到选择、正在完整重算”这一轮时，仍须显式绑定当前比较，不能先用无产物轮次撤掉它，再尝试定稿：

```bash
wwtp-fin case checkpoint CASE --stage 3 --message CASE/responses/user-selected.md --response CASE/responses/finalizing.md --kind comparison --artifact CASE/comparisons/compare-0001/output/scheme-comparison.json --schemes CASE/comparisons/compare-0001/scheme-set.yaml
wwtp-fin finalize --comparison CASE/comparisons/compare-0001/output/scheme-comparison.json --selection CASE/selections/selection-0001.json --contract CASE/input/decision-contract.yaml --evidence CASE/input/evidence.json -o CASE/runs/run-0002
```

此时当前产物仍是比较，不会提前显示为最终成果。计算完成后登记新选定产物：

```bash
wwtp-fin case checkpoint CASE --stage 3 --message CASE/responses/user-selected.md --response CASE/responses/selected-result.md --kind selected --artifact CASE/runs/run-0002
wwtp-fin verify-final-run CASE/runs/run-0002 --case CASE
```

带 `--case` 的验证还要求该运行仍是当前选定成果。Word或图表交付前要做这道检查；报告编写期间的新信息若影响计算，应先返回建模和比较，不能修改已验证旧成果或把旧表继续混入新报告。

台账提供可追溯性和当前性，不鉴定来源真伪，也不证明agent理解材料正确。它不常驻监视文件；agent在收到更改后、每次回复和导出前执行检查并刷新当前入口。人工直接打开旧导出件仍在查看历史版本，因此对外发送时应引用当前入口及明确运行编号。
