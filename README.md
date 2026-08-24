<h1 align="center">wwtp-fin</h1>

<p align="center">Deterministic financial consulting CLI for wastewater projects</p>

<p align="center">
  <a href="README.zh-CN.md">中文</a>
  ·
  <a href="#installation">Installation</a>
  ·
  <a href="#quick-start">Quick Start</a>
  ·
  <a href="#scope-and-boundaries">Boundaries</a>
</p>

<p align="center">
  <img alt="npm" src="https://img.shields.io/npm/v/@dztabel/wwtpfin?label=npm">
  <img alt="platforms" src="https://img.shields.io/badge/platform-macOS%20arm64%20%7C%20Linux%20x64%20%7C%20Windows%20x64-blue">
</p>

---

wwtp-fin turns traceable structured parameters and evidence into deterministic wastewater-project financial calculations, checks, findings, report semantics, table data and figure briefs. It does not create Word files or images, and it never fills missing project facts.

## Installation

### npm binary

```bash
npm install -g @dztabel/wwtpfin
wwtp-fin --version
```

The npm package installs a platform binary for macOS Apple Silicon, Linux x64 or Windows x64.

### Python package

```bash
python3 -m pip install wwtp-fin
wwtp-fin --version
```

Python 3.9+ is required for the Python package route.

## Quick Start

```bash
wwtp-fin build -p examples/showcase/project.yaml \
  --evidence examples/showcase/evidence.json -o deliverable
wwtp-fin verify-deliverable deliverable
wwtp-fin check -p examples/showcase/project.yaml
```

Read `quality.json`, `warnings.json`, `result.json`, `document.json`, tables and figure briefs together.

## Scope and boundaries

- [INTAKE](docs/INTAKE.md): material-to-contract conversion discipline.
- [Contract surface](docs/contract-surface.md): public commands, schemas, exits and determinism.
- [Boundaries](docs/boundary.md): product scope and DocxKit/ChartKit handoff.
- [Binary distribution](docs/binary-distribution.md): platform-package release shape.

The public repository contains the npm wrapper, user documentation, examples and agent skills only. The financial core source is not included.
