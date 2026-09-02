# STM32 24V Industrial I/O Bridge

Project Identity: wum747349-debug/STM32-24V-Industrial-IO-Bridge
Current Project Stage: Stage 6 — Routing and Copper
Hardware Revision: TBD

## 项目目的（Purpose）

设计一块以 STM32F103C8T6 为主控、面向 24 V 工业现场的 I/O 中继与接口板，连接 C# 上位机、板载 USB-UART、STM32 与 CM35 运动控制器，并接入 4 路 AN-LS18-40-N 光电开关。新板替代外购 STM32 最小系统板与外置 USB 转串口模块，并面向 JLCPCB / LCSC 及 SMT / PCBA 实现。

## 当前状态（Current Status）

- Framework binding 与初始化状态：[FRAMEWORK.md](FRAMEWORK.md)
- 第一版 Requirements Baseline 已建立，Gate 1.5 已执行并记录 PASS，初始化状态为 `Initialized`。
- Stage 2 selection closeout 保持完成，并在 [docs/component_selection_plan.md](docs/component_selection_plan.md) 记录 `PASS`；Stage 3 module design / capture closeout 已完成，结论为 `READY FOR SCHEMATIC REVIEW`。
- M1 power、M2 STM32 minimum-system、M3 isolated USB-UART、M4 CM35 I/O 与 M5 Sensor Interface 的 module design / EDA capture 均达到 `CLOSEOUT ACCEPTABLE`；长期记录见 [M1](docs/module_design/m1_power.md)、[M2](docs/module_design/m2_stm32_minimum_system.md)、[M3](docs/module_design/m3_usb_uart_isolation.md)、[M4](docs/module_design/m4_cm35_io.md) 与 [M5](docs/module_design/m5_sensor_interface.md)。
- M5 已完成 Sensor 1–4 的 NO / NC 共 8 路 capture，并通过当前会话 screenshot-level completeness review；该结论不代表 `.SchDoc` object parsing、footprint verification、ERC、EMC/surge 或实测通过。
- 当前 Primary 范围包括 STM32F103C8T6、CH340C、ISO7721DR、USBLC6-2SC6、保留用于 M4/M5 的 2N7002 LCSC `C7420321`、LMR36510FADDAR、0468.500NRHF、STPS2H100A 与 SMBJ30A-TR；Nexperia `2N7002,215` 保留为 qualification history/reference，不是强制替换要求；USB-C receptacle 为 mechanical-conditional candidate。
- 24 V source 当前有用户提供的 `MS-120-24` 24 V / 5 A / 120 W 图片证据，且用户已用万用表确认实际输出约 24 V、观察较稳定；该 evidence 不替代官方 tolerance / surge specification。
- Stage 2 已建立 `0.225 A` 的 24 V continuous design envelope，并将 Littelfuse `0468.500NRHF` 0.5 A / 63 V Slo-Blo fuse 选为 F1 Primary；60 V PPTC 仅作为有温度限制的 Alternate architecture。
- CM35 Stage-2 topology qualification 已关闭；Rev.A 使用两套隔离输出的 24 V switching PSU：PSU A 仅供 CM35 system `24V/0V`，PSU B 直接分配至 CM35 I/O `V/G` 与 PCB `24V/GND`。PCB `GND = CM35 G / 24G = PSU B -V`，且不得直接连接 CM35 system `0V`、PSU A `-V`、PE 或 chassis。M4 的 16-channel 2N7002 network 与 safe-startup contract 保持不变。
- Stage 4 Formal Schematic Review 已 **PASS / CLOSED**，最终结论为“可以进入 PCB Layout”。
- Stage 5 Full-board Placement 已依据用户提供的 Altium 整板 Placement / Ratsnest evidence 完成最终检查并 **PASS / CLOSED**；当前 PCB mechanical baseline 为 **100 mm × 80 mm、R3、4 × M3 NPTH + Copper Keepout**。此前 110 mm × 80 mm working outline 已在布线前主要从右侧缩减至 100 mm × 80 mm，未发现新的 placement-level routing blocker；进一步缩宽暂不建议。
- 当前 CM35 connector routing baseline 已校正并锁定：**左侧 `CN6 = IN11–IN18`，右侧 `CN5 = OUT1–OUT8`**；CN1–CN4 Sensor、M1 Power、M2 MCU minimum system、M3 USB/UART/Isolation 与 M4 I/O placement 均进入 routing baseline。详细记录见 [docs/pcb_review.md](docs/pcb_review.md) 与 [docs/pcb_design_rules.md](docs/pcb_design_rules.md)。
- Stage 5 minor mechanical note：后续适合时用 3D / courtyard / 实际机械 evidence 再确认 `CN5` 与右下 M3 螺钉/垫片/可拔插端子 envelope；当前 2D evidence 不将其视为 Stage 6 blocker。
- 最新完整 schematic PDF 与 BOM 已归档到 `hardware/outputs/`，作为当前 Stage 4 formal-review evidence；Hardware Revision 仍为 `TBD`。本结论不声称 `.SchDoc` parser、ERC、全板 footprint verification、DRC、routed-copper correctness、hardware test、EMC/surge、Manufacturing 或 Bring-up PASS。
- 用户已在 Altium 中完成 Q25 schematic symbol D/G/S、PowerDI3333-8 footprint pads 与 manufacturer pinout 的最终核对，SR-M1-001 已关闭；`GND_IN_RAW` 仍不得绕过 Q25 直接连接 PCB `GND`。

## 项目事实入口（Project Facts）

- [需求基线（Requirements Baseline）](requirements.md)
- [系统框图（Block Diagram）](block_diagram.md)
- [设计说明（Design Notes）](design_notes.md)
- [资料索引（Reference Index）](references.md)
- [关键器件选型记录（Component Selection Plan）](docs/component_selection_plan.md)

## 仓库导航（Repository Navigation）

- [Project Runtime Rules](PROJECT_RULES.md)
- [Stage 文档职责](docs/README.md)
- [PCB Design Rules](docs/pcb_design_rules.md)
- [PCB Review](docs/pcb_review.md)
- [Hardware source 与 Evidence 职责](hardware/README.md)
- [本地资料职责](references/README.md)
- [Project Validator](scripts/validate_project_repository.py)

## 下一步（Next Step）

执行 Stage 6 — Routing and Copper。按当前基线采用“critical / module-local networks -> MCU fanout / escape -> inter-module signals -> power distribution -> GND / copper / stitching”的增量式布线方式，并在高密度网络组完成后根据 Altium screenshot / net highlighting 进行局部复核。Stage 5 closeout 不等同于 DRC、routed-copper、manufacturing、hardware-test 或 EMC/surge compliance PASS。
