# 输入字段速查

字段真源是当前 schema，而非本页。先生成骨架，再按 `description`、必填项、枚举与 `x-cross-field-constraints` 核对；本页只按领域分组，不能据此编造字段或补默认值。

```bash
wwtp-fin schema --kind input -o schema-out
wwtp-fin schema --kind project-evidence -o schema-out
```

## `wwtp-fin/input/1`：计算参数

| 字段域 | 主要字段 | 说明 |
| --- | --- | --- |
| 项目与期间 | `project_name`、`mode`、`concession_years`、`evaluation_date`、`base_calendar_year` | 期限和模式必须明确；运营期不含建设期。评价日可缺省；未给日历基年时只输出相对期间，显式日历基年仅作展示轴，不成为评价日或政策证据日期；日期相关裁决保持未决。 |
| 声明口径 | `calculation_basis`、`declared_basis` | 前者影响计算；后者用于呈现、对照与追溯，不替代计算字段。 |
| 建设与资产 | `capital`、`transfer_price_wan`、`terminal_value_method` | 建设计划、资产、提款、IDC、费用化利息、更新资产、长期资产进项税调整与期末事件在此域闭合。 |
| 水量与服务 | `design_capacity_m3d`、`vol_segments`、`water`、`billable_cap_*` | 需求、处理、计费、成本驱动口径分开声明。 |
| 收入 | `tariff_*`、`revenue`、`tariff_escalation` | 收入机制、价格、调价和资金来源必须分开。 |
| 成本 | `opex_items`、`opex_step_escalation`、`other_taxes`、`self_generation` | 每个成本项的水量关系、增长、税率和显式年度金额应如实填写。 |
| 融资 | `equity_ratio`、`loan_*`、`loan_tranches`、`operating_loan_tranches`、`financing_declaration` | `loan_tranches[].principal_repayment_schedule_wan` 可按真实贷款承接逐年非均匀还本，不得同时填写该笔期限、宽限期或公式还款方式，也不得伪造 bullet 分档；运营期专项贷款必须绑定同年资本性投入；缺融资资料时声明不可用并登记未决，不以惯例填充。 |
| 税务 | `vat_*`、`cit_mode`、`income_tax`、`capital_grants` | 计税方式、优惠资格证据与金额计算分离。 |
| 评价 | `financial_benchmarks`、`discount_rate`、`breakeven_ratios`、`sensitivity_*` | 基准情景须附口径、来源、日期、提供方和证据状态；不运行敏感性分析时目标可省略且不产出空分析。 |
| VfM | `vfm_*` | 仅显式输入齐备时产出；不是多方案情景组。 |

## `wwtp-fin/project-evidence/1`：项目证据

| 字段 | 用途 |
| --- | --- |
| `decisions`、`required_decisions` | 非财务裁决及其判据登记。 |
| `supporting` | 可引用证据；结构化表使用 `table_role` + `value.columns` + `value.rows`。 |
| `unresolved`、`required_user_inputs` | 不可转换、待核或必须补齐的内容。 |
| `consulting_claims`、`fact_sources` | 已提供事实和可追溯主张。 |
| `normative_profile` | 规范文号、名称、日期、要点、适用范围和证据状态。 |
| `declared_scalars`、`deliverable_profile` | 已声明数值对账与成果包配置。 |

## 输出 schema

- `wwtp-fin/input-warnings/1`：根对象包含 `schema` 与 `warnings[]`；每条至少有 `id`、`path`、`message`。
- `wwtp-fin/deliverable/1`：成果包清单，包含项目名、评价日、工件列表与 `quality_passed`。
- `wwtp-fin/scheme-set/1`：有限候选方案、目标、硬约束、代价、责任、审批与证据定位；不触发自动搜索。

字段不存在、语义不明或材料缺值时，写入转换日志并登记未决；不要为了通过校验而选枚举、补零或把材料全文塞进叙事字段。详见 [INTAKE](INTAKE.md)。
