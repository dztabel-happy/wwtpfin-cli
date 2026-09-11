<h1 align="center">wwtp-fin</h1>
<p align="center">从项目资料到方案比较，再到选定方案的完整财务成果</p>
<p align="center"><a href="README.md">English</a> · <a href="#安装">安装</a> · <a href="#快速开始">快速开始</a></p>

为污水处理项目咨询服务。你提供可研、初步方案或运营资料，并说明希望改善的成本与实施条件；业务人员和 agent 研究有依据的措施，wwtp-fin 计算各方案的财务影响，在你选择后输出同一参数版本的完整计算成果。

三阶段分别交付：有来源的测算基准；包含成本、条件和责任的候选方案；选定方案的财务报表、敏感性分析与可核验成果包。Word 报告和图表可继续交给 DocxKit、ChartKit。

## 安装

### 1. 安装 CLI

```bash
npm install -g @dztabel/wwtpfin
wwtp-fin --version
wwtp-fin --help
```

支持 macOS Apple Silicon、Linux x64 和 Windows x64。本分支的三阶段流程要求 0.2.0；发布状态见 [更新记录](CHANGELOG.md)。

### 2. 安装 agent skill

Codex 用户执行以下命令，将两项 skill 复制到用户技能目录。更新 CLI 后重新执行以同步 skill。

```bash
node -e 'const fs=require("node:fs"),p=require("node:path"),os=require("node:os"),cp=require("node:child_process"); const root=cp.execSync("npm root -g",{encoding:"utf8"}).trim(); for(const name of ["wwtpfin-consulting-core","wwtpfin-consulting-report"]) fs.cpSync(p.join(root,"@dztabel/wwtpfin/skills",name),p.join(os.homedir(),".agents/skills",name),{recursive:true});'
```

Claude Code 用户将命令中的 `.agents/skills` 替换为 `.claude/skills`。重新打开会话，在技能列表中确认 `wwtpfin-consulting-core` 和 `wwtpfin-consulting-report` 可见；同时确认 CLI 帮助中有 `compare`、`finalize` 和 `verify-final-run`。

## 快速开始

### 从可研开始研究降本

Codex：

> $wwtpfin-consulting-core 阅读这些项目资料，先建立有来源的基准，再研究建设期和运营期降本措施。保持服务要求，分别说明措施的依据、适用条件、全周期影响和责任，重算组合供我选择。

Claude Code 使用 `/wwtpfin-consulting-core`，后面的请求相同。

### 找到一条新依据后继续迭代

> $wwtpfin-consulting-core 分析这条新政策是否适用于本项目。说明关联参数与必要条件，计算采用和不采用的影响，再与现有措施组合比较。

### 选择方案并生成成果

> $wwtpfin-consulting-core 我确认采用这次比较中的方案 B。请按该方案完整参数重新计算并校验最终成果。

如果方案仍有未满足的约束或实施条件，系统会指出具体事项。需要 Word 时继续：

> $wwtpfin-consulting-report 根据刚才明确选定的最终运行和项目资料组织完整咨询报告，用 DocxKit 导出 Word。

Claude Code 使用相同名称的斜杠命令。单次基准测算、条件分析也可独立交付，并标明用途。

## 命令、示例与边界

- [三阶段职责](docs/THREE_STAGE_PRODUCT.md)：每阶段交付与选择规则。
- [可执行流程示例](examples/three_stage/README.md)：合成项目从比较到完整重算。
- [公开接口](docs/contract-surface.md)、[字段速查](docs/spec-reference.md)和[材料转化](docs/INTAKE.md)。
- [产品边界](docs/boundary.md)、[下游交接](examples/handoff/README.md)和[二进制分发](docs/binary-distribution.md)。

CLI 重算明确给出的候选及约束；政策适用性、工程实施条件和最终选择需要相应责任人判断。条件试算不等同于已核定方案，排序也不代表全局最优。

公开仓包含安装入口、文档、通用示例与 agent skills；核心源码不在此仓公开。软件采用专有许可（`UNLICENSED`），未授予开源许可。
