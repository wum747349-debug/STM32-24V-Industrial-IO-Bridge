# STM32 24V Industrial I/O Bridge

Project Identity: wum747349-debug/STM32-24V-Industrial-IO-Bridge
Current Project Stage: Stage 6 — Routing and Copper
Hardware Revision: TBD

## 项目目的（Purpose）

设计一块以 STM32F103C8T6 为主控、面向 24 V 工业现场的 I/O 中继与接口板，连接 C# 上位机、板载 USB-UART、STM32 与 CM35 运动控制器，并接入 4 路 AN-LS18-40-N 光电开关。新板替代外购 STM32 最小系统板与外置 USB 转串口模块，并面向 JLCPCB / LCSC 及 SMT / PCBA 实现。

## 当前状态（Current Status）

- Framework binding 与初始化状态：[FRAMEWORK.md](FRAMEWORK.md)
- 第一版 Requirements Baseline 已建立，Gate 1.5 已执行并记录 PASS，初始化状态为 `Initialized`。
- Stage 2 selection closeout 保持完成，并在 [docs/component_selection_plan.md](docs/component_selection_plan.md) 记录 `PASS`；Stage 3 module design / capture closeout 已完成。
- M1 power、M2 STM32 minimum-system、M3 isolated USB-UART、M4 CM35 I/O 与 M5 Sensor Interface 的 module design / EDA capture 均达到 closeout-acceptable 状态；长期记录见 [M1](docs/module_design/m1_power.md)、[M2](docs/module_design/m2_stm32_minimum_system.md)、[M3](docs/module_design/m3_usb_uart_isolation.md)、[M4](docs/module_design/m4_cm35_io.md) 与 [M5](docs/module_design/m5_sensor_interface.md)。
- Stage 4 Formal Schematic Review 已 **PASS / CLOSED**。2026-09-04 Stage 6 final review 期间发现并修正两项 post-review implementation defect：U2 LMR36510 `EN -> 24V_PROTECTED`、unused `PG -> GND`；U3 CH340C 修正为 `TXD -> CH340_TX`、`RXD <- CH340_RX`，保持 ISO7721 正确方向。该 targeted correction 已记录在 [docs/schematic_review.md](docs/schematic_review.md)，但不声称 full-board ERC PASS。
- Stage 5 Full-board Placement 已 **PASS / CLOSED**；当前 PCB mechanical baseline 为 **100 mm × 80 mm、R3、4 × M3 NPTH + Copper Keepout**。此前 110 mm × 80 mm working outline 已在布线前缩减至 100 mm × 80 mm，后续 routing 未要求重新打开整板 placement。
- 当前 CM35 connector topology 保持：**左侧 `CN6 = IN11–IN18`，右侧 `CN5 = OUT1–OUT8`**；CN1–CN4 为 Sensors 1–4。
- Stage 6 的主要 signal / power routing、Top/Bottom polygon 与 machine-side GND-via stitching 已按用户提供的连续 Altium screenshot evidence 完成到 final-review level；当前未识别到需要重新打开 ordinary routing 的电气 blocker。
- Stage 6 routing-driven GPIO baseline 已收敛并记录在 [docs/pcb_review.md](docs/pcb_review.md)：

```text
IN11 -> PA8      IN12 -> PA11
IN13 -> PA12     IN14 -> PA15
IN15 -> PB4      IN16 -> PB5
IN17 -> PB6      IN18 -> PB7

SENSOR2_NO -> PA0      SENSOR2_NC -> PA1
OUT1 -> PA2            OUT2 -> PA3
OUT3 -> PA4            OUT4 -> PA5
OUT5 -> PA6            OUT6 -> PA7
OUT7 -> PB10           OUT8 -> PB11
SENSOR1_NO -> PB8      SENSOR1_NC -> PB9
SENSOR3_NO -> PB12     SENSOR3_NC -> PB13
SENSOR4_NO -> PB14     SENSOR4_NC -> PB15
```

- M3 USB / isolation routing 已完成到 final-review level：USB D+/D- 与 USB_VBUS 保持局部、`USB_GND != GND`；USB 域采用 Bottom `USB_GND` polygon 作为主要 reference，同时已实现 Top `USB_GND` copper；ISO7721 Top/Bottom 均保留明确 polygon cutout / copper exclusion，USB_GND 与 machine GND 的 Via 均留在各自域内，不跨 isolation corridor。
- SWDIO / SWCLK / MCU_NRST 因局部 crossing topology 使用必要的 Bottom routing；此前 MCU 附近真实 Track/Via clearance findings 已在 2026-09-04 最终 DRC 迭代中清除。
- M1 Buck 电源地已经做局部收敛：U2 exposed-pad / GND thermal vias 保留，C11/C12 输入电容使用局部 Top GND copper + 多 Via 回到底层，C14/C15/C16 输出电容侧保持宽 GND / 多 Via；`SW_NODE` width 当前 DRC 为 0 violation。
- M2 HSE 区已完成局部优化：X1/C2/C4 保持靠近 MCU，OSC 走线短且在 Top；使用 10 mil Top GND guard、局部 GND vias 与 Top Polygon Pour Cutout 控制晶振区铜皮。当前 DRC 的 6 个 `Net Antennae` 已由用户截图确认均为 intentional HSE GND guard track / GND via 结构，不作为 dead-signal defect 处理。
- PCB-side Solder / Paste mask normalization 已完成：ordinary SMD pads 使用 Rule Expansion；普通 SMT 焊盘已有有效 Paste aperture，THT / mounting features 不进入普通 Paste population。
- PCB finalization 已完成：已增加可访问的 **3V3 + GND Top-side test pads**，采用约 2.0 mm round copper、无 drill、Top Paste disabled、Top Solder 依 Rule Expansion 开窗；关键 Top Overlay 已整理，包括 power polarity、SWD/debug、USB-UART、Sensors、CM35 IN/OUT、RESET/BOOT 与测试点标识。
- 当前 Altium DRC baseline 已同步到 [docs/pcb_design_rules.md](docs/pcb_design_rules.md)：Default Clearance 6 mil、`GND_IN_RAW↔GND` 20 mil、Default Width 6/6/15 mil、`SW_NODE` 16/20/24 mil、`NC_POWER` 8/20/32 mil、Hole-to-Hole 8 mil、Minimum Solder Mask Sliver 6 mil。
- **Final DRC（2026-09-04 21:42）**：Warnings **0** / Rule Violations **76**。Short-Circuit、Un-Routed、Modified Polygon、Width、`GND_IN_RAW↔GND`、Hole Size、Hole-to-Hole 均为 **0 violation**。
- Final DRC 剩余 76 条仍为已审查分类：**4 × M3 NPTH 与自身 Keepout 的 intentional rule-scope collision；66 × Minimum Solder Mask Sliver；6 × intentional HSE GND guard Net Antennae**。没有因 test-point / overlay finalization 新增 ordinary electrical routing/connectivity blocker；raw report 仍非 zero-violation，因此不声明形式上的 `DRC PASS`。
- `GND_IN_RAW -> Q25 -> PCB GND` 仍是必须保持的功能边界；Final DRC dedicated 20 mil rule 为 0 violation。
- Final Gerber 已生成并上传 JLCPCB Gerber/CAM Viewer。基于用户提供的实际 CAM preview，board outline / corner geometry / four M3 holes、主要 copper、USB isolation corridor、Q25 ground-boundary interpretation、critical Top Overlay 与新增 3V3/GND test points 未发现新的 fabrication blocker。
- **PCB Fabrication Release：READY / RELEASED**。2026-09-05 用户已确认嘉立创生成的最终生产稿，当前订单已放行并进入等待生产状态；未发现新的 PCB fabrication blocker。
- 当前下单配置记录为：**PCB 5 pcs；PCBA 2 pcs；Economic / Top Side only；Single Board 坐标文件**。34 个 BOM 物料组中 29 组由嘉立创装配，5 组保持“不贴”，对应 9 个后续手焊 THT 器件：`BOOT0`、`SWD`、`CM35_IN / CM35_OUT`、`SENSOR1~4`、`24V_IN`。
- PCBA BOM matching 已完成；已记录的自动匹配修正包括 `X1 -> C20617233`、`C11 -> C577211`、`C12 -> C513710`、`L1 -> C83454`。关键器件 U1/U2/U3/U4/Q25/USB-C/二极管等已在当前 manufacturing review 范围内核对，嘉立创极性处理采用“由工程师依据丝印协助确认/修正方向”。
- **JLCPCB Manufacturing Order：RELEASED / AWAITING PRODUCTION**。这表示当前订单已经由用户确认生产稿并放行；仓库仍不虚构独立的 exhaustive SMT orientation PASS、hardware test、assembly fit、EMC/surge 或 system validation PASS。
- 最新完整 schematic PDF 与 BOM 已归档到 `hardware/outputs/`，作为 Stage 4 formal-review evidence；Hardware Revision 仍为 `TBD`。
- Stage 5 minor mechanical note 仍保留：后续用 3D / courtyard / 实际机械 evidence 确认 `CN5` 与右下 M3 螺钉/垫片/可拔插端子 envelope；当前 evidence 不将其视为 PCB fabrication blocker。

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

当前 PCB / PCBA 制造订单已放行，设计侧不再主动重新打开已收口的 routing、polygon、mask、BOM 或 placement，除非嘉立创生产过程中返回新的 DFM / substitution / polarity / assembly query 并暴露真实 blocker。

当前工作状态：

```text
JLCPCB production artwork: CONFIRMED
PCB fabrication order:     RELEASED
PCBA order:                 RELEASED
Manufacturing state:        AWAITING PRODUCTION
```

收板后再进入 incoming inspection / continuity checks / power-on bring-up / USB-UART / GPIO / sensor / CM35 interface validation，并按照当时的 Framework / Stage Gate evidence 要求决定后续 Stage transition。

Current Project Stage remains **Stage 6 — Routing and Copper**; this documentation sync does not itself execute a Stage transition.