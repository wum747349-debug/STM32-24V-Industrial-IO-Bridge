# Design Notes

本文件记录整板架构、系统级设计意图、接口/跨模块约定和架构权衡；候选方案在形成依据前不得写成已选事实。已有 module design record 负责的逐引脚连接、普通 R/C 值和模块计算无需在此并行维护。

## Board-level Intent

- 新板以 STM32F103C8T6 直接集成为基础，不再依赖外购 minimum-system module；面向 JLCPCB SMT / PCBA。
- USB-to-serial 功能板载，USB-UART 与 STM32 UART 之间采用 galvanic isolation；PC USB ground 与 machine-side 24 V `0V` 不直接共地。
- CM35 实际提供 IN1–IN18 与 OUT1–OUT8；本板使用 IN11–IN18 和 OUT1–OUT8，IN1–IN10 不属于本板控制范围。当前 reserved channels 仍是硬件边界的一部分。
- 上一代 CM35 I/O 功能行为可作为 Legacy Functional Baseline。Stage 2 已检查归档上一代原理图，确认其电平转换主要使用 2N7002 MOSFET networks；用户已明确授权复用该转换思路，但 exact connection、resistor values 和 protection 不自动成为新板已验证事实。
- 4 个传感器每个都提供 `+24V / 0V / NO / NC` 端子，并采集全部 NO + NC，共 8 路 sensor digital inputs；Stage 2 Primary conversion device 为 Nexperia 2N7002,215，外部 protection/filter details 仍待 Stage 3。
- 板级设计优先考虑工业长线保护、safe startup、现场接线可维护性和首次限流上电。

## Current Decisions

| Architecture Fact | Current Position | Basis |
| --- | --- | --- |
| 主控 | STM32F103C8T6 直接集成到 PCB；implementation not started | 用户确认的项目目标；Stage 2 official-source qualification |
| CM35 channel scope | CM35 提供 IN1–IN18 / OUT1–OUT8；本板使用 IN11–IN18 / OUT1–OUT8 | 用户确认的系统边界 |
| Protocol polarity | Application `1=Active`; physical GPIO Active-Low; firmware inversion | 已验证系统行为与用户提供的 interface contract |
| CM35 / Sensor conversion | 复用 legacy 2N7002 MOSFET conversion approach；Primary device = Nexperia 2N7002,215 | 用户授权 + archived legacy schematic review + Nexperia official data |
| Sensor acquisition | 每个传感器独立 `+24V/0V/NO/NC` 端子并采集 NO+NC，共 8 路 inputs | 用户确认；OPEN-002 |
| USB-UART / isolation | CH340C -> ISO7721DR -> STM32 UART；USB ground 与 machine-side 0V 不直连 | Stage 2 selection；OPEN-001 |
| 24 V input protection | input overcurrent element + STPS2H100A series reverse-polarity protection + SMBJ30A-TR TVS -> protected 24V bus | 用户明确要求防反接；Stage 2 qualification；OPEN-005 |
| 24 V -> 3.3 V | LMR36510FADDAR synchronous buck | Stage 2 official-source qualification；OPEN-006 |

## Power and Interfaces

| Domain / Interface | Source | Destination | Required Boundary |
| --- | --- | --- | --- |
| Machine power | External 24 V DC | M1 -> protected 24V bus / 3.3 V | reverse-polarity、overcurrent、surge/transient、长线；首次上电可限流 |
| PC communication | PC USB | CH340C -> ISO7721DR -> STM32 UART | PC GND 与 machine 24 V 0V 不直接共地；不得 back-power machine side |
| CM35 control | STM32 GPIO | 2N7002 conversion -> CM35 IN11–IN18 | Active-Low physical contract；reset/boot safe inactive |
| CM35 status | CM35 OUT1–OUT8 | 2N7002 conversion -> STM32 GPIO | Active-Low physical status；firmware 转正逻辑 DataOut |
| Sensors | 4 × 24 V NPN NO+NC | protected 24V + 2N7002-based input conversion -> STM32 | 8 路 inputs；工业长线 protection/current limiting/filtering 仍需 Stage 3 qualification |

## 24 V Source Evidence Boundary

- 用户提供的现有电源图片标示型号 `MS-120-24`、输出 24 V / 5 A、120 W。
- 用户已用万用表确认当前实际输出约 24 V 且观察较稳定。
- 该信息支持当前 24 V nominal design point，但不是 manufacturer official regulation/surge specification；不得据此声称满足特定 IEC surge 等级或长期 tolerance。
- 外部 PSU 的 5 A capability 不是 PCB input fuse/current-limit rating。板上 overcurrent element 必须按本板实际 load budget 与 fault-energy requirement 另行确定。

## M1 Power Architecture Decision

Current Stage 2 architecture:

```text
24V INPUT
  -> input overcurrent element (exact part/rating deferred)
  -> STPS2H100A series reverse-polarity diode
  -> 24V_PROTECTED
       -> SMBJ30A-TR to 0V
       -> Sensor / CM35 interface 24 V needs
       -> LMR36510FADDAR -> 3V3_MACHINE
```

- LMR36510FADDAR is a 4.2–65 V, 1 A synchronous buck with high-voltage transient tolerance class suitable for this nominal 24 V architecture.
- SMBJ30A-TR uses a 30 V stand-off level so it remains off at the measured ~24 V operating point while providing transient suppression below the converter absolute high-voltage boundary under the currently assumed source conditions.
- Exact surge waveform/source impedance, input bulk capacitance, fuse/PTC behavior and thermal margin remain design calculations, not Stage 2 PASS claims.

## M3 Isolation Architecture Decision

```text
USB-C / USB_GND domain
  -> USBLC6-2SC6
  -> CH340C
  -> ISO7721DR isolation barrier
  -> STM32 UART / machine-side 3.3 V domain
```

- ISO7721DR provides one forward and one reverse digital channel, matching UART TX/RX direction needs.
- USB side and machine side can each power their own side of the isolator; an isolated DC/DC is not automatically required solely to power the isolator because both domains already have independent supplies.
- Stage 3 must still verify exact supply pins, decoupling, power-off behavior, UART idle state and no-back-power conditions.

## Pin and Connection Planning

只有真实 Project decision 已形成依据时，才记录 board-level pin/function constraints、项目网络名或跨模块 mapping；module-specific pin-by-pin implementation 由启用后的 module design record 维护。

| Function | Required Direction / Behavior | Candidate Mapping | Basis |
| --- | --- | --- | --- |
| CM35 IN11–IN18 control | 8 outputs; LOW=Active, HIGH=Inactive | TBD MCU pins | exact MCU pins 留待 Stage 3；2N7002 conversion approach 已选 |
| CM35 OUT1–OUT8 status | 8 inputs; LOW=Active, HIGH=Inactive | TBD MCU pins | exact MCU pins 留待 Stage 3；legacy MOSFET readback wording 已纠正 |
| USB-UART | Bidirectional UART | TBD USART | CH340C + ISO7721DR 已选；exact USART / pins 留待 Stage 3 |
| Sensor inputs | 4 × (NO+NC) = 8 inputs | TBD MCU pins | OPEN-002 已确认通道数量；2N7002 Primary 已选 |
| SWD / reset / boot | Programming, debug and safe startup | TBD | Stage 3 必须覆盖；不在 Stage 2 固化普通外围值 |

## PCB Inputs

- Mechanical constraints：terminal 倾向约 5.0/5.08 mm、可插拔螺钉端子可评估；PCB size、enclosure、安装孔和连接器最终系列待确认。
- Sensitive or high-risk areas：24 V input protection、long-line CM35/Sensor I/O、USB/machine isolation boundary、clock/VDDA、reset/boot、安全默认状态。
- Power and thermal constraints：完整 load budget、LMR36510 external component values / thermal、STPS2H100A dissipation、TVS/fuse interaction 待 Stage 3 计算。
- Required official layout sources：STM32、CH340C、ISO7721DR、LMR36510、STPS2H100A、SMBJ30A、USBLC6-2SC6、2N7002 及 CM35/Sensor external-interface data。

## Open Decision References

Open Question 与 decision status 只在 `requirements.md` 的 `OPEN-xxx` 表维护。本文件仅记录架构影响，不建立第二套状态：OPEN-005/006 已在 Stage 2 形成 architecture decision；OPEN-003/004/007/008/009/010 仍按 `requirements.md` 维护。
