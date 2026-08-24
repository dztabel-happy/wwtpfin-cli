<h1 align="center">wwtp-fin</h1>

<p align="center">污水处理项目确定性财务咨询 CLI</p>

<p align="center">
  <a href="README.md">English</a>
  ·
  <a href="#安装">安装</a>
  ·
  <a href="#快速开始">快速开始</a>
  ·
  <a href="#边界与文档">边界与文档</a>
</p>

<p align="center">
  <img alt="npm" src="https://img.shields.io/npm/v/@dztabel/wwtpfin?label=npm">
  <img alt="platforms" src="https://img.shields.io/badge/platform-macOS%20arm64%20%7C%20Linux%20x64%20%7C%20Windows%20x64-blue">
</p>

---

wwtp-fin 把可追溯的结构化参数与证据转换为确定性的污水处理项目财务计算、检查、裁决、报告语义、表格数据和图表 brief。它不生成 Word 或图片，也不补造缺失项目事实。

## 安装

### npm 二进制

```bash
npm install -g @dztabel/wwtpfin
wwtp-fin --version
```

npm 路径支持 macOS Apple Silicon、Linux x64 和 Windows x64。

### Python 包

```bash
python3 -m pip install wwtp-fin
wwtp-fin --version
```

Python 包路径要求 Python 3.9+。

## 快速开始

```bash
wwtp-fin build -p examples/showcase/project.yaml \
  --evidence examples/showcase/evidence.json -o deliverable
wwtp-fin verify-deliverable deliverable
wwtp-fin check -p examples/showcase/project.yaml
```

应同时阅读 `quality.json`、`warnings.json`、`result.json`、`document.json`、表格与图表 brief。

## 边界与文档

- [INTAKE](docs/INTAKE.md)：材料到契约的转化纪律。
- [公开契约面](docs/contract-surface.md)：命令、schema、退出码与确定性约束。
- [产品边界](docs/boundary.md)：产品范围及与 DocxKit/ChartKit 的交接。
- [二进制分发](docs/binary-distribution.md)：平台包发布形制。

公开仓只包含 npm 壳、用户文档、示例与 agent skills；不包含财务核心源码。
