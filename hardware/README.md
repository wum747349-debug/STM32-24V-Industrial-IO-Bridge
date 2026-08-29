# Hardware Sources and Evidence（硬件源与证据）

只有相应工作或 Evidence 真实存在时才创建 hardware 子目录：

- `altium_project/`：权威 `.PrjPcb`、`.SchDoc`、`.PcbDoc` 与必要 Project libraries；
- `outputs/`：可追溯的 schematic PDF、BOM、reports 与 manufacturing outputs；
- `images/`：Review、Assembly、Bring-up、Test 与展示图片。

`.SchDoc` 与 `.PcbDoc` 是权威 EDA implementation sources。目录、PDF、图片或书面设计意图不能证明 ERC、DRC、rule matching、copper state 或 manufacturing release。用户负责实际 Altium 操作与导出；AI/Codex 只在明确限制内分析用户提供的 Evidence。

不得仅为让目录看起来完整而创建空 output 分类或低信息量 placeholder 文件。
