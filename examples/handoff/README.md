# wwtp-fin 下游交接示例

本示例只说明文件映射，不依赖或调用 DocxKit、ChartKit。

## 先生成最小完整成果包

```bash
.venv/bin/wwtp-fin build -p examples/minimal_complete/project.yaml \
  --evidence examples/minimal_complete/evidence.json -o handoff-out
.venv/bin/wwtp-fin verify-deliverable handoff-out
```

## 先组织报告

调用 `wwtpfin-consulting-report`，完整盘点语义块、表格和图表，先生成
`report-plan.json` 与有论证结构的 `report.md`。原始 `report.md` 是确定性咨询核投影，
不能直接全量转换为 Word。

| wwtp-fin 工件 | 报告编排用途 |
| --- | --- |
| `document.json` | 结论、分析、限定与建议的权威语义来源。 |
| `tables/index.json` 与表格数据 | 按 `report_role` 取舍，展示时使用 `columns[].label`。 |
| `figures/index.json` | 候选图；只选择能支撑正文结论的图。 |
| `quality.json`、`warnings.json` | 交付前复核；重大限制写入对应分析，不机械抄表。 |

完成编排后，ChartKit 先生成已选图，DocxKit 再消费组织后的 `report.md` 与图表资产。

DocxKit 只负责 Word 排版、目录、页眉页脚、图表编号和交叉引用；不得重新组织财务逻辑或续写未经证据支持的咨询结论。

```bash
jq '.quality_passed, (.files | length)' handoff-out/manifest.json
jq '.tables[0]' handoff-out/tables/index.json
```

## ChartKit 映射

| wwtp-fin 工件 | 交给 ChartKit 的用途 |
| --- | --- |
| `figures/index.json` | 每张图的 ID、题目、语义角色和 brief 索引。 |
| `figures/*.json` | 该图的 brief：数据意图、标题、题注与来源引用。 |
| `figures/data/*.csv` | 图表所需的可读数据；按 brief 选择，不重算指标。 |

agent 用 brief 选择图型并把 ChartKit 输出的图片路径和题注交回文档层；图片内部不写图号，图号与摆放由 DocxKit 完成。

```bash
jq '.figures[0]' handoff-out/figures/index.json
find handoff-out/figures -maxdepth 1 -name '*.json' ! -name index.json | sort | head -1
```
