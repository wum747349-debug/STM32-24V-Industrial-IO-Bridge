# Design Notes

本文件记录整板架构、系统级设计意图、接口/跨模块约定和架构权衡；候选方案在形成依据前不得写成已选事实。已有 module design record 负责的逐引脚连接、普通 R/C 值和模块计算无需在此并行维护。

## Board-level Intent

- 新板以 STM32F103C8T6 直接集成为基础，不再依赖外购 minimum-system module；面向 JLCPCB SMT / PCBA。
- USB-to-serial 功能板载，USB-UART 与 STM32 UART 之间采用 galvanic isolation；PC USB ground 与 machine-side 24 V `0V` 不直接共地。具体 USB-UART、digital isolator 与实现参数仍待 Stage 2/3 qualification（见 `requirements.md` 的 OPEN-001）。
- CM35 实际提供 IN1–IN18 与 OUT1–OUT8；本板使用 IN11–IN18 和 OUT1–OUT8，IN1–IN10 不属于本板控制范围。当前 reserved channels 仍是硬件边界的一部分。
- 上一代 CM35 I/O 功能行为可作为 Legacy Functional Baseline，但旧器件和旧连接不自动成为本项目当前设计决定。
- 4 个传感器每个都提供 `+24V / 0V / NO / NC` 端子，并采集全部 NO + NC，共 8 路 sensor digital inputs（见 `requirements.md` 的 OPEN-002）；具体 frontend 仍待 Stage 2/3。
- 板级设计优先考虑工业长线保护、safe startup、现场接线可维护性和首次限流上电。

## Current Decisions

| Architecture Fact | Current Position | Basis |
| --- | --- | --- |
| 主控 | STM32F103C8T6 直接集成到 PCB；implementation not started | 用户确认的项目目标 |
| CM35 channel scope | CM35 提供 IN1–IN18 / OUT1–OUT8；本板使用 IN11–IN18 / OUT1–OUT8 | 用户确认的系统边界 |
| Protocol polarity | Application `1=Active`; physical GPIO Active-Low; firmware inversion | 已验证系统行为与用户提供的 interface contract |
| Sensor acquisition | 每个传感器独立 `+24V/0V/NO/NC` 端子并采集 NO+NC，共 8 路 inputs | 用户确认；OPEN-002 |
| USB isolation | Board-mounted USB-UART + galvanically isolated UART interface；具体器件未选择 | 用户确认；OPEN-001 |

## Power and Interfaces

| Domain / Interface | Source | Destination | Required Boundary |
| --- | --- | --- | --- |
| Machine power | External 24 V DC | M1 → protected 24V bus / low voltage | 反接、surge/transient、长线；首次上电可限流 |
| PC communication | PC USB | M3 → isolated STM32 UART | 板载 USB-UART；PC GND 与 machine 24 V 0V 不直接共地；不得 back-power machine side |
| CM35 control | STM32 GPIO | M4 → CM35 IN11–IN18 | Active-Low physical contract；reset/boot safe inactive |
| CM35 status | CM35 OUT1–OUT8 | M4 → STM32 GPIO | Active-Low physical status；firmware 转正逻辑 DataOut |
| Sensors | 4 × 24 V NPN NO+NC | M5 → STM32 | 8 路 inputs；工业长线 protection/current limiting/filtering；frontend 待定 |

## Pin and Connection Planning

只有真实 Project decision 已形成依据时，才记录 board-level pin/function constraints、项目网络名或跨模块 mapping；module-specific pin-by-pin implementation 由启用后的 module design record 维护。

| Function | Required Direction / Behavior | Candidate Mapping | Basis |
| --- | --- | --- | --- |
| CM35 IN11–IN18 control | 8 outputs; LOW=Active, HIGH=Inactive | TBD | 现有系统级 interface contract；exact MCU pins 留待 Stage 3 |
| CM35 OUT1–OUT8 status | 8 inputs; LOW=Active, HIGH=Inactive | TBD | 现有系统级 interface contract；exact MCU pins 留待 Stage 3 |
| USB-UART | Bidirectional UART | TBD USART | 现有 frame/model 尽量复用；USB-UART IC 未选择 |
| Sensor inputs | 4 × (NO+NC) = 8 inputs | TBD | OPEN-002 已确认通道数量；exact MCU pins 留待 Stage 3 |
| SWD / reset / boot | Programming, debug and safe startup | TBD | Stage 3 必须覆盖；不在 Stage 1 设具体外围值 |

## PCB Inputs

- Mechanical constraints（机械约束）：terminal 倾向约 5.0/5.08 mm、可插拔螺钉端子可评估；PCB size、enclosure、安装孔和连接器最终系列待确认。
- Sensitive or high-risk areas（敏感或高风险区域）：24 V 输入与保护、长线 CM35/Sensor I/O、USB/机器地边界、clock/VDDA、reset/boot、安全默认状态。
- Power and thermal constraints（电源与热约束）：完整 load budget、DC/DC efficiency/thermal、4 个传感器电流与保护器件耗散待 Stage 2/3 计算。
- Required official layout sources（所需官方 Layout 资料）：MCU、USB-UART/隔离器、DC/DC/保护器件、CM35与Sensor前端关键器件的官方 datasheet/application note；具体清单随 Stage 2 候选建立。

## Open Decision References

Open Question 与 decision status 只在 `requirements.md` 的 `OPEN-xxx` 表维护。本文件仅记录架构影响，不建立第二套状态：power/protection 见 OPEN-005/006，GPIO/USART 见 OPEN-007，具体 isolation/sensor-interface components 见 OPEN-008，mechanical/terminals/indicators 见 OPEN-003/004/009/010。
