# wwtp-fin 公开契约面

本页是 CLI、已导出 schema 与测试共同定义的公开面。字段以当前 schema 为准；变更公开命令、退出码、告警或 schema 后，运行 `python scripts/export_schemas.py` 并更新本页。

## 输入与成果 schema

| `schema --kind` | 标识 | 用途 |
| --- | --- | --- |
| `input` | `wwtp-fin/input/1` | 项目计算参数；YAML 或 JSON 均可作为 CLI 参数文件。 |
| `project-evidence` | `wwtp-fin/project-evidence/1` | 项目证据、未决、规范登记和成果配置。 |
| `input-warnings` | `wwtp-fin/input-warnings/1` | `build` 产生的输入形状告警。 |
| `deliverable` | `wwtp-fin/deliverable/1` | 成果包清单与质量结论。 |
| `scheme-set` | `wwtp-fin/scheme-set/1` | 使用者明确给出的有限候选方案、目标、硬约束、代价与责任。 |
| `decision-contract` | `wwtp-fin/decision-contract/1` | 跨轮次复用的目标、比较口径、固定参数、硬约束与实施条件。 |
| `scheme-selection` | `wwtp-fin/scheme-selection/1` | 用户对具体比较和完整候选参数的确认记录；模拟验收单独标记。 |

```bash
wwtp-fin schema --kind input
wwtp-fin schema --kind project-evidence
wwtp-fin schema --kind input-warnings
wwtp-fin schema --kind deliverable
wwtp-fin schema --kind scheme-set
```

输入字段与跨字段约束见 [字段速查](spec-reference.md)；材料转化规则见 [INTAKE](INTAKE.md)。

## 子命令

| 命令 | 输入 | 主要输出 |
| --- | --- | --- |
| `intake` | `-p` 不完整参数草稿，可选 `-o` | 缺参问题、建议条件与输入就绪状态；不自动填值。 |
| `run` | `-p` 参数文件，可选 `--evidence` | stdout 或 `run.json`：计算、检查、分析、决策、表格数据与证据。 |
| `build` | `-p`、`--evidence`、`-o` | 可核验财务咨询成果包：完整机器语义 `document.json`、财务核心稿 `report.md`、计算结果、质量、告警、表格与图表语义。 |
| `solve` | `-p` 与目标/变量 | 一维反求结果；无解时返回 4。 |
| `sensitivity` | `-p` | 敏感性表与排序。 |
| `compare` | `-p`、`--schemes`、`-o` | 有限候选逐案重算、硬约束检查、机械排序及责任/审批披露；最终选择仍需用户确认。 |
| `finalize` | `--comparison`、`--selection`、`--contract`、`--evidence`、`-o` | 按明确选择重新计算完整成果，写入输入快照和 `final-run.json`，不覆盖旧运行。 |
| `verify-final-run` | 最终运行目录 | 检查选择、合同、参数、证据、软件身份与完整成果文件的绑定。 |
| `check` | `-p` | 财务一致性检查；可写 `checks.json`。 |
| `schema` | `--kind` | 指定公开 JSON Schema。 |
| `capability` | 可选 `--mode` | 能力矩阵与模式就绪度。 |
| `verify-deliverable` | 成果包目录 | 工件、引用与清单闭合校验。 |

`run` 是唯一计算契约；`build` 只消费其可序列化结构化结果，是唯一完整成果契约。

`finalize` 复用 `run`/`build` 的完整计算链，始终包含表格、敏感性和决策边界；它是选定方案的文件编排入口，不是另一套财务引擎。

`compare --contract ... --evidence ...` 将决策合同和证据绑定到比较。合同硬约束自动加入，不能被候选文件遗漏；目标冲突、未知指标为输入错误；固定参数被改变的候选不可行。`conditions` 用 `pending/satisfied/not_applicable` 记录实施条件，后两者必须有依据说明。

用户可以明确选择维持基准：另设候选 ID，使用空 `overrides: {}`，完整登记其理由、代价与条件，照常接受同一合同检查。自动附带的 `base` 行仅作参照，不自动表示来源已核验或已获选择。

兼容性：未传合同的旧 `compare` 仍可探索并按数值目标排序，`feasible` 仅代表已声明的数值/固定边界通过，不代表项目已审批。新增 `numerically_feasible`、`readiness`、`eligible_for_selection` 和 `selectable_shortlist` 分别披露状态；未绑定合同的探索不能 `finalize`。退出 0 只表示存在数值可行候选，不能据此推定有可定稿方案。所有比较输出目录必须为空。

选择哈希采用 UTF-8、排序键、紧凑分隔符的规范 JSON。二进制用户可通过 skill 附带的 `record-selection.py` 记录已发生的确认。最终运行绑定实际计算代码/配置、Python 与 YAML 版本；计算环境变化应重新比较，历史 `verify-final-run` 不要求安装原版本。哈希用于追踪一致性，不是对确认人的身份认证或对资格、审批的独立证明。

## 退出码

| 代码 | 含义 |
| ---: | --- |
| 0 | 命令成功；输入形状告警不改变退出码。 |
| 1 | 参数、文件或成果包校验错误。 |
| 2 | `run` 或 `check` 的财务一致性检查未通过。 |
| 3 | `build` 已写出成果包，但质量门禁未通过。 |
| 4 | `solve` 未求得可行解，或 `compare` 没有满足全部硬约束的候选。 |

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
| `D7-09` | 支撑证据缺少日期或提供方，已登记待补且不能支持确定裁决。 |

## 确定性承诺

- 同一输入不依赖系统当前日期；`evaluation_date` 可缺省，未给 `base_calendar_year` 时只输出相对期间；显式 `base_calendar_year` 仅作展示轴，不成为评价日或政策证据日期，日期相关裁决保持未决。
- `document.json` 保留完整机器语义；`report.md` 只确定性投影财务计算、分析、裁决和待补数据，不冒充完整项目咨询报告。
- 凡参与财务裁决或会改变用户决策的计算主题，`report.md` 必须给出数值、口径和解释；纯中间序列、模型自检计数和审计结果只保留在 `result.json`、`document.json` 与技术表中。
- `quality.json.checks.financial_narrative_complete` 同时检查计算主题分析与裁决指标覆盖；缺任一项时 `build` 以质量门禁失败结束。
- 同一输入产生逐字节一致的成果包；表、图、证据和引用必须闭合。
- 财务计算不自行证明政策资格、模式适用性或项目必要性；未决必须保留为未决。
- `compare` 只运行输入中明确列出的候选，不搜索参数空间；目标排序不替代项目依据、审批或用户确认。

## 报告编排元数据

`tables/index.json` 使用 `wwtp-fin/table-index/3`。原始 CSV 表头仍是稳定机器字段；
索引中的 `columns[]` 提供对应展示列名、单位、格式、展示优先级、位置与是否可直接用于报告的标志。
`priority` 取 1/2/3，分别表示主要展示列、说明列和技术列；它只帮助下游组织内容，
不改变 CSV 机器字段或计算结果。
`report_role` 只表达默认用途：`body` 可进入正文，`appendix` 是待选择的客户附表，
`workpaper` 是完整成果包中的技术底稿，`audit` 仅供核验。下游必须先组织咨询逻辑，
不能把技术底稿、审计表或全部附表机械拼接成报告。

产品边界见 [boundary.md](boundary.md)，三阶段职责与验收见 [THREE_STAGE_PRODUCT.md](THREE_STAGE_PRODUCT.md)。
