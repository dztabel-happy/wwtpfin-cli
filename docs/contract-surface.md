# wwtp-fin 公开契约面

本页是 CLI、已导出 schema 与测试共同定义的公开面。字段以当前 schema 为准；变更公开命令、退出码、告警或 schema 后，运行 `python scripts/export_schemas.py` 并更新本页。

## 四份 schema

| `schema --kind` | 标识 | 用途 |
| --- | --- | --- |
| `input` | `wwtp-fin/input/1` | 项目计算参数；YAML 或 JSON 均可作为 CLI 参数文件。 |
| `project-evidence` | `wwtp-fin/project-evidence/1` | 项目证据、未决、规范登记和成果配置。 |
| `input-warnings` | `wwtp-fin/input-warnings/1` | `build` 产生的输入形状告警。 |
| `deliverable` | `wwtp-fin/deliverable/1` | 成果包清单与质量结论。 |

```bash
wwtp-fin schema --kind input
wwtp-fin schema --kind project-evidence
wwtp-fin schema --kind input-warnings
wwtp-fin schema --kind deliverable
```

输入字段与跨字段约束见 [字段速查](spec-reference.md)；材料转化规则见 [INTAKE](INTAKE.md)。

## 子命令

| 命令 | 输入 | 主要输出 |
| --- | --- | --- |
| `run` | `-p` 参数文件，可选 `--evidence` | stdout 或 `run.json`：计算、检查、分析、决策、表格数据与证据。 |
| `build` | `-p`、`--evidence`、`-o` | 完整咨询内容包：`document.json`、`report.md`、`result.json`、`quality.json`、`warnings.json`、表格与图表语义。 |
| `solve` | `-p` 与目标/变量 | 一维反求结果；无解时返回 4。 |
| `sensitivity` | `-p` | 敏感性表与排序。 |
| `check` | `-p` | 财务一致性检查；可写 `checks.json`。 |
| `schema` | `--kind` | 指定公开 JSON Schema。 |
| `capability` | 可选 `--mode` | 能力矩阵与模式就绪度。 |
| `verify-deliverable` | 成果包目录 | 工件、引用与清单闭合校验。 |

`run` 是唯一计算契约；`build` 只消费其可序列化结构化结果，是唯一完整成果契约。

## 退出码

| 代码 | 含义 |
| ---: | --- |
| 0 | 命令成功；输入形状告警不改变退出码。 |
| 1 | 参数、文件或成果包校验错误。 |
| 2 | `run` 或 `check` 的财务一致性检查未通过。 |
| 3 | `build` 已写出成果包，但质量门禁未通过。 |
| 4 | `solve` 未求得可行解。 |

## 告警 ID

告警写入 `build` 的 `warnings.json`，不计入 `quality.counts`，也不单独改变退出码。

| ID | 含义 |
| --- | --- |
| `D7-01` | 支撑表形状或 `table_role` 不合格，已跳过。 |
| `D7-02` | `fact_sources` 的事实容器未识别，已跳过。 |
| `D7-03` | 泵站、时间线或风险通道的近似输入缺关键键，已跳过。 |
| `D7-04` | 自用能源批次缺效应输入，或资本性投入无到位批次。 |
| `D7-05` | 融资声明不可计算或还款未决，贷款参数已忽略。 |
| `D7-06` | 大体量事实载荷已从正文折叠，原值保留在数据层。 |
| `D7-07` | 含税建设投资的进项倒算未译为抵扣字段。 |
| `D7-08` | 建设投放比例声明与纳入测算的比例不一致，已并列披露。 |

## 确定性承诺

- 同一输入不依赖系统当前日期；`evaluation_date` 是日期判断基准。
- `document.json` 是正文语义权威，`report.md` 只能作确定性投影。
- 同一输入产生逐字节一致的成果包；表、图、证据和引用必须闭合。
- 财务计算不自行证明政策资格、模式适用性或项目必要性；未决必须保留为未决。

产品边界见 [boundary.md](boundary.md)，实现与门禁见 [development.md](development.md)。
