# 输入字段速查

字段真源是当前 schema，而非本页。先生成 schema，再按 `description`、必填项、枚举与 `x-cross-field-constraints` 核对；本页只按领域分组，不能据此补默认值。

```bash
wwtp-fin schema --kind input -o schema-out
wwtp-fin schema --kind project-evidence -o schema-out
```

## 计算参数

| 字段域 | 主要字段 | 说明 |
| --- | --- | --- |
| 项目与期间 | `project_name`、`mode`、`concession_years`、`evaluation_date` | 运营期不含建设期。 |
| 声明口径 | `calculation_basis`、`declared_basis` | 前者影响计算；后者用于呈现与追溯。 |
| 建设与资产 | `capital`、`transfer_price_wan`、`terminal_value_method` | 建设计划、资产、提款、更新资产与期末事件在此闭合。 |
| 水量与服务 | `design_capacity_m3d`、`vol_segments`、`water`、`billable_cap_*` | 需求、处理、计费、成本驱动口径分开声明。 |
| 收入与成本 | `tariff_*`、`revenue`、`opex_items`、`other_taxes` | 价格、调价、成本关系和税率必须有材料依据。 |
| 融资与税务 | `financing_declaration`、`loan_*`、`vat_*`、`cit_mode` | 缺融资或资格资料时登记未决，不按惯例填充。 |
| 评价 | `financial_benchmarks`、`discount_rate`、`sensitivity_*` | 基准须附口径、来源、日期、提供方和证据状态。 |
| VfM | `vfm_*` | 仅显式输入齐备时产出。 |

## 项目证据

| 字段 | 用途 |
| --- | --- |
| `decisions`、`required_decisions` | 非财务裁决及其判据。 |
| `supporting` | 可引用证据；表格使用 `table_role`、`value.columns` 和 `value.rows`。 |
| `unresolved`、`required_user_inputs` | 不可转换、待核或必须补齐的内容。 |
| `consulting_claims`、`fact_sources` | 已提供事实和可追溯主张。 |
| `normative_profile` | 规范登记及其证据状态。 |
| `declared_scalars`、`deliverable_profile` | 已声明数值对账与成果配置。 |

字段不存在、语义不明或材料缺值时，写入转换日志并登记未决；不要为了通过校验而选枚举、补零或倾倒原始材料。详见 [INTAKE](INTAKE.md)。
