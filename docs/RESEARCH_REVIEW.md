# 研究与推荐约束

第二阶段的责任是从同一事实与目标出发，主动研究有依据的措施，测试会改变选择的假设，给业务人员一份可以判断的建议。一个正常案例内可以多次检索、比较和重算；不要求用户重开任务、点名政策或指出遗漏之后才补研究。

CLI 对有限候选进行确定性计算并核对已登记的研究。它不判断原文真伪、政策是否实际适用、工程方案是否穷尽，也不证明全局最优。研究记录通过不是专业判断的替代品。资料仍不足时，应给出已测的条件分支与下一步取证价值，不编造唯一最优方案。

## 与现有三阶段的关系

第一阶段准备参数、证据和独立的决策合同；第二阶段在原有方案集增加 `research`，由 `compare` 输出 `research_review`；第三阶段在用户明确选择后，沿用 `finalize` 完整重算与历史绑定。没有新增阶段或新增 skill。资料、目标或关键假设改变时返回前阶段，当前入口与旧成果处理沿用[案例工作流](CASE_WORKFLOW.md)。

```bash
wwtp-fin schema --kind scheme-set
wwtp-fin schema --kind decision-contract
wwtp-fin schema --kind scheme-selection
wwtp-fin compare -p input/project.yaml --contract input/decision-contract.yaml --evidence input/evidence.json --schemes comparisons/compare-0001/scheme-set.yaml -o comparisons/compare-0001/output
```

以当前安装版本导出的 schema 为字段权威。旧的无 `research` 方案集仍可试算，比较会明确显示尚未研究，不能借数值排序直接进入选定成果。

## 先明确如何判断“更好”

决策合同的 `objective` 是主目标，可选的 `secondary_objectives` 为至多三项有序次级目标。每项使用 `metric`、`direction`、`basis`，可选非负绝对 `tolerance`，单位与该指标一致，缺省为零。

每次比较先保留与当轮主目标最优值相差不超过其 `tolerance` 的候选，再对这一组按次级目标依次处理。最后仍可有并列。容差是有依据的无差异范围，不能改变硬约束、补救计算错误或为指定候选放宽标准。多个目标不跨口径相加，也不暗设权重；未登记的次级目标不用于自动打破并列。

候选列表、CLI 摘要与每个研究情景共用这一排序算法。`ranking_groups` 按优先顺序列出并列组，`shortlist` 仅将各组展开；同组按 ID 排列是稳定展示，不构成偏好。`best_candidates` 是完整首组；旧字段 `best_by_objective` 仅在首组唯一时给出 ID，并列时为 `null`。这些字段描述本情景内的数值排序；研究情景还排除模型未闭合候选，实际推荐须继续检查共同情景与实施条件。

主目标、服务边界和硬约束保持一致。降低资源投入、降低项目资金支出和改变财政支付时点可能是不同结果；若实际推荐依赖其中另一项，应在比较前说明主次与取舍并更新合同，不能算完后更换判据。

## `research` 输入

`research` 由 `directions`、`assumptions`、`scenarios`、`combinations` 和非空 `stopping_reason` 组成。它直接放入当前方案集，供计算与选择绑定，不再要求另建一套同内容台账。来源文件和工程推导仍保留在原有证据与底稿中。

四类条目的 `evidence_refs` 均须唯一解析到本次绑定 `evidence.supporting[].evidence_id`。只写一个文件名、URL或不存在的编号不等于登记证据；先把实际原文、估算底稿或计算记录放入 supporting，再引用其 ID。缺失、重复或仅在 unresolved 中的引用使 `research_evidence_review.passed=false`，保留计算而阻止收口。普通估算可继续标为 `unverified`，不要求伪装成已核验事实，也不要求全部材料使用下述严格来源快照。引用可解析不证明原文理解、估算方法或政策适用正确。

`user_bound: true` 只用于用户实际固定的设计选择；其全部关联路径和值必须同时由决策合同 `fixed_parameters` 覆盖，基准与候选保持相同。产品验证合同与研究是否一致，不认证录入者声称的用户确认真实；用户的原话及来源仍须保留。

### 方向及措施

`directions[]` 每条包含 `id`、`domain`、`status`、`candidate_ids`、`paths`、`basis`、`evidence_refs`，结构排除另带 `exclusion`。六个通用域均需处置；同一域可以有多条具体方向：

| `domain` | 审查问题 |
|---|---|
| `service_demand` | 服务范围、处理量、负荷与质量要求是否理解正确，有无有依据的需求或时序方案？ |
| `capital_and_renewal` | 建设规模、工程组织、设备更新与期末处理是否有可研究的替代？ |
| `operations` | 能耗、药耗、人员、维护及处置方式有哪些可验证的改进？ |
| `tax_and_support` | 税费与支持政策是否有效且适用，金额、时序与资格条件怎样影响方案？ |
| `financing_and_payment` | 融资、还本、拨付和资金安排是否闭合，是否影响已声明目标及风险？ |
| `delivery_and_contract` | 实施模式、服务分工、采购和合同责任是否提供可执行的替代？ |

`status` 使用 `evaluated`、`excluded`、`open` 或 `not_applicable`。数值较差、收益较小或暂不采用的方向仍为 `evaluated`：关联完整反事实候选、实际变化路径和共同情景，保留为什么不选它的计算。关联路径须在至少一个关联候选或共同情景中相对该情景基准实际变化；候选不能有计算错误、未支持模型、不可比口径或缺失目标值。真实算出的硬约束失败可以保留为有用反例，不应伪装成结构排除。`excluded` 和 `not_applicable` 仅用于来源支持的结构排除，须提供下述 `exclusion`，不能拿某单项表现不好代替。仍有待研究的有价值方向保持 `open`。六域是检查覆盖面的提示，不是固定杠杆目录或每案必须生成六套方案的数量要求。

`paths` 记录该方向解释的规范化参数路径，数组项可用数字索引；应尽量贴近实际变化。候选相对基准的每项参数变化，必须由关联的已研究方向路径或下面的假设路径解释。不要用过宽父路径掩盖无关变化。

### 结构排除与来源快照

`excluded` / `not_applicable` 方向，以及 `result_candidate_id: null` 的组合，在收口时需要 `exclusion`。对象包含：

| 字段 | 含义 |
|---|---|
| `kind` | 固定为 `source_rule`；来源支持的法律、合同、工程或其他结构限制。 |
| `scope_candidate_ids` | 排除所适用的真实候选 ID。方向须覆盖本轮全部候选（含自动加入的 `base`）；组合须恰好对应该条的 `candidate_ids`。 |
| `applicability` | 来源规定如何对应本项目事实、实施主体或参数安排。 |
| `exceptions` | 相关允许安排、例外和处理说明；没有适用例外也须说明核查结果。 |

新增候选会改变方向排除的范围，不能静默继承旧判断。范围字段只是机械核对范围声明，不能使过宽的解释变得成立。一个来源只限制某种融资或实施安排时，不能直接排除同名政策或模式的全部变体。

`exclusion` 沿用该方向或组合的 `evidence_refs`，其中每项都必须解析到 `evidence.supporting[]` 的来源快照；不能混入只有标题或未取得正文的所谓支持证据。普通推理写在 `basis`，所依赖的工程、合同原文也可以登记快照。支持排除的记录使用 `value.type: source_snapshot`：`text` 是保存的连续完整来源正文，`sha256` 是该正文 UTF-8 字节的 SHA256；`citation` 包含 `start`、`end`、`text` 和 `locator`。引文区间按 Python Unicode 码点计数、左闭右开，`citation.text` 必须等于正文的精确切片，定位说明为条款、页段或表格位置。原有 `source`、`as_of` 等元数据保留在 supporting 记录外层。排除证据须有非空来源定位，以及按来源实际精度填写的 `YYYY-MM` 或 `YYYY-MM-DD` 日期；不能用抓取日冒充文件生效日。

下面从已取得的 UTF-8 来源文本及核对过的引文范围生成 `value`，不会生成项目适用性判断。命令参数依次为来源文本路径、起止码点和定位说明：

```python
from pathlib import Path
import hashlib, json, sys

text = Path(sys.argv[1]).read_bytes().decode("utf-8")
start, end = map(int, sys.argv[2:4])
assert 0 <= start < end <= len(text)
value = {
    "type": "source_snapshot",
    "text": text,
    "sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
    "citation": {
        "start": start, "end": end,
        "text": text[start:end], "locator": sys.argv[4],
    },
}
print(json.dumps(value, ensure_ascii=False, indent=2))
```

来源正文应来自实际取得的原文或附件，保留完整相关条款及限定语；不能把摘要或 Agent 自写结论改名为原文。CLI 不要求另设外置文件路径字段，只检查嵌入记录存在、正文哈希、引文切片及范围声明一致，不认证正文真实性、法律效力、上下文是否充分或适用解释正确。政策存在和项目资格成立仍是两件事。缺附件、条款未读或含义未决时可继续条件试算，不能据此关闭另一条路径。

### 事实、估算与设计选择

`assumptions[]` 每条包含 `id`、非空 `paths`、`kind`、`basis`、`evidence_refs`、`material`、`scenario_ids`，可选 `user_bound`。`kind` 为 `source_fact`、`estimate` 或 `design_choice`。

来源事实必须保留范围和限定语。设计能力不等于年均处理量，整体成本不等于新增项目成本，资产寿命不等于项目日历年份。原文没有建立所需含义时，估算须说明推导方法，不能仅引用原文件名便把推导结果归为事实。缺少 Excel 不阻止基于工程量、适用定额、地区价格或明确研究提案开展测算。

`material` 表示该假设是否可能影响目标、可行性或选择，须由研究者说明判断依据，不能为通过检查随意改为 `false`。重要估算须有应用到全部候选且实际改变参数的有效情景。重要设计选择须通过实际候选或情景研究；若用户明确固定，才可用 `user_bound: true` 并在依据中绑定该选择。Agent 提出的默认值不是用户固定值。

不确定性可能来自数值也可能来自方法。一个估算方法上下小幅浮动，不能代替对另一种合理来源解释或推导方法的比较。情景数量应服务于这些真实问题。

### 共同情景及工程派生

`scenarios[]` 每条包含 `id`、非空 `assumption_ids`、`basis`、非空 `evidence_refs` 和非空 `overrides`；最多十二项，`baseline` 为保留 ID。情景与假设通过 `assumption_ids`、`scenario_ids` 双向引用。

`overrides` 采用现有参数覆盖结构，在各候选参数之后应用。对象字段递归合并；候选、共同情景及派生覆盖中的数组字段（如 `opex_items`）须提供完整数组并整体替换，不支持数字键稀疏覆盖。同一情景代表对全部候选相同的外部条件或估算解释，不能让某候选偷偷恢复自己的有利取值。情景只能改变所关联假设的路径，不能修改决策合同固定参数。需要变更固定边界时，返回第一阶段修改合同并重新比较。

工程关系需要按方案重新推导时，可以添加 `candidate_overrides`：键是候选 ID，值包含 `overrides` 与说明工程推导的 `basis`。派生变化仍须在关联假设路径内，不得改写共同冲击的同一变化路径，也不能夹带新措施。费用与数量、设备配置、时序等相互关联时，应实际重算关联字段；CLI 校验路径与计算，不验证该工程推导是否正确。

情景结果保留每个候选的指标、可行性、约束、口径、模型限制和参数哈希，不能只保存赢家。某条件失效导致方案不可行是有用结果；参数错误或不完整情景无法完成计算，需要修复后才能收口。全体候选都未受实际影响的“情景”不能充当重要估算测试。

### 组合与收口

`combinations[]` 每条包含至少两个 `candidate_ids`、`result_candidate_id`、`basis` 与非空 `evidence_refs`。可以组合时，`result_candidate_id` 指向另一条已完整计算的候选；数值较差也要保留这个实际结果。只有来源支持的结构不兼容才使用 `null`，并给出完整 `exclusion` 和来源快照。登记本身不证明完整组合的参数构造正确，Agent 仍须检查相互作用。不得把独立节约额相加作为组合结果，也不得以某单项表现差宣称其全部组合不会更好。

组合替代原措施时，使用可选 `replaced_candidate_ids` 显式列出被替代的单项候选 ID。例如已有工程措施加银行贷款，再改用专项债，组合成员可以引用旧完整方案和专项债候选，但必须移除旧银行贷款单项。CLI 递归展开有效措施，拒绝循环谱系、同一结果相互矛盾的定义，以及仍包含已声明互斥措施的组合。替代项只能来自该组合继承的单项，不能随意删除无关候选。

CLI 自动检查所有已测情景赢家与剩余已研究单项的组合处置，输出 `combination_coverage`：已包含（`already_included`）、已有实际组合（`tested_combination`）、有依据排除（`excluded`）或尚未处理（`missing`）。缺失项会阻止进入选择，不能用“已有很多组合”或一句停止理由绕过。实际组合须具有准确的有效措施集合且改变参数；附带另一项措施的超集不能代替这项组合，换 ID 复制原参数也不能充数。已声明单项互斥可继承到包含它的完整方案，已被替代掉的措施不参与继承。选择非赢家时，`finalize` 对该候选执行同样检查。

这项检查只针对当前已有措施与优选候选，不枚举全部子集，也不声称发现了所有外部政策。CLI 验证声明的组合谱系、引用、排除来源快照和实际计算，不能验证工程合并或排除理由的事实真伪。新组合改变赢家后，需要继续处置新赢家剩余的措施；未落实的真实实施条件仍保留为条件，不能为收口伪造互斥。

只有在全部已测情景均没有参数差异时，原基准才不作为新增措施。某措施或组合只在不利情景生效，也要保留并接受组合覆盖检查。省略自动基准、另建可按情景重新推导的基准候选时，可设置 `research.baseline_candidate_id`；该候选在基准情景的完整参数必须与比较基准一致，CLI会以它各情景的参数识别基准，不按名称猜测。

推荐前结合材料自查，反查最影响取舍的排除：完整条款中的允许部分或例外是否改变适用范围，完整反事实计算是否支持数值理由。一个税种、余额或会计科目为零，并不证明完整经济影响为零；关联税费、资产基数、融资和支付安排发生变化时须一并重算，不能只看单个字段。结论范围不得超过所读原文和实测范围。

`stopping_reason` 解释为什么当前研究足以支持建议、尚未覆盖的边界和重新研究的触发条件。数值全绿、菜单已经生成、候选数量够多或用户已选一项，都不是研究完成的理由。记录很少也可以充分；记录很多仍可能遗漏一个决定性的事实或方案。

## `research_review` 输出与使用

比较文件中的 `research_review` 提供 `status`、`ready_for_selection`、`issues`、`scenario_results`、`baseline_winners`、`robust_winners`、`recommended_candidates`、`assumption_tests`、`combination_coverage`、`source_exclusion_review`、目标与研究哈希。各情景的 `winners` 可以包含多个并列候选；`robust_winners` 为所有已测情景赢家集合的交集。

| 状态 | 含义及后续动作 |
|---|---|
| `not_assessed` | 没有研究登记，只有数值比较；继续研究。 |
| `incomplete` | 已登记研究仍有未处置方向、未解释变化、未行使的重要假设或其他问题；按 `issues` 继续修正。 |
| `no_feasible_candidate` | 研究检查完成，但基准条件下没有可选的非基准候选；分析控制约束，继续提出措施或有依据的边界调整。 |
| `stable_within_tested_scenarios` | 存在在所有已测情景中均位列赢家集合的方案；仅表示该有限范围内的稳定性，可能仍并列或有待落实条件。 |
| `conditional_on_assumptions` | 不存在覆盖全部已测情景的共同赢家；需要交付各条件下的选择及其理由，不能宣称稳健唯一最优。 |

`source_exclusion_review` 逐条输出作用范围、证据引用与问题，状态为 `source_reproduced` 或 `unsupported`。前者仅表示来源登记、正文哈希和引文能复现，不表示排除理由已获专业认证。未绑定 `--evidence`、证据缺失或重复、正文/引文不匹配、候选范围未覆盖都会阻止该排除收口。

`recommended_candidates` 是供审查的计算候选集合，不是自动替用户决策。即使 review 为稳定，真实来源误读、遗漏重大假设或错误工程估算仍应使 Agent 返回研究。若只有原基准稳定，说明新措施没有在已测范围内证明更好；若要选择维持原方案，也须作为明确可选候选记录，不能暗选一个试算。

候选原有的 `numerically_feasible`、`eligible_for_selection`、`eligible_for_research_selection` 及两个 shortlist 继续表达各自的数值、口径、模型和实施条件门禁。它们不包含完整的研究收口判断。`finalize` 另外要求 `research_review.ready_for_selection`，不能把旧的 `best_by_objective` 单点排序当作推荐证明。

## 选择与成果如何保留结论边界

向用户说明推荐理由、采用与不采用的影响、重要条件失效的结果以及会翻转排序的假设。不要让用户靠查看原始 JSON 才发现这些限制。可以选择条件方案，也可以基于明确取舍选择非共同赢家；选择记录保留 `decision_reason` 和 `acknowledged_research_status`，说明所作的决定，不能抹去翻转或将自选包装成稳健最优。

选择仍绑定具体比较、完整参数、决策合同、证据及软件身份；第三阶段重新核验研究并全量计算。`selection_scope=conditional_research` 允许保留待落实实施条件，不允许跳过不完整研究。选定后的 Word、图表和一页说明继承同一研究边界。新证据影响选择时返回研究并生成新比较，旧判断作为历史保留。

## 验收边界

机械验收检查共同情景确实重算、数值不采用有完整反事实候选、结构排除有可复现的来源引文、排序翻转与并列如实显示、无解释改参被拦截，以及不完整研究不能定稿。业务验收检查来源语义是否正确、方向和场景是否抓住重要问题、依据是否适用、建议是否值得采用。这两层都需要成立；“字段齐全”不能代替“一轮正常使用即可获得充分研究的建议”。
