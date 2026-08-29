# STM32 24V Industrial I/O Bridge

Project Identity: wum747349-debug/STM32-24V-Industrial-IO-Bridge
Current Project Stage: Stage 2 — Critical Component Selection
Hardware Revision: TBD

## 项目目的（Purpose）

设计一块以 STM32F103C8T6 为主控、面向 24 V 工业现场的 I/O 中继与接口板，连接 C# 上位机、板载 USB-UART、STM32 与 CM35 运动控制器，并接入 4 路 AN-LS18-40-N 光电开关。新板替代外购 STM32 最小系统板与外置 USB 转串口模块，并面向 JLCPCB / LCSC 及 SMT / PCBA 实现。

## 当前状态（Current Status）

- Framework binding 与初始化状态：[FRAMEWORK.md](FRAMEWORK.md)
- 第一版 Requirements Baseline 已建立，Gate 1.5 已执行并记录 PASS，初始化状态为 `Initialized`。
- Project 当前处于 Stage 2 — Critical Component Selection；Stage 2 selection closeout 已完成并在 [docs/component_selection_plan.md](docs/component_selection_plan.md) 记录 `PASS`，尚未开始 Stage 3 engineering work。
- 当前 Primary 范围包括 STM32F103C8T6、CH340C、ISO7721DR、USBLC6-2SC6、Nexperia 2N7002,215、LMR36510FADDAR、0468.500NRHF、STPS2H100A 与 SMBJ30A-TR；USB-C receptacle 为 mechanical-conditional candidate。
- 24 V source 当前有用户提供的 `MS-120-24` 24 V / 5 A / 120 W 图片证据，且用户已用万用表确认实际输出约 24 V、观察较稳定；该 evidence 不替代官方 tolerance / surge specification。
- Stage 2 已建立 `0.225 A` 的 24 V continuous design envelope，并将 Littelfuse `0468.500NRHF` 0.5 A / 63 V Slo-Blo fuse 选为 F1 Primary；60 V PPTC 仅作为有温度限制的 Alternate architecture。
- CM35 Stage-2 topology qualification 已关闭；Sensor 以用户提供 manual 支持 conditional closeout。exact interface parameters、GPIO/USART、普通外围、connector mechanical acceptance 与 PCB mechanics 均按真实 lifecycle 后置，不是 Stage 2 blocker。
- Hardware Revision 仍为 `TBD`；没有声称 `.SchDoc` / `.PcbDoc`、ERC、DRC、Manufacturing、Bring-up 或 Test 已完成。

## 项目事实入口（Project Facts）

- [需求基线（Requirements Baseline）](requirements.md)
- [系统框图（Block Diagram）](block_diagram.md)
- [设计说明（Design Notes）](design_notes.md)
- [资料索引（Reference Index）](references.md)
- [关键器件选型记录（Component Selection Plan）](docs/component_selection_plan.md)

## 仓库导航（Repository Navigation）

- [Project Runtime Rules](PROJECT_RULES.md)
- [Stage 文档职责](docs/README.md)
- [Hardware source 与 Evidence 职责](hardware/README.md)
- [本地资料职责](references/README.md)
- [Project Validator](scripts/validate_project_repository.py)

## 下一步（Next Step）

Stage 2 已满足退出条件。下一次明确启动 Stage 3 时，先建立首个真实 module design record，再进行模块连接、参数设计和 EDA capture；本次 closeout 不创建 Stage 3 records，不计算 exact resistor / RC / buck magnetics，也不创建或修改 `.SchDoc` / `.PcbDoc`。采购或 PCBA BOM submission 前对 Primary / Alternate 做 lightweight availability recheck。
