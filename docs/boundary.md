# wwtp-fin ↔ DocxKit ↔ ChartKit 边界

> wwtp-fin 负责“结构化项目材料 → 可核验咨询语义”；DocxKit 负责“语义 → Word”；ChartKit 负责“数据与图表 brief → 图片”。三者只在文件和 agent 层交接，不互相调用。

## 职责边界

| | wwtp-fin | DocxKit | ChartKit |
| --- | --- | --- | --- |
| 负责 | 参数、证据、计算、检查、裁决、报告语义、表格数据、图表 brief | 章节排版、样式、页眉页脚、目录、图表编号、`.docx` | 数据图的图型、轴、图例、样式与图片导出 |
| 输入 | 项目参数与项目证据 | 由 `document.json` 转出的 `report.json`、表格、图片资产 | 图表 brief 与对应 CSV/结构化表 |
| 输出 | `document.json`、`report.md`、`result.json`、tables、figures briefs、质量与告警 | `.docx` | PNG/SVG/PDF 等图片与题注 |

```text
材料 → INTAKE → wwtp-fin build
                 ├─ document.json → report.json → DocxKit → .docx
                 └─ figures/*.json briefs + figures/data/*.csv → ChartKit → 图片
                                                        │
                                      图片路径 + 题注 ──┘
```

`build` 不启动 DocxKit 或 ChartKit；`document.json` 也不会自动变为 DocxKit 的 `report.json`。下游也不重算财务结果或替换裁决。交接字段、示例命令见 [examples/handoff/README.md](../examples/handoff/README.md)。

## wwtp-fin 不做什么

- 不把材料改写成完整的咨询文笔、工程设计理由、现场调查、方案比选或规范原件；这些是项目材料或下游报告作业。CLI 只呈现已结构化并有出处的事实、计算和裁决语义。
- 不输出 Word、PDF、图片或版式；不包含 Office 提取器、原始文件校验、报告模板和 benchmark 材料。
- 不以行业惯例补齐缺失融资、税务资格、基准收益率、授权或项目事实；应登记 `unresolved`、`required_user_inputs` 或 `declared_basis`。
- 不把 `report.md` 当作可自由续写的草稿；`document.json` 与其 Markdown 投影必须一致。
- 不把“模式名称”当作算法开关，不按项目专名、旧表格或案例答案分支。

## 当前能力边界

| 范围 | 当前状态 |
| --- | --- |
| 概率分析 / 蒙特卡洛 | 未实现。 |
| 长期资产混合用途进项税调整 | 未实现；输入触及该组合会硬失败，不以经营期收入比例替代。 |
| 建设期利息非资本化 | 未实现；不以零利息替代。 |
| 运营期新增长期贷款提款 | 未实现；长期贷款仅在初始融资时点形成。 |
| 多方案/多情景组编排 | 未接通。现有 `sensitivity` 是单项目因素重算；财务基准可逐情景比较，但不构成方案组编排器。 |
| VfM | 仅在显式提供 PSC/PPP 所需输入时输出；缺 `vfm_opex_uplift` 或政府投资即不产出，不替代完整法定 VfM 资料与论证。 |
| 地方税 | 房产税、城镇土地使用税、印花税可逐年输入并声明可扣除性；不自动按地方规则推导。 |

完整能力矩阵用 `wwtp-fin capability` 实时查看；输入和成果语义以 CLI 导出的 schema 为准。
