# Design Notes

本文件记录整板架构、系统级设计意图、接口/跨模块约定和架构权衡；候选方案在形成依据前不得写成已选事实。已有 module design record 负责的逐引脚连接、普通 R/C 值和模块计算无需在此并行维护。

## Board-level Intent

- 新板以 STM32F103C8T6 直接集成为基础，不再依赖外购 minimum-system module；面向 JLCPCB SMT / PCBA。
- USB-to-serial 功能板载，但 USB/machine galvanic isolation 尚未冻结。
- 隔离候选仅作为待评估 option：PC USB → USB-UART → digital UART isolator → STM32；PC side 由 USB 5 V 供电，machine side 由 24 V 降压供电，可能无需 isolated DC/DC。该描述不是已选架构，仍需现场接地与器件资格核对。
- CM35 的 16 个现有使用通道全部保留；当前 reserved channels 仍是硬件边界的一部分。
- 上一代 CM35 I/O 功能行为可作为 Legacy Functional Baseline，但旧器件和旧连接不自动成为本项目当前设计决定。
- 4 个传感器每个都提供 `+24V / 0V / NO / NC` 端子；实际读取通道数待应用需求确认。
- 板级设计优先考虑工业长线保护、safe startup、现场接线可维护性和首次限流上电。

## Current Decisions

| Decision | Current Position | Basis | Decision State |
| --- | --- | --- | --- |
| 主控 | STM32F103C8T6 直接集成到 PCB | 用户确认的项目目标 | Confirmed requirement; implementation not started |
| CM35 channel count | 8 controls + 8 status，包含 reserved channels | 现有 CM35 使用边界 | Confirmed requirement; implementation not started |
| Protocol polarity | Application `1=Active`; physical GPIO Active-Low; firmware inversion | 已验证系统行为与用户提供的 interface contract | Confirmed contract; later cross-layer verification required |
| Sensor connector | 每个传感器独立 `+24V/0V/NO/NC` 端子 | 现场接线需求 | Confirmed requirement; connector not selected |
| USB isolation | Isolated / non-isolated 尚未冻结 | 工业现场 ground/noise/fault 风险未完成权衡 | Open |

## Power and Interfaces

| Domain / Interface | Source | Destination | Required Boundary |
| --- | --- | --- | --- |
| Machine power | External 24 V DC | M1 → protected 24V bus / low voltage | 反接、surge/transient、长线；首次上电可限流 |
| PC communication | PC USB | M3 → STM32 UART | 板载 USB-UART；isolation TBD；不得 back-power machine side |
| CM35 control | STM32 GPIO | M4 → CM35 IN11–IN18 | Active-Low physical contract；reset/boot safe inactive |
| CM35 status | CM35 OUT1–OUT8 | M4 → STM32 GPIO | Active-Low physical status；firmware 转正逻辑 DataOut |
| Sensors | 4 × 24 V NPN NO/NC | M5 → STM32 | 工业长线 protection/current limiting/filtering；channel count TBD |

## Pin and Connection Planning

只有真实 Project decision 已形成依据时，才记录 board-level pin/function constraints、项目网络名或跨模块 mapping；module-specific pin-by-pin implementation 由启用后的 module design record 维护。

| Function | Required Direction / Behavior | Candidate Mapping | Basis |
| --- | --- | --- | --- |
| CM35 IN11–IN18 control | 8 outputs; LOW=Active, HIGH=Inactive | TBD | 现有系统级 interface contract；exact MCU pins 留待 Stage 3 |
| CM35 OUT1–OUT8 status | 8 inputs; LOW=Active, HIGH=Inactive | TBD | 现有系统级 interface contract；exact MCU pins 留待 Stage 3 |
| USB-UART | Bidirectional UART | TBD USART | 现有 frame/model 尽量复用；USB-UART IC 未选择 |
| Sensor inputs | 4 × NO or 4 × (NO+NC) | TBD | 由 OPEN-002 决定 4 或 8 个 MCU inputs |
| SWD / reset / boot | Programming, debug and safe startup | TBD | Stage 3 必须覆盖；不在 Stage 1 设具体外围值 |

## PCB Inputs

- Mechanical constraints（机械约束）：terminal 倾向约 5.0/5.08 mm、可插拔螺钉端子可评估；PCB size、enclosure、安装孔和连接器最终系列待确认。
- Sensitive or high-risk areas（敏感或高风险区域）：24 V 输入与保护、长线 CM35/Sensor I/O、USB/机器地边界、clock/VDDA、reset/boot、安全默认状态。
- Power and thermal constraints（电源与热约束）：完整 load budget、DC/DC efficiency/thermal、4 个传感器电流与保护器件耗散待 Stage 2/3 计算。
- Required official layout sources（所需官方 Layout 资料）：MCU、USB-UART/隔离器、DC/DC/保护器件、CM35与Sensor前端关键器件的官方 datasheet/application note；具体清单随 Stage 2 候选建立。

## Open Decisions

| ID | Decision Needed | Affected Stage | Resolution Source | Resolution State |
| --- | --- | --- | --- | --- |
| DN-001 | USB-UART galvanic isolation architecture | Before Stage 2 selection | 用户现场接地信息 + 风险分析 + 候选官方资料 | Open |
| DN-002 | Sensor NO only vs NO + NC | Before Stage 2 selection | 用户应用/诊断需求 | Open |
| DN-003 | Power/protection architecture | Stage 2 | Load budget、现场 transient boundary、官方资料 | Open |
| DN-004 | GPIO / USART allocation and safe-state implementation | Stage 3 | MCU resource plan、reset/boot behavior、schematic analysis | Open |
| DN-005 | Mechanical envelope, terminals and indicators | Stage 2; freeze by Stage 5 | 用户机械/维护需求、装配能力 | Open |
