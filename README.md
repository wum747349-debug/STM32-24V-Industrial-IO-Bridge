# STM32 24V Industrial I/O Bridge

Project Identity: wum747349-debug/STM32-24V-Industrial-IO-Bridge
Current Project Stage: Stage 3 — Schematic Module Design and Capture
Hardware Revision: TBD

## 项目目的（Purpose）

设计一块以 STM32F103C8T6 为主控、面向 24 V 工业现场的 I/O 中继与接口板，连接 C# 上位机、板载 USB-UART、STM32 与 CM35 运动控制器，并接入 4 路 AN-LS18-40-N 光电开关。新板替代外购 STM32 最小系统板与外置 USB 转串口模块，并面向 JLCPCB / LCSC 及 SMT / PCBA 实现。

## 当前状态（Current Status）

- Framework binding 与初始化状态：[FRAMEWORK.md](FRAMEWORK.md)
- 第一版 Requirements Baseline 已建立，Gate 1.5 已执行并记录 PASS，初始化状态为 `Initialized`。
- Stage 2 selection closeout 保持完成，并在 [docs/component_selection_plan.md](docs/component_selection_plan.md) 记录 `PASS`；Stage 3 engineering work 已启动。
- M1 power、M2 STM32 minimum-system、M3 isolated USB-UART 与 M4 CM35 I/O 的当前 module design / current-session EDA capture 均达到 `CLOSEOUT ACCEPTABLE`；长期记录见 [M1](docs/module_design/m1_power.md)、[M2](docs/module_design/m2_stm32_minimum_system.md)、[M3](docs/module_design/m3_usb_uart_isolation.md) 与 [M4](docs/module_design/m4_cm35_io.md)。
- M5 Sensor Interface 的单通道 frontend baseline 已定义并可复制，但 capture 仍为 `IN PROGRESS`；当前只完成 Sensor 1 NO reference channel 的 screenshot-level review，详见 [M5](docs/module_design/m5_sensor_interface.md)。
- 当前 Primary 范围包括 STM32F103C8T6、CH340C、ISO7721DR、USBLC6-2SC6、Nexperia 2N7002,215、LMR36510FADDAR、0468.500NRHF、STPS2H100A 与 SMBJ30A-TR；USB-C receptacle 为 mechanical-conditional candidate。
- 24 V source 当前有用户提供的 `MS-120-24` 24 V / 5 A / 120 W 图片证据，且用户已用万用表确认实际输出约 24 V、观察较稳定；该 evidence 不替代官方 tolerance / surge specification。
- Stage 2 已建立 `0.225 A` 的 24 V continuous design envelope，并将 Littelfuse `0468.500NRHF` 0.5 A / 63 V Slo-Blo fuse 选为 F1 Primary；60 V PPTC 仅作为有温度限制的 Alternate architecture。
- CM35 Stage-2 topology qualification 已关闭；M4 已冻结 Rev.A common-reference implementation、16-channel 2N7002 network 与 safe-startup contract。M5 已冻结 per-channel 2N7002 / series resistor / TVS baseline，但其余 7 路 capture 与完整性 review 尚未完成；connector mate mechanical acceptance 与 PCB mechanics 仍按 lifecycle 后置。
- Stage 3 overall 尚未完成；Hardware Revision 仍为 `TBD`。当前文档不声称 `.SchDoc` 已被解析、ERC、Stage 4 review、PCB Layout、DRC、Manufacturing、Bring-up 或 Test 已完成。

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

继续 M5 — Photoelectric Sensor Interface 的 Stage-3 capture：按已审核的 Sensor 1 NO reference channel 复制其余 7 路，并完成 8 路 screenshot-level completeness review。当前不进入 Stage 4，不将 M5 标记完成，也没有 PCB Layout approval。
