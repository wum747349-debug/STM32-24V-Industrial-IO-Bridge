# Reference Index

关键参数必须回到官方 datasheet、reference manual 或 application note 核对。商品页可辅助库存和采购研究，但不能替代官方技术证据；开源项目只能用于学习方法与结构，不能成为本 Project facts。

## Project Inputs and Legacy Evidence

| Item | Source | Role | Current State | Local Path or Link |
| --- | --- | --- | --- | --- |
| Project initialization brief | 用户在 2026-08-29 提供的本任务说明 | 当前 Stage 1 requirements 与 interface contract 的事实输入 | Reviewed for Stage 1 | Conversation record; no local file |
| Previous-generation schematic PDF | 用户说明存在 | Legacy Design Reference / Existing Functional Evidence；不是本项目 EDA authority | Not available in current workspace search | 待用户提供后归档 |
| Previous-generation BOM spreadsheet | 用户说明存在 | Legacy Design Reference；旧器件仍需重新 qualification | Not available in current workspace search | 待用户提供后归档 |
| AN-LS18-40-N manual / purchase information | 用户说明存在 | External Device Reference；需区分官方资料与采购信息 | Not available in current workspace search | 待用户提供后归档 |

当前 workspace 的最小文件名检索未找到上述 PDF/表格。没有创建假资料，也没有读取 Legacy `.SchDoc` / `.PcbDoc`。未来新项目的 `.SchDoc` 与 `.PcbDoc` 才是 EDA implementation authority。

## Official Sources

| Item / Module | Document | Source | Version | Purpose | Review Status | Local Path or Link |
| --- | --- | --- | --- | --- | --- | --- |
| STM32F103C8T6 | Datasheet + reference manual + relevant application notes | STMicroelectronics official | Exact revisions TBD | Minimum system、electrical limits、boot/reset/clock/SWD/VDDA 与 safe state qualification | Not collected | 待 Stage 2/3 按当前决策获取 |
| AN-LS18-40-N | Manufacturer manual / datasheet | Manufacturer to be confirmed | TBD | Supply、wiring、output circuit、current、timing、environment rating | Not collected | 待用户提供或确认制造商正式来源 |
| CM35 controller | Official I/O manual / electrical specification | CM35 manufacturer to be confirmed | TBD | IN11–IN18 / OUT1–OUT8 electrical characteristics and timing qualification | Not collected | 待用户提供或确认正式来源 |
| Future critical devices | Manufacturer datasheet / application note | TBD in Stage 2 | TBD | USB-UART、isolation、power/protection、CM35/Sensor frontend qualification | Not selected | Stage 2 按候选获取 |

## Procurement Sources

| Item | Source | Purpose | Technical Limitation |
| --- | --- | --- | --- |
| AN-LS18-40-N purchase information | 用户已有购买资料，当前未归档 | 型号、购买来源与初步接线信息 | 不能替代 manufacturer official electrical specification |
| JLCPCB / LCSC availability | Future supplier search | 库存、PCBA 可用性、封装与成本 | 不能替代器件 manufacturer datasheet 或设计 qualification |

## Open-source References

| Project | Source | Learning Purpose | Content Not Reused |
| --- | --- | --- | --- |
| None | 不使用开源项目作为当前事实源 | Not applicable | Schematic, PCB, BOM, manufacturing files |

## Missing Evidence

| Topic | Required Source | Decision Blocked | Priority | Evidence State |
| --- | --- | --- | --- | --- |
| STM32 minimum system and safe startup | ST official datasheet/reference manual/application notes | Stage 3 peripheral and safe-state design | High; needed by Stage 3 | Open |
| CM35 I/O electrical specification | CM35 official manual/datasheet | 当期输入驱动与输出接收重新 qualification | High; needed by Stage 2/3 | Open |
| AN-LS18-40-N official specification | Manufacturer official manual/datasheet | Sensor frontend、power budget、wiring confirmation | High; needed by Stage 2 | Open |
| Legacy schematic PDF and BOM | User-provided original files with provenance | Legacy behavior traceability and comparison only | Medium; review before Stage 3 qualification | Open |
| USB grounding / isolation field constraints | User site grounding, cable, fault and EMC context | USB isolation architecture | High; decision needed before Stage 2 | Open |
| Mechanical envelope | Enclosure, board size, mounting and wiring constraints | Connector selection and PCB outline | High; begin before Stage 2, freeze before Stage 5 | Open |
