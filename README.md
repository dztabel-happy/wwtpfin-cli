<h1 align="center">wwtp-fin</h1>
<p align="center">From project materials to scheme comparison and complete selected-scheme financial results</p>
<p align="center"><a href="README.zh-CN.md">中文</a> · <a href="#installation">Installation</a> · <a href="#quick-start">Quick Start</a></p>

For wastewater-project consulting. Supply feasibility studies, draft schemes or operating records and your cost objectives. Consultants and agents investigate supported measures; wwtp-fin calculates their financial effects and produces a complete, version-bound calculation package after you select a scheme.

The three stages deliver a sourced baseline; alternatives with costs, conditions and responsibilities; and full financial schedules, sensitivity analysis and verifiable results for the selected scheme. DocxKit and ChartKit can then produce Word reports and charts.

## Installation

### 1. Install the CLI

```bash
npm install -g @dztabel/wwtpfin
wwtp-fin --version
wwtp-fin --help
```

Supports macOS Apple Silicon, Linux x64 and Windows x64. This branch's three-stage workflow requires 0.2.0; see the [changelog](CHANGELOG.md) for release status.

### 2. Install the agent skills

Codex and Claude Code use the same two skills: [wwtpfin-consulting-core](skills/wwtpfin-consulting-core/SKILL.md) handles all three stages through complete recalculation; [wwtpfin-consulting-report](skills/wwtpfin-consulting-report/SKILL.md) compiles a formal report when requested.

For Codex, copy the two bundled skills into your user skills directory. Repeat after CLI updates to keep them synchronized.

```bash
node -e 'const fs=require("node:fs"),p=require("node:path"),os=require("node:os"),cp=require("node:child_process"); const root=cp.execSync("npm root -g",{encoding:"utf8"}).trim(); for(const name of ["wwtpfin-consulting-core","wwtpfin-consulting-report"]) fs.cpSync(p.join(root,"@dztabel/wwtpfin/skills",name),p.join(os.homedir(),".agents/skills",name),{recursive:true});'
```

For Claude Code, replace `.agents/skills` with `.claude/skills`. Reopen the session and confirm both skills appear in its skill list. CLI help should include `compare`, `finalize` and `verify-final-run`.

## Quick Start

### Investigate cost reductions from a feasibility study

Codex:

> $wwtpfin-consulting-core Read these project materials, establish a sourced baseline, and investigate construction and operating cost reductions. Preserve service requirements, explain evidence, eligibility, lifecycle effects and responsibilities, then recompute complete combinations for my selection.

For Claude Code, use `/wwtpfin-consulting-core` with the same request.

### Continue with a newly discovered policy

> $wwtpfin-consulting-core Assess whether this policy applies to the project, identify linked parameter changes and conditions, calculate adoption versus non-adoption, and compare combinations with existing measures.

### Select a scheme and generate results

> $wwtpfin-consulting-core I confirm scheme B from this comparison. Recalculate its complete parameters and verify the final calculation package.

Unsatisfied constraints or implementation conditions are identified explicitly. To produce Word:

> $wwtpfin-consulting-report Organize a complete consulting report from the explicitly selected final run and source materials, then export Word with DocxKit.

Claude Code uses slash commands with the same skill names. Baseline and conditional calculations can also be delivered independently with their purpose stated.

## Commands, examples and boundaries

- [Three-stage responsibilities](docs/THREE_STAGE_PRODUCT.md) and [executable synthetic example](examples/three_stage/README.md).
- [Public interfaces](docs/contract-surface.md), [field reference](docs/spec-reference.md) and [material conversion](docs/INTAKE.md).
- [Product boundaries](docs/boundary.md), [downstream handoff](examples/handoff/README.md) and [binary distribution](docs/binary-distribution.md).

The CLI recalculates explicit candidates and constraints. Responsible people assess policy eligibility, engineering conditions and final selection. Conditional calculations are not approved schemes, and rankings do not prove a global optimum.

This public repository contains the launcher, documentation, generic examples and agent skills. It does not publish the financial core source. The software is proprietary (`UNLICENSED`); no open-source license is granted.
