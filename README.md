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
- PCB-side Solder / Paste mask normalization 已完成：ordinary SMD pads 使用 Rule Expansion；Top Paste visual evidence 已确认普通 SMT 焊盘有有效 aperture，THT / mounting features 未被错误加入普通 Paste population。最终 GTP/GBP 或等效制造输出仍待 Stage 7 检查。
- 当前 Altium DRC working baseline 已同步到 [docs/pcb_design_rules.md](docs/pcb_design_rules.md)：Default Clearance 6 mil、`GND_IN_RAW↔GND` 20 mil、Default Width 6/6/15 mil、`SW_NODE` 16/20/24 mil、`NC_POWER` 8/20/32 mil、Hole-to-Hole 8 mil、Minimum Solder Mask Sliver 6 mil。
- 最新 DRC（2026-09-04 18:30）结果：**Warnings 0 / Rule Violations 76**。Short-Circuit、Un-Routed、Modified Polygon、Width、`GND_IN_RAW↔GND`、Hole Size、Hole-to-Hole 均为 **0 violation**。
- 剩余 76 条已完成工程归类：**4 × M3 NPTH 与自身 Keepout 的 intentional rule-scope collision；66 × Minimum Solder Mask Sliver；6 × intentional HSE GND guard Net Antennae**。此前真实 ordinary copper clearance findings 已清除。66 条 mask sliver 主要来自 U1 / Q25 / USB-C fine-pitch pad geometry 与少量已拉开的 Pad↔Via mask-dam 检查；当前没有从这些 findings 中识别到新的电气 routing/connectivity blocker，但 raw DRC report 仍非 zero-violation，因此不声明正式 `DRC PASS`。
- `GND_IN_RAW -> Q25 -> PCB GND` 仍是必须保持的功能边界；最新 dedicated 20 mil DRC rule 为 0 violation，最终 manufacturing-data review 仍需确认 polygon / via / mounting feature 没有绕过 Q25。
- 最新完整 schematic PDF 与 BOM 已归档到 `hardware/outputs/`，作为 Stage 4 formal-review evidence；Hardware Revision 仍为 `TBD`。
- Stage 5 minor mechanical note 仍保留：后续用 3D / courtyard / 实际机械 evidence 确认 `CN5` 与右下 M3 螺钉/垫片/可拔插端子 envelope；当前 2D evidence 不将其视为 Stage 6 blocker。

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

Stage 6 ordinary routing / copper review 当前可以停止继续大范围修改。下一轮只做 **PCB finalization**：

```text
1. add accessible 3V3 + GND test points
2. add / clean critical Top Overlay labels: power, GND, connector function, Pin 1, polarity, SWD/debug, sensor / IN / OUT identification
3. avoid moving electrically accepted components solely for silkscreen cleanup
4. repour polygons after the test-point / overlay edits
5. rerun complete Final DRC and confirm no new electrical / copper / hole blocker was introduced
6. preserve the four intentional M3 self-keepout findings and six confirmed HSE GND-guard findings as documented exceptions unless rule scoping is refined
7. generate final Gerber / Drill / Solder Mask / Paste manufacturing data
8. inspect the actual JLCPCB CAM / Gerber interpretation before manufacturing release
```

Stage 6 closeout / transition toward manufacturing preparation should be judged after the test-point / silkscreen edits and the resulting Final DRC. Manufacturing release is **not yet approved**; no hardware-test, EMC/surge, assembly-fit or manufacturing PASS is claimed.