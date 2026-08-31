# Design Notes

本文件记录整板架构、系统级设计意图、接口/跨模块约定和架构权衡；候选方案在形成依据前不得写成已选事实。已有 module design record 负责的逐引脚连接、普通 R/C 值和模块计算无需在此并行维护。

## Board-level Intent

- 新板以 STM32F103C8T6 直接集成为基础，不再依赖外购 minimum-system module；面向 JLCPCB SMT / PCBA。
- USB-to-serial 功能板载，USB-UART 与 STM32 UART 之间采用 galvanic isolation；`USB_GND` 与 machine-side `GND` 不直接共地。
- CM35 实际提供 IN1–IN18 与 OUT1–OUT8；本板使用 IN11–IN18 和 OUT1–OUT8，IN1–IN10 不属于本板控制范围。当前 reserved channels 仍是硬件边界的一部分。
- 上一代 CM35 I/O 功能行为可作为 Legacy Functional Baseline。Stage 2 已检查归档上一代原理图，确认其电平转换主要使用 2N7002 MOSFET networks；用户已明确授权复用该转换思路，但 exact connection、resistor values 和 protection 不自动成为新板已验证事实。
- 用户提供的 CM35 official-manual pages 确认：输入下拉至 `24G` 时为“通”，输入带抗干扰过滤且信号需保持至少约 2 ms；输出接线为负载位于 `+24 V` 与 OUT 之间，因此按 low-side / sinking behavior 处理，不推断未公开的内部 transistor topology。
- CM35 `V/G` 是 I/O 隔离 24 V 供电端，`24V/0V` 是 controller system supply。Rev.A 采用两套独立、隔离输出的 24 V switching PSU：PSU A 只供 CM35 system `24V/0V`；PSU B 直接分配至 CM35 I/O `V/G` 和 PCB `24V/GND`。PCB `GND = CM35 G / 24G = PSU B -V`，不得直接连接 CM35 system `0V`、PSU A `-V`、PE 或 chassis。用户已确认实际设备存在 IN15–IN18。
- 4 个传感器每个都提供 `+24V_PROTECTED / GND / NO / NC` 端子，并采集全部 NO + NC，共 8 路 sensor digital inputs；M5 全 8 路 2N7002 + series resistor + field-side TVS capture 已完成当前会话 screenshot-level completeness review。
- 板级设计优先考虑工业长线保护、safe startup、现场接线可维护性和首次限流上电。

## Current Decisions

| Architecture Fact | Current Position | Basis |
| --- | --- | --- |
| 主控 | STM32F103C8T6 直接集成到 PCB；M2 current-session module closeout acceptable | 用户确认的项目目标；Stage 2 qualification + Stage 3 user/ChatGPT session review |
| CM35 channel scope | CM35 提供 IN1–IN18 / OUT1–OUT8；本板使用 IN11–IN18 / OUT1–OUT8 | 用户确认的系统边界；IN15–IN18 已由用户针对实际设备确认 |
| Protocol polarity | Application `1=Active`; physical GPIO Active-Low; firmware inversion | 已验证系统行为与用户提供的 interface contract |
| CM35 / Sensor conversion | 复用 legacy 2N7002 MOSFET conversion approach；Primary device = Nexperia 2N7002,215 | 用户授权 + archived legacy schematic review + Nexperia official data |
| CM35 Rev.A power domain | PSU A -> CM35 system `24V/0V`；独立 PSU B -> CM35 I/O `V/G` + PCB `24V/GND`；`PCB GND = CM35 G / 24G`，且 `PSU A -V != PSU B -V`；不增加 per-channel isolation | CM35 official-manual evidence + 用户最终系统架构决策 |
| M4 module status | 16-channel CM35 interface 与 safe-startup design / current-session capture `CLOSEOUT ACCEPTABLE` | Stage 3 user-provided Altium screenshots；不代表 ERC、footprint 或 Stage 4 结果 |
| Sensor acquisition | 每个传感器独立 `+24V/0V/NO/NC` 端子并采集 NO+NC，共 8 路 inputs | 用户确认；OPEN-002 |
| M5 frontend status | 8-channel capture `CLOSEOUT ACCEPTABLE` | 全 8 路 current-session screenshot-level completeness review + Littelfuse official SMF30A data |
| USB-UART / isolation | USB side `USB_VBUS/USB_GND` ↔ ISO7721DR ↔ STM32 USART1 on machine-side `3V3/GND`; M3 current-session closeout acceptable | Stage 2 selection + Stage 3 manufacturer-data review + user-provided Altium screenshot |
| 24 V input protection | 0468.500NRHF 0.5 A / 63 V Slo-Blo fuse + STPS2H100A series reverse-polarity protection + SMBJ30A-TR TVS -> protected 24V bus | Stage-2 0.225 A continuous design envelope + Littelfuse/ST official data；OPEN-005 |
| 24 V -> 3.3 V | LMR36510FADDAR synchronous buck | Stage 2 official-source qualification；OPEN-006 |

M1 当前 schematic architecture 已细化并达到 current-session module closeout acceptable；exact connections、values、L1 decision 与 validation boundary 由 `docs/module_design/m1_power.md` 持有。M3 的 exact USB/UART connections、power-state/default behavior、shield termination 与 module-specific layout details 由 `docs/module_design/m3_usb_uart_isolation.md` 持有。M4/M5 的 channel-level mapping、values、connector pin order 与 evidence boundary 分别由 `docs/module_design/m4_cm35_io.md` 和 `docs/module_design/m5_sensor_interface.md` 持有。

## Power and Interfaces

| Domain / Interface | Source | Destination | Required Boundary |
| --- | --- | --- | --- |
| CM35 system power | Isolated-output PSU A | CM35 `24V/0V` only | PSU A `-V` 不得直接连接 PSU B `-V`、PCB `GND`、CM35 `G/24G`、PE 或 chassis |
| Isolated I/O power | Independent isolated-output PSU B | Cabinet-direct CM35 `V/G` distribution + PCB M1 input | `PCB GND = CM35 G / 24G = PSU B -V`；CM35 `V/G` 不经过 PCB F1 |
| PC communication | PC USB | USB-C -> USBLC6-2SC6 -> CH340C -> ISO7721DR -> STM32 USART1 | `USB_GND` 与 machine `GND` 不直接共地；两侧分别由 `USB_VBUS` 与 `3V3` 供电；不得 back-power machine side |
| CM35 control | STM32 GPIO | 2N7002 conversion -> CM35 IN11–IN18 | Shared PSU-B I/O-domain `GND` / `G / 24G` reference；pull-to-24G active；reset/boot safe inactive；M4 closeout acceptable |
| CM35 status | CM35 OUT1–OUT8 | 2N7002 conversion -> STM32 GPIO | Shared PSU-B I/O-domain reference；CM35 low-side / sinking behavior；firmware 转正逻辑 DataOut；M4 closeout acceptable |
| Sensors | 4 × 24 V NPN NO+NC | `24V_PROTECTED` + 2N7002-based input conversion -> STM32 | Same PSU-B I/O domain；8 路 inputs；M5 closeout acceptable |

## Rev.A System Power-domain Architecture

```text
CM35 System Domain
  PSU A +24 V -> CM35 24V
  PSU A -V    -> CM35 0V

Isolated I/O Domain
  PSU B +24 V -> CM35 V             (cabinet terminal distribution)
  PSU B -V    -> CM35 G / 24G       (cabinet terminal distribution)
  PSU B +24 V -> PCB 24V input
  PSU B -V    -> PCB GND
                 -> PCB M1 -> F1 -> reverse-polarity protection
                 -> 24V_PROTECTED -> M4 pull-ups / M5 sensors / LMR36510 -> 3V3

Isolation rule: PSU A -V != PSU B -V
```

CM35 `V/G` is not powered through PCB F1 or `24V_PROTECTED`, and the PCB does not add a CM35 `V/G` power-output connector. Exact PSU-B procurement, manufacturer, and current rating remain later system-integration items.

## 24 V Source Evidence Boundary

- 用户提供的现有电源图片标示型号 `MS-120-24`、输出 24 V / 5 A、120 W。
- 用户已用万用表确认当前实际输出约 24 V 且观察较稳定。
- 该信息支持当前 24 V nominal design point，但不是 manufacturer official regulation/surge specification；不得据此声称满足特定 IEC surge 等级或长期 tolerance。
- 外部 PSU 的 5 A capability 不是 PCB input fuse/current-limit rating。板上 overcurrent element 必须按本板实际 load budget 与 fault-energy requirement 另行确定。

## M1 Power Architecture Decision

Current board-level architecture:

```text
PSU B +24V -> PCB 24V INPUT
  -> 0468.500NRHF 0.5 A / 63 V Slo-Blo fuse
  -> STPS2H100A series reverse-polarity diode
  -> 24V_PROTECTED
       -> SMBJ30A-TR to GND
       -> M4 pull-ups / M5 sensors
       -> LMR36510FADDAR -> 3V3
```

- LMR36510FADDAR is a 4.2–65 V, 1 A synchronous buck with high-voltage transient tolerance class suitable for this nominal 24 V architecture.
- SMBJ30A-TR uses a 30 V stand-off level so it remains off at the measured ~24 V operating point while providing transient suppression below the converter absolute high-voltage boundary under the currently assumed source conditions.
- M1 current-session module design / EDA capture closeout is acceptable；exact values and remaining validation boundaries are maintained in `docs/module_design/m1_power.md`，not duplicated here.
- Exact surge waveform/source impedance, startup/inrush coordination、capacitor DC-bias、thermal and layout verification remain open；no compliance claim is made.

## Stage-2 Bounding Power Budget

本预算只用于 PCB branch 及其 board-powered loads 的关键器件 current-class selection；它不是 Stage-3 ripple、magnetics、startup 或 thermal calculation，也不是包含 CM35 I/O consumption 在内的完整 PSU-B cabinet-supply sizing value。本 transaction 不重新计算或指定 PSU-B rating。

| Load | Stage-2 allowance | Basis / limitation |
| --- | ---: | --- |
| 4 × AN-LS18-40-N sensor supply | ≤40 mA @ 24 V | User-provided manual states ≤10 mA each；manufacturer provenance provisional |
| CM35 16-channel interface circuitry | 80 mA @ 24 V | Conservative PCB-side 5 mA/channel allocation；exact CM35 input current/output-load parameters remain formal-review inputs and do not size the complete PSU-B cabinet supply |
| STM32F103C8T6 | 60 mA @ 3.3 V | Conservative architecture allowance, not an operating-point prediction |
| ISO7721 machine-side supply | 10 mA @ 3.3 V | Includes logic-rate allowance |
| Machine-side pull-ups / interface logic | 40 mA @ 3.3 V | Bounding allocation pending exact values |
| Indicators / ordinary support | 40 mA @ 3.3 V | Optional-support allowance |
| 3.3 V engineering reserve | 100 mA @ 3.3 V | Raises the 3.3 V design envelope to 250 mA |

At 24 V and a deliberately conservative 75% buck-efficiency assumption, 250 mA at 3.3 V corresponds to about 46 mA input. Sensors + CM35 allocation + buck input total about 166 mA; the Stage-2 24 V continuous design envelope is rounded up to **225 mA**, leaving about 59 mA additional board-level reserve.

The historical CM35 interface allocation in this Stage-2 envelope bounded PCB-side interface pull-ups and related board circuitry; it must not be interpreted as the complete cabinet-distributed CM35 `V/G` supply current. Final PSU-B sizing must include the actual CM35 I/O-domain load separately.

## Stage 3 Cross-Module Integration Closeout

- Power Flow: PSU A and PSU B domains are explicitly separated; the PSU-B PCB branch feeds M1/F1, `24V_PROTECTED`, sensors, M4 pull-ups, and `3V3`, while CM35 `V/G` is cabinet-fed directly.
- Signal / Control Flow: USB-UART, STM32, CM35 IN/OUT, and all eight sensor NO/NC mappings are recorded without responsibility gaps.
- Voltage / Logic Compatibility: M4 and M5 retain the reviewed 2N7002 Active-Low translation; USB/machine isolation remains unchanged.
- Startup / Shutdown / Fault State: M4 safe-startup remains hardware-enforced; USB back-power and unverified transient/thermal behavior remain explicit later-review boundaries.
- Cross-sheet Net Consistency: current-session visible evidence uses `3V3`, `24V_PROTECTED`, `GND`, `USB_GND`, and the recorded channel names consistently; this is screenshot/PDF evidence, not `.SchDoc` object parsing.
- Missing / Conflicting Responsibility: no Stage-3 module responsibility conflict remains. The complete same-date schematic PDF and BOM are available locally, so the Stage-3 conclusion is **READY FOR SCHEMATIC REVIEW**.

- LMR36510FADDAR：0.25 A output envelope versus 1 A rating → current-class margin PASS。
- STPS2H100A：0.225 A input envelope versus 2 A rating → current-class margin PASS；exact forward-loss/thermal verification remains Stage 3。
- External PSU 5 A capability is not used in this calculation.

## F1 Overcurrent Decision

- Primary：Littelfuse `0468.500NRHF`，0.5 A / 63 V，1206 Slo-Blo fuse，LCSC C206993。
- Manufacturer basis：50 A interrupting rating at 63 VAC/VDC；time-delay behavior is specified to tolerate inrush. Littelfuse requires a standard 25% continuous-operation derating plus temperature re-rating. At 70°C the datasheet example gives usable continuous current `0.75 × 0.80 × 0.5 A = 0.30 A`, still about 33% above the 0.225 A envelope.
- Startup boundary：0.5 A is accepted because the time-delay characteristic provides input-capacitor/startup tolerance without moving immediately to a 1 A class. Final startup/inrush and local-temperature evidence remain later verification inputs. If allowable continuous current falls to or below 0.225 A, or startup nuisance opening is predicted, reassess the 468 Series 1 A member and verify its exact orderable MPN rather than silently changing F1.
- Fault boundary：the 50 A interrupt rating does not by itself prove coordination with the PSU peak fault current or field wiring；those source/fault-path inputs remain unverified, and no system safety-standard claim is made.
- Alternate architecture：Littelfuse `1210L035/60PR` PPTC，0.35 A hold / 0.70 A trip at 20°C，60 V max，10 A max fault current. It is not Primary because hold current falls to 0.24 A at 60°C and 0.21 A at 70°C, its resistance can rise to 1.5 Ω after trip/reflow, it dissipates about 1.5 W tripped, and it continues residual current during a sustained fault. Use only after application-temperature、voltage drop/heating、trip/recovery and sustained-fault verification.

## M3 Isolation Architecture Decision

- M3 keeps the PC USB domain (`USB_VBUS/USB_GND`) galvanically isolated from the machine domain (`3V3/GND`) through ISO7721DR; `USB_GND` must not connect directly to machine `GND`.
- STM32 USART1 remains PA9 = `MCU_UART_TX` and PA10 = `MCU_UART_RX`; M3 current-session module closeout is acceptable.
- Exact USB-C / USBLC6-2SC6 / CH340C / ISO7721 connections, channel direction, default-HIGH / power-state reasoning, shield termination and module-specific layout constraints are owned by `docs/module_design/m3_usb_uart_isolation.md` and are not duplicated here.

## Pin and Connection Planning

只有真实 Project decision 已形成依据时，才记录 board-level pin/function constraints、项目网络名或跨模块 mapping；module-specific pin-by-pin implementation 由启用后的 module design record 维护。

| Function | Required Direction / Behavior | Frozen Mapping | Basis |
| --- | --- | --- | --- |
| CM35 IN11–IN18 control | 8 outputs; LOW=Active, HIGH=Inactive | PB0 / PB1 / PB5 / PB6 / PB7 / PA8 / PA11 / PA12 | M4 external network must enforce safe inactive startup |
| CM35 OUT1–OUT8 status | 8 inputs; LOW=Active, HIGH=Inactive | PA0–PA7 | Preserves one-to-one EXTI0–EXTI7 allocation |
| USB-UART | Bidirectional USART1 | PA9 = MCU_UART_TX；PA10 = MCU_UART_RX | STM32 ↔ ISO7721DR ↔ CH340C；M3 current module closeout acceptable |
| Sensor inputs | 4 × (NO+NC) = 8 inputs | PB8–PB15 | Preserves one-to-one EXTI8–EXTI15 allocation |
| SWD | Programming and debug | PA13 = SWDIO；PA14 = SWCLK | 1×5 current interface also carries VTREF / 3V3, GND and NRST |
| Boot / clock | Main Flash baseline；8 MHz HSE | PB2 = BOOT1；PD0 = OSC_IN；PD1 = OSC_OUT | BOOT0/BOOT1 default LOW；LSE not fitted |

PA0–PA7 and PB8–PB15 intentionally avoid EXTI line-number conflicts across all 16 external inputs. PA15 / PB3 / PB4 are SWJ/JTAG-related pins at reset；future GPIO use requires firmware to release JTAG resources. M2 does not depend on MCU reset GPIO state for CM35 safety: M4 implements the cross-module contract `MCU high-Z -> 3V3 pull-up -> 2N7002 OFF -> 24 V side HIGH -> CM35 inactive`; current-session screenshots support module closeout, while `.SchDoc` parsing、ERC and hardware behavior remain unverified.

## PCB Inputs

- Mechanical constraints：M4 CM35 使用 3.81 mm 8P pluggable terminal，M5 Sensor 使用 3.81 mm 4P pluggable terminal；final mating、board-edge access、enclosure 与 mechanical acceptance 仍后置到 Stage 5 Layout Preflight。
- Sensitive or high-risk areas：24 V input protection、long-line CM35/Sensor I/O、USB/machine isolation boundary、clock/VDDA、reset/boot、安全默认状态。
- Power and thermal constraints：Stage-2 bounding load budget 与 F1 current class 已关闭；M1 Stage-3 external values and L1 are recorded, while exact capacitor qualification、thermal、startup 与 TVS/fuse interaction remain later validation items。
- M3 layout boundary：USBLC6 靠近 USB-C，USB ESD return 保持短；CH340C 与 ISO7721 decoupling 靠近对应 pin；不得用 copper/pour/via/test point 跨接 `USB_GND` 与 `GND`；isolator barrier 区域保持所需 creepage/clearance。
- Required official layout sources：STM32、CH340C、ISO7721DR、LMR36510、STPS2H100A、SMBJ30A、USBLC6-2SC6、2N7002 及 CM35/Sensor external-interface data。

## Open Decision References

Open Question 与 decision status 只在 `requirements.md` 的 `OPEN-xxx` 表维护。本文件仅记录架构影响，不建立第二套状态：OPEN-005/006 已在 Stage 2 形成 architecture decision；OPEN-007/008 已在 Stage 3 关闭；OPEN-003/004/009/010 仍按 `requirements.md` 维护。
