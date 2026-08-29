# Critical Component Selection Plan

本文件是 Stage 2 — Critical Component Selection 的 selection decision 主记录。关键器件先于普通外围器件确定；本文件不构成最终 BOM、EDA implementation 或 Stage completion 证明。

## Stage 2 Current State

- Selection activity：In progress
- Critical component candidates：Recorded
- Primary decisions：Recorded for current first-pass scope
- Deferred peripherals：Open
- EDA implementation：Not started
- Stage 2 complete：NO

## Confirmed Inputs

- 主控：STM32F103C8T6 直接集成到 PCB。
- 通信：board-mounted USB-UART，经 galvanically isolated UART interface 连接 machine-side STM32；PC USB ground 与 machine-side 24 V `0V` 不直接共地。
- CM35：使用 IN11–IN18 与 OUT1–OUT8，共 8 路 control + 8 路 status；physical interface 为 Active-Low contract。
- Sensor acquisition：4 个 AN-LS18-40-N 的 NO + NC 均采集，共 8 路 digital inputs。
- 制造目标：JLCPCB / LCSC 与 SMT / PCBA preferred。
- 24 V source：用户提供的电源图片显示 `MS-120-24`、24 V / 5 A / 120 W；用户已用万用表确认当前实际输出约 24 V 且观察较稳定。该测量只证明当前 operating point，不证明电源 tolerance、surge 或 protection performance。
- Legacy conversion：用户明确授权复用上一代 I/O 转换思路；已检查归档旧原理图，主要转换器件为 2N7002 MOSFET，而不是 optocoupler。新设计仍需在 Stage 3 对 exact connection、resistor values、safe state 与 external-interface protection 重新核对。

## Primary Candidate Table

Availability 为 2026-08-29 的 point-in-time procurement evidence；未取得明确库存数量时不推断库存状态。

| Module | Function | JLC C# | Manufacturer | MPN | Package | Availability | Key requirements / qualification basis | Datasheet verified | Decision | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| M2 | MCU | C8734 | STMicroelectronics | STM32F103C8T6 | LQFP-48 | Unknown | 2.0–3.6 V、72 MHz、37 I/O class、USART/SWD resources；Project requirement 指定 | Yes | Primary | Exact GPIO / clock / boot / reset / VDDA implementation 留待 Stage 3 |
| M3 | USB-UART | C84681 | WCH | CH340C | SOP-16 | Good | USB 2.0 Full-Speed to UART、3.3/5 V supply、built-in clock、2 Mbps class | Yes | Primary | -20~+70 °C；若后续环境温度要求超出范围需重新评估 |
| M3 | UART galvanic isolation | C366164 | Texas Instruments | ISO7721DR | SOIC-8 | Unknown | 2 channels, 1 forward + 1 reverse；2.25–5.5 V each side；default output HIGH；适合 UART TX/RX domain isolation | Yes | Primary | USB side 与 machine side 分别由各自电源域供电；不因此声称 system-level isolation certification |
| M3 | USB data ESD | C7519 | STMicroelectronics | USBLC6-2SC6 | SOT-23-6L | Unknown | 2-line USB 2.0 high-speed ESD protection；low line capacitance | Yes | Primary | Placement / routing / VBUS connection 留待 Stage 3/5 |
| M3 | USB-C receptacle | C165948 | Korean Hroparts Elec | TYPE-C-31-M-12 | SMD, right-angle, 16P | Unknown | USB 2.0 device connection；JLC/LCSC sourcing convenient | Supplier data | Conditional | Electrical use acceptable for current concept；mechanical/enclosure qualification remains OPEN-003 |
| M4/M5 | 24 V ↔ 3.3 V open-drain / pull-down conversion | C65189 | Nexperia | 2N7002,215 | SOT-23 | Unknown | 60 V N-MOSFET、logic-level drive、manufacturer lists logic-level translator use；matches verified legacy MOSFET approach | Yes | Primary | Legacy topology reuse authorized；exact per-channel interface/protection must be requalified with CM35/Sensor electrical data |
| M1 | 24 V → 3.3 V buck | C1858394 | Texas Instruments | LMR36510FADDAR | HSOIC/ESOP-8 | Good | 4.2–65 V input、1 A synchronous buck、400 kHz FPWM、70 V transient tolerance class、industrial-oriented protection features | Yes | Primary | Inductor、FB、input/output capacitors、thermal/load budget deferred to Stage 3 |
| M1 | Reverse-polarity protection | C81548 | STMicroelectronics | STPS2H100A | SMA (DO-214AC) | Unknown | 100 V / 2 A Schottky series diode；simple fail-safe reverse-polarity blocking for low-current 24 V control board | Yes | Primary | Forward drop / dissipation to be checked against final current budget |
| M1 | 24 V transient suppression | C133663 | STMicroelectronics | SMBJ30A-TR | SMB (DO-214AA) | Good | 30 V stand-off；600 W class 10/1000 µs TVS；selected above measured ~24 V steady source and below LMR36510 high-voltage boundary | Yes | Primary | ST table gives higher clamp under 8/20 µs high-current condition; Stage 3 must check source impedance, surge assumption and margin before claiming a compliance level |

## Primary Decisions

### M1 — 24 V Input / Protection / Low-voltage Power

Current architecture decision:

```text
24V input
  -> input overcurrent element (exact fuse/PTC rating deferred)
  -> STPS2H100A series reverse-polarity protection
  -> protected 24V bus
       -> SMBJ30A-TR to 0V for transient suppression
       -> Sensor / CM35 interface supply needs
       -> LMR36510FADDAR -> 3.3V machine-side rail
```

The external 24 V source has been measured by the user at approximately 24 V and observed stable. This supports the 30 V TVS stand-off choice for the current design assumption, but it is not a substitute for an official PSU tolerance/surge specification.

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

The new board will use Nexperia `2N7002,215` as the Primary device for the reused MOSFET conversion approach. This is a topology reuse decision, not a declaration that every old resistor value or protection detail is automatically valid for the new board.

## Alternate / Scalability Notes

- `LMR36520` family is a pin-compatible 65 V / 2 A scaling option if the final 3.3 V load budget materially exceeds the 1 A class; it is not currently required.
- `ISO6721` family may be evaluated as a cost-focused UART-isolator alternate if procurement or cost requires it; no alternate is promoted to equal Primary status without current datasheet/procurement qualification.
- 2N7002 has multiple supplier/order variants; exact alternates must preserve at least the required VDS margin, 3.3 V gate-drive behavior, package/pin mapping and current capability.
- Purchase-time availability must be rechecked before ordering / PCBA submission; current stock observations are not permanent Project facts.

## Open Issues / Deferred Peripherals

- [Datasheet] CM35 official I/O electrical specification remains missing. It blocks final per-channel threshold/current/protection qualification, not the current selection of 2N7002 as the reuse Primary.
- [Datasheet] AN-LS18-40-N archived manual gives 10–30 V, NPN NO+NC and wiring information, but manufacturer provenance remains unconfirmed; final input protection/filter values remain Stage 3 work.
- [Risk] SMBJ30A-TR + LMR36510 margin must be checked against the actual assumed surge waveform/source impedance before any IEC/system-level surge claim. No such compliance claim is made now.
- [Risk] Exact input overcurrent element and rating remain deferred until the final load/current budget is calculated; the 24 V / 5 A external PSU capability must not be used as the PCB fuse rating.
- [Deferred] LMR36510 inductor、feedback divider、input/output capacitors、bulk capacitor voltage rating and thermal/layout details.
- [Deferred] MCU crystal / load capacitors、normal decoupling、ordinary pull-up/down、LEDs、test points and other non-architecture peripherals.
- [Mechanical] USB-C connector and 5.0/5.08 mm terminal exact mechanical acceptance remain open until enclosure/board constraints are known.
- [Procurement] Primary and alternate availability must be rechecked immediately before purchasing / PCBA BOM submission.

## Evidence Boundary

- Manufacturer official datasheet / product documentation is the technical qualification authority for critical devices.
- LCSC/JLC pages are procurement evidence for MPN, C-number, package and point-in-time availability; they do not replace manufacturer technical documentation.
- User multimeter observation is Measured Evidence for the present PSU operating point only; it does not establish long-term tolerance, ripple, surge or protection behavior.
- Legacy schematic is Legacy Design Reference / Existing Functional Evidence; topology reuse is explicitly authorized by the user, but the new Project `.SchDoc` will become EDA implementation authority only after Stage 3 capture.
- No ERC、DRC、EDA implementation、Manufacturing、Bring-up or Test PASS is claimed by this Stage 2 record.
