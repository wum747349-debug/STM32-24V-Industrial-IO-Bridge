# Critical Component Selection Plan

本文件是 Stage 2 — Critical Component Selection 的 selection decision 主记录。关键器件先于普通外围器件确定；本文件不构成最终 BOM、EDA implementation 或 Stage completion 证明。

## Stage 2 Current State

- Selection activity：Closeout complete
- Critical component candidates：Recorded
- Primary decisions：Recorded for current first-pass scope
- Deferred peripherals：Routed to Stage 3 / Stage 5 owners；not Stage-2 blockers
- EDA implementation：Not started
- Stage 2 complete：YES
- Closeout decision：PASS

## Confirmed Inputs

- 主控：STM32F103C8T6 直接集成到 PCB。
- 通信：board-mounted USB-UART，经 galvanically isolated UART interface 连接 machine-side STM32；PC USB ground 与 machine-side 24 V `0V` 不直接共地。
- CM35：使用 IN11–IN18 与 OUT1–OUT8，共 8 路 control + 8 路 status；physical interface 为 Active-Low contract。
- Sensor acquisition：4 个 AN-LS18-40-N 的 NO + NC 均采集，共 8 路 digital inputs。
- 制造目标：JLCPCB / LCSC 与 SMT / PCBA preferred。
- 24 V source：用户提供的电源图片显示 `MS-120-24`、24 V / 5 A / 120 W；用户已用万用表确认当前实际输出约 24 V 且观察较稳定。该测量只证明当前 operating point，不证明电源 tolerance、surge 或 protection performance。
- Legacy conversion：用户明确授权复用上一代 I/O 转换思路；已检查归档旧原理图，主要转换器件为 2N7002 MOSFET，而不是 optocoupler。新设计仍需在 Stage 3 对 exact connection、resistor values、safe state 与 external-interface protection 重新核对。
- CM35 official I/O evidence：用户提供的官方资料页面确认 input pull-to-24G active、输入过滤要求信号保持至少约 2 ms、OUT1–OUT8 采用 low-side/sinking external connection、`V/G` 为 I/O 隔离 24 V power domain；不据此声称 exact threshold/current 或内部 transistor topology。
- Channel scope：用户已明确确认实际使用设备存在 IN15–IN18，Project 继续保留 IN11–IN18 + OUT1–OUT8。

## Primary Candidate Table

Availability 为 2026-08-29 的 point-in-time procurement evidence；未取得明确库存数量时不推断库存状态。

| Module | Function | JLC C# | Manufacturer | MPN | Package | Availability | Key requirements / qualification basis | Datasheet verified | Decision | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| M2 | MCU | C8734 | STMicroelectronics | STM32F103C8T6 | LQFP-48 | Unknown | 2.0–3.6 V、72 MHz、37 I/O class、USART/SWD resources；Project requirement 指定 | Yes | Primary | Exact GPIO / clock / boot / reset / VDDA implementation 留待 Stage 3 |
| M3 | USB-UART | C84681 | WCH | CH340C | SOP-16 | Good | USB 2.0 Full-Speed to UART、3.3/5 V supply、built-in clock、2 Mbps class | Yes | Primary | -20~+70 °C；若后续环境温度要求超出范围需重新评估 |
| M3 | UART galvanic isolation | C366164 | Texas Instruments | ISO7721DR | SOIC-8 | Unknown | 2 channels, 1 forward + 1 reverse；2.25–5.5 V each side；default output HIGH；适合 UART TX/RX domain isolation | Yes | Primary | USB side 与 machine side 分别由各自电源域供电；不因此声称 system-level isolation certification |
| M3 | USB data ESD | C7519 | STMicroelectronics | USBLC6-2SC6 | SOT-23-6L | Unknown | 2-line USB 2.0 high-speed ESD protection；low line capacitance | Yes | Primary | Placement / routing / VBUS connection 留待 Stage 3/5 |
| M3 | USB-C receptacle | C165948 | Korean Hroparts Elec | TYPE-C-31-M-12 | SMD, right-angle, 16P | Unknown | USB 2.0 device connection；JLC/LCSC sourcing convenient | Supplier data | Conditional | Electrical use acceptable for current concept；mechanical/enclosure qualification remains OPEN-003 |
| M4/M5 | 24 V ↔ 3.3 V open-drain / pull-down conversion | C7420321 | Current supplier listing | 2N7002 | SOT-23 | Retained | Same C-number used on the previous working board；accepted for the current low-current level-translation application | Legacy/application evidence；Nexperia reference retained | Primary / retained | Do not require replacement with Nexperia `2N7002,215` solely because earlier documentation named it Primary；normal purchase-time identity and footprint checks still apply |
| M1 | 24 V → 3.3 V buck | C1858394 | Texas Instruments | LMR36510FADDAR | HSOIC/ESOP-8 | Good | 4.2–65 V input、1 A synchronous buck、400 kHz FPWM、70 V transient tolerance class、industrial-oriented protection features | Yes | Primary | Inductor、FB、input/output capacitors、thermal/load budget deferred to Stage 3 |
| M1 | Reverse-polarity protection | C81548 | STMicroelectronics | STPS2H100A | SMA (DO-214AC) | Unknown | 100 V / 2 A Schottky series diode；simple fail-safe reverse-polarity blocking for low-current 24 V control board | Yes | Primary | Forward drop / dissipation to be checked against final current budget |
| M1 | 24 V transient suppression | C133663 | STMicroelectronics | SMBJ30A-TR | SMB (DO-214AA) | Good | 30 V stand-off；600 W class 10/1000 µs TVS；selected above measured ~24 V steady source and below LMR36510 high-voltage boundary | Yes | Primary | ST table gives higher clamp under 8/20 µs high-current condition; Stage 3 must check source impedance, surge assumption and margin before claiming a compliance level |
| M1 | Input overcurrent protection | C206993 | Littelfuse | 0468.500NRHF | 1206 | Unknown | 0.5 A / 63 V Slo-Blo；50 A interrupt at 63 VAC/VDC；manufacturer continuous and temperature derating applied to 0.225 A design envelope | Yes | Primary | Final Cin/startup pulse and local-temperature check remain Stage 3 |

## Stage-2 Bounding Power Budget

This budget selects current classes only. It is not a detailed startup、ripple、magnetics、thermal or compliance calculation.

| Load | Bounding allowance | Evidence / limitation |
| --- | ---: | --- |
| 4 × AN-LS18-40-N static sensor supply | ≤40 mA @ 24 V | User manual states ≤10 mA each；manufacturer provenance provisional |
| CM35 16-channel interface circuitry | 80 mA @ 24 V | Conservative 5 mA/channel allocation；exact CM35 current/impedance is not known |
| STM32F103C8T6 | 60 mA @ 3.3 V | Conservative selection allowance |
| ISO7721 machine-side supply | 10 mA @ 3.3 V | Logic-rate allowance |
| Machine-side pull-ups / interface logic | 40 mA @ 3.3 V | Bounding allowance pending exact values |
| Indicator / support allowance | 40 mA @ 3.3 V | Ordinary peripheral allowance |
| 3.3 V engineering reserve | 100 mA @ 3.3 V | Total 3.3 V design envelope = 250 mA |

Using 75% buck efficiency for a deliberately conservative Stage-2 conversion, the 250 mA / 3.3 V output envelope draws about 46 mA at 24 V. Sensors + CM35 allocation + buck input total about 166 mA; rounding to a **225 mA continuous 24 V design envelope** adds about 59 mA board-level reserve.

Conclusions:

- LMR36510FADDAR：0.25 A envelope vs 1 A class → **PASS**, about 4× current-class headroom.
- STPS2H100A：0.225 A envelope vs 2 A class → **PASS**, about 8.9× current-class headroom before exact forward-loss/thermal calculation.
- Input protection：0.5 A time-delay fuse class is appropriate; external PSU 5 A is not used as F1 rating.

## Primary Decisions

### M1 — 24 V Input / Protection / Low-voltage Power

Current architecture decision:

```text
24V input
  -> 0468.500NRHF 0.5 A / 63 V Slo-Blo fuse
  -> STPS2H100A series reverse-polarity protection
  -> protected 24V bus
       -> SMBJ30A-TR to 0V for transient suppression
       -> Sensor / CM35 interface supply needs
       -> LMR36510FADDAR -> 3.3V machine-side rail
```

The external 24 V source has been measured by the user at approximately 24 V and observed stable. This supports the 30 V TVS stand-off choice for the current design assumption, but it is not a substitute for an official PSU tolerance/surge specification.

F1 rationale:

- Littelfuse specifies the 0.5 A 468 device for 50 A interrupting at 63 VAC/VDC and gives time-delay opening behavior suitable for inrush tolerance.
- Littelfuse requires 25% standard continuous derating plus temperature re-rating. Its 70°C example yields `0.75 × 0.80 × 0.5 A = 0.30 A`, about 33% above the 0.225 A Stage-2 envelope.
- Stage 3 must compare final DC/DC input capacitance and sensor startup with the time-current curve and verify local ambient. If usable continuous rating falls to or below 0.225 A, or nuisance opening is predicted, reassess the 468 Series 1 A member and verify its exact orderable MPN rather than silently increasing F1.
- The 50 A interrupting rating does not by itself prove coordination with the PSU peak fault current or field wiring；those source/fault-path inputs remain unverified, and no system safety-standard claim is made.

### M3 — USB-UART / Isolation

Current primary architecture:

```text
PC USB-C
  -> USBLC6-2SC6
  -> CH340C
  -> ISO7721DR isolation barrier
  -> STM32 UART
```

USB-side power/ground and machine-side 3.3 V / 0 V remain separate across the digital-isolator barrier. Detailed power-state, unplugged-state and back-power analysis remains a Stage 3 task.

### M4 / M5 — CM35 and Sensor I/O Conversion

The archived previous-generation schematic was reviewed in Stage 2 and shows repeated 2N7002 MOSFET conversion networks. The earlier project wording that described the legacy CM35 readback as optocoupler-based was inconsistent with that schematic evidence and is corrected in `requirements.md`.

The new board intentionally retains LCSC `C7420321` for the reused 2N7002 MOSFET conversion approach. The same C-number was used on the previous working board, and the present low-current level-translation application remains accepted. The earlier Nexperia `2N7002,215` qualification is preserved as useful technical history and a reference envelope, but it is not the mandatory/current Primary and does not by itself require replacement of C7420321. This remains a topology/application acceptance, not a declaration that every old resistor value or protection detail is automatically valid for the new board.

CM35 topology qualification is **PASS** for Stage 2:

- Input：pull/sink signal to `24G` is active；official material describes anti-interference filtering and requires at least about 2 ms signal duration.
- Output：official external wiring places the load between `+24 V` and OUT, supporting low-side / sinking behavior. No more specific internal transistor topology is claimed.
- Power domains：`V/G` is the isolated I/O 24 V supply and `24V/0V` is controller system power；the official recommendation is isolated, non-common-ground sources. Exact Project connection is a Stage-3 design input.
- Exact ON/OFF threshold、input current/impedance、maximum sink current、ON-state voltage、leakage and resistor/RC/protection values remain unknown. They do not block the Stage-2 topology decision.

Sensor qualification is **CONDITIONAL** for Stage 2: the user-provided manual supports 10–30 V、NPN、NO+NC、wiring and ≤10 mA static current, so the 2N7002 direction and current class can close. Manufacturer provenance and exact frontend values remain a Stage-3 evidence gate.

## Primary / Alternate Decisions

| Architecture-sensitive function | Primary | Alternate | Qualification / reassessment rule |
| --- | --- | --- | --- |
| 24 V → 3.3 V | LMR36510FADDAR, 65 V / 1 A | LMR36520FADDAR, 65 V / 2 A | Qualified electrical scaling Alternate；TI identifies DDA-8 pin compatibility. Use only if Stage-3 load/thermal results require it and recheck sourcing. |
| UART isolator | ISO7721DR | ISO6721BDR | Qualified cost-focused Alternate for 1-forward/1-reverse UART and default-HIGH behavior. ISO6721BDR is basic-isolation class；do not substitute if later requirements demand the ISO7721 reinforced-isolation capability. |
| Input overcurrent | 0468.500NRHF one-time 0.5 A / 63 V Slo-Blo fuse | 1210L035/60PR 60 V PPTC architecture | Alternate is temperature-conditional：0.35 A hold at 20°C falls to 0.21 A at 70°C；resistance/heating、residual current and sustained-fault behavior prevent Primary status. |
| 24 V / 3.3 V interface MOSFET | LCSC C7420321 2N7002, intentionally retained | Nexperia 2N7002,215 qualification history / reference envelope | Do not replace C7420321 solely because the earlier record named Nexperia Primary. Any actual purchase-time substitution must preserve the required voltage/current class, 3.3 V low-current application suitability, SOT-23 pin/footprint mapping, and temperature envelope. |

Purchase-time availability must be rechecked before ordering / PCBA submission；current stock observations are not permanent Project facts.

## Blocking / Deferred Boundary

Stage-2 closeout blockers：**None**.

Deferred to Stage 3:

- exact GPIO / USART allocation；MCU crystal/load capacitors、boot/reset values and ordinary decoupling；
- LMR36510 inductor、feedback divider、Cin/Cout、startup waveform、ripple、thermal and detailed loss calculations；
- exact CM35 / Sensor resistor、RC、ESD/transient/current-limiting networks and CM35 V/G reference/domain connection（closed in Stage 3 module records；Rev.A uses the isolated PSU-B I/O domain）；
- F1 final local-temperature/time-current verification and STPS2H100A exact forward-loss；
- LEDs、test points and ordinary peripherals。

Deferred to Stage 5 Layout Preflight:

- USB-C final mechanical acceptance；terminal exact series/MPN；
- PCB outline、mounting holes、enclosure and final wiring access。

Deferred to procurement:

- Primary/Alternate stock and price recheck immediately before purchasing / PCBA BOM submission。

Any new evidence that changes the 24 V architecture、fault-energy boundary、isolation requirement、interface voltage/current class or critical component qualification reopens Stage 2. Exact parameters listed above do not do so by themselves.

## Stage 2 Exit Review

- Critical architecture / safety / selection decisions：Closed for Stage 2.
- Bounding power budget：PASS.
- F1 Primary + Alternate architecture：Qualified with explicit Stage-3 verification rules.
- CM35 Stage-2 qualification：PASS.
- Sensor Stage-2 qualification：CONDITIONAL；not a closeout blocker.
- Primary / Alternate completeness：PASS with C7420321 intentionally retained and the Nexperia qualification preserved as reference history rather than a mandatory replacement rule.
- Stage 2 Closeout：**PASS**.

## Evidence Boundary

- Manufacturer official datasheet / product documentation is the technical qualification authority for critical devices.
- LCSC/JLC pages are procurement evidence for MPN, C-number, package and point-in-time availability; they do not replace manufacturer technical documentation.
- User multimeter observation is Measured Evidence for the present PSU operating point only; it does not establish long-term tolerance, ripple, surge or protection behavior.
- Legacy schematic is Legacy Design Reference / Existing Functional Evidence; topology reuse is explicitly authorized by the user, but the new Project `.SchDoc` will become EDA implementation authority only after Stage 3 capture.
- No ERC、DRC、EDA implementation、Manufacturing、Bring-up or Test PASS is claimed by this Stage 2 record.
