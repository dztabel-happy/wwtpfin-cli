# 下游交接

先生成并校验咨询内容包：

```bash
wwtp-fin build -p examples/showcase/project.yaml \
  --evidence examples/showcase/evidence.json -o handoff-out
wwtp-fin verify-deliverable handoff-out
```

## DocxKit

- `document.json`：报告章节、语块、表格和引用的语义来源；agent 按 DocxKit 契约转换为 `report.json`。
- `tables/`：可编辑表格数据，保留标题和来源引用。
- `quality.json`、`warnings.json`：交付前复核，不写入正文。

DocxKit 只负责 Word 排版与交付，不重算财务结果，也不续写无证据结论。

## ChartKit

- `figures/index.json`：图表 ID、题目、语义角色和 brief 索引。
- `figures/*.json`：数据意图、标题、题注和来源引用。
- `figures/data/*.csv`：图表使用的数据。

ChartKit 负责图型和图片导出；图号、题注与摆放由文档层处理。
