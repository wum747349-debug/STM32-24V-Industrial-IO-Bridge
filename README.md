# STM32 24V Industrial I/O Bridge

Project Identity: wum747349-debug/STM32-24V-Industrial-IO-Bridge
Current Project Stage: Stage 4 — Schematic Review
Hardware Revision: TBD

## 项目目的（Purpose）

设计一块以 STM32F103C8T6 为主控、面向 24 V 工业现场的 I/O 中继与接口板，连接 C# 上位机、板载 USB-UART、STM32 与 CM35 运动控制器，并接入 4 路 AN-LS18-40-N 光电开关。新板替代外购 STM32 最小系统板与外置 USB 转串口模块，并面向 JLCPCB / LCSC 及 SMT / PCBA 实现。

## 当前状态（Current Status）

- Framework binding 与初始化状态：[FRAMEWORK.md](FRAMEWORK.md)
- 第一版 Requirements Baseline 已建立，Gate 1.5 已执行并记录 PASS，初始化状态为 `Initialized`。
- Stage 2 selection closeout 保持完成，并在 [docs/component_selection_plan.md](docs/component_selection_plan.md) 记录 `PASS`；Stage 3 module design / capture closeout 已完成，结论为 `READY FOR SCHEMATIC REVIEW`。
- M1 power、M2 STM32 minimum-system、M3 isolated USB-UART、M4 CM35 I/O 与 M5 Sensor Interface 的当前 module design / current-session EDA capture 均达到 `CLOSEOUT ACCEPTABLE`；长期记录见 [M1](docs/module_design/m1_power.md)、[M2](docs/module_design/m2_stm32_minimum_system.md)、[M3](docs/module_design/m3_usb_uart_isolation.md)、[M4](docs/module_design/m4_cm35_io.md) 与 [M5](docs/module_design/m5_sensor_interface.md)。
- M5 已完成 Sensor 1–4 的 NO / NC 共 8 路 capture，并通过当前会话 screenshot-level completeness review；该结论不代表 `.SchDoc` object parsing、footprint verification、ERC、EMC/surge 或实测通过。
- 当前 Primary 范围包括 STM32F103C8T6、CH340C、ISO7721DR、USBLC6-2SC6、Nexperia 2N7002,215、LMR36510FADDAR、0468.500NRHF、STPS2H100A 与 SMBJ30A-TR；USB-C receptacle 为 mechanical-conditional candidate。
- 24 V source 当前有用户提供的 `MS-120-24` 24 V / 5 A / 120 W 图片证据，且用户已用万用表确认实际输出约 24 V、观察较稳定；该 evidence 不替代官方 tolerance / surge specification。
- Stage 2 已建立 `0.225 A` 的 24 V continuous design envelope，并将 Littelfuse `0468.500NRHF` 0.5 A / 63 V Slo-Blo fuse 选为 F1 Primary；60 V PPTC 仅作为有温度限制的 Alternate architecture。
- CM35 Stage-2 topology qualification 已关闭；Rev.A 使用两套隔离输出的 24 V switching PSU：PSU A 仅供 CM35 system `24V/0V`，PSU B 直接分配至 CM35 I/O `V/G` 与 PCB `24V/GND`。PCB `GND = CM35 G / 24G = PSU B -V`，且不得直接连接 CM35 system `0V`、PSU A `-V`、PE 或 chassis。M4 的 16-channel 2N7002 network 与 safe-startup contract 保持不变。
- 当前本地同日导出的完整 schematic PDF 与 BOM 支持 Stage 3 closeout；Hardware Revision 仍为 `TBD`。当前文档不声称 `.SchDoc` 已被解析、ERC、footprint verification、Stage 4 PASS、PCB Layout approval、DRC、Manufacturing、Bring-up 或 Test 已完成。

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

使用当前完整 schematic PDF、当前 BOM、Requirements、Design Notes、References 与 module records 执行 Stage 4 Formal Schematic Review，并把实际 findings 与结论记录到当前 `PENDING` 的 [docs/schematic_review.md](docs/schematic_review.md)。当前仅为 `READY FOR SCHEMATIC REVIEW`；尚无 ERC PASS、Stage 4 PASS 或 PCB Layout approval。
