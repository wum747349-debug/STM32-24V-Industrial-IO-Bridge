# STM32 24V Industrial I/O Bridge

Project Identity: wum747349-debug/STM32-24V-Industrial-IO-Bridge
Current Project Stage: Stage 1 — Requirements Definition
Hardware Revision: TBD

## 项目目的（Purpose）

设计一块以 STM32F103C8T6 为主控、面向 24 V 工业现场的 I/O 中继与接口板，连接 C# 上位机、板载 USB-UART、STM32 与 CM35 运动控制器，并接入 4 路 AN-LS18-40-N 光电开关。新板替代外购 STM32 最小系统板与外置 USB 转串口模块，并面向 JLCPCB / LCSC 及 SMT / PCBA 实现。

## 当前状态（Current Status）

- Framework binding 与初始化状态：[FRAMEWORK.md](FRAMEWORK.md)
- 第一版 Requirements Baseline 已建立，Gate 1.5 尚未记录 PASS。
- 当前仅完成 Project Bootstrap、Stage 1 文档和 Gate 1.5 Readiness Review 所需输入；Stage 2 及之后尚未开始。
- Hardware Revision 仍为 `TBD`；没有声称器件选型、EDA、ERC、DRC、Manufacturing、Bring-up 或 Test 已完成。

## 项目事实入口（Project Facts）

- [需求基线（Requirements Baseline）](requirements.md)
- [系统框图（Block Diagram）](block_diagram.md)
- [设计说明（Design Notes）](design_notes.md)
- [资料索引（Reference Index）](references.md)

## 仓库导航（Repository Navigation）

- [Project Runtime Rules](PROJECT_RULES.md)
- [Stage 文档职责](docs/README.md)
- [Hardware source 与 Evidence 职责](hardware/README.md)
- [本地资料职责](references/README.md)
- [Project Validator](scripts/validate_project_repository.py)

## 下一步（Next Step）

运行 Project Validator 与 Gate 1.5 Validator，依据绑定 Framework 的 Initialization Checklist 完成人工事实审查；本次只形成 `READY / NOT READY` 技术结论，不记录 Gate PASS、不把初始化状态改为 `Initialized`、不进入 Stage 2。
