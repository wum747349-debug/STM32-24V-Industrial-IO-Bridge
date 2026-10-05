# Hardware Sources and Evidence（硬件源与证据）

只有相应工作或 Evidence 真实存在时才创建 hardware 子目录：

- `altium_project/`：权威 `.PrjPcb`、`.SchDoc`、`.PcbDoc` 与必要 Project libraries；
- `outputs/`：可追溯的 schematic PDF、BOM、reports 与 manufacturing outputs；
- `images/`：Review、Assembly、Bring-up、Test 与展示图片。

`.SchDoc` 与 `.PcbDoc` 是权威 EDA implementation sources。目录、PDF、图片或书面设计意图不能证明 ERC、DRC、rule matching、copper state 或 manufacturing release。用户负责实际 Altium 操作与导出；AI/Codex 只在明确限制内分析用户提供的 Evidence。

不得仅为让目录看起来完整而创建空 output 分类或低信息量 placeholder 文件。

## Current Rev.C Altium Source Set

The versioned source set is limited to the files required by the current `STM32 24V Industrial IO Bridge.PrjPcb` project:

- `altium_project/P1.schdoc`
- `altium_project/PCB1.PcbLib`
- `altium_project/STM32 24V Industrial IO Bridge.SCHLIB`
- `altium_project/STM32 24V Industrial IO Bridge/STM32 24V Industrial IO Bridge.PrjPcb`
- `altium_project/STM32 24V Industrial IO Bridge/STM32 24V Industrial IO Bridge.PcbDoc`

The `.PrjPcb` source explicitly references the schematic, both project-local libraries, and the PCB document above. Generated `History`, project logs, previews, project outputs, `.PrjPcbStructure`, backups, temporary ZIP files, Gerber/drill data, and pick-and-place or assembly archives are not part of the public source set.
