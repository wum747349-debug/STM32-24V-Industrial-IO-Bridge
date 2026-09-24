# Hardware Bring-up Record and Recommended Test Plan

Project: STM32 24V Industrial I/O Bridge

Hardware Revision: TBD

Current Project Stage: see repository root `README.md`

## Document Boundary

This document deliberately separates two evidence classes:

- **Part A — Actual Bring-up Record** records only the hardware work confirmed by the user as already performed. It is not a reconstruction of a fully instrumented test session.
- **Part B — Recommended Bring-up & Hardware Test Plan** is a future test procedure. Its steps and expected behaviors are recommendations or design expectations, not completed tests or PASS evidence.

Creating this record does not mean that a new hardware test session occurred, does not create a formal system acceptance result, and does not execute a Project Stage transition.

# Part A — Actual Bring-up Record

## A1. Current Bring-up Status

- The physical PCB has completed actual hardware bring-up and practical debugging.
- Basic 24 V power-on, board 3.3 V checking, STM32 programming, host communication, and industrial I/O functional debugging were performed.
- A complete quantified test report has not been provided. There is no basis here for declaring every channel, power-integrity parameter, abnormal supply condition, EMC/surge requirement, isolation withstand requirement, or full system acceptance criterion PASS.
- This documentation update records an already completed activity; it does not claim that another round of hardware testing was performed during the update.

## A2. Actual Debug Sequence

The following sequence is limited to the user's confirmed account. No unconfirmed inspection, current-limit setting, waveform capture, or per-channel step has been inserted.

1. A programmable DC power supply was set to 24 V.
2. The supply was connected to the PCB 24 V input terminal.
3. A multimeter was used at the board 3.3 V and GND test points to check the 3.3 V supply.
4. After confirming the 3.3 V output, an ST-Link was connected and STM32 firmware was programmed.
5. The host computer was connected for serial communication and basic industrial I/O functional debugging.
6. Control commands were sent from the host computer, and a multimeter was used to check the corresponding motion-controller input-terminal voltage.
7. The observed basic Active-Low behavior was approximately 24 V for the inactive state and approximately 0 V for the active state.

## A3. Known Results and Evidence Boundary

| Item | Confirmed actual result | Evidence limitation |
| --- | --- | --- |
| Machine-side power | The board was powered from a 24 V DC supply. | Exact input voltage at the terminals, current limit, steady-state current, inrush, load, and temperature were not recorded. |
| 3.3 V rail | The board 3.3 V rail was checked before connecting ST-Link. | No exact voltage, tolerance, ripple, startup waveform, or load-step record was provided. |
| STM32 | Firmware was programmed through ST-Link. | Firmware identity, programming log, reset/BOOT matrix, and long-duration runtime evidence were not provided. |
| Host communication | Host serial communication and basic functional debugging were performed. | Enumeration details, baud rate, error-rate/duration data, power-sequence matrix, and isolation performance were not provided. |
| Industrial control | Host commands were exercised and corresponding motion-controller input-terminal voltages were checked. | The tested channel subset and a complete channel-by-channel result table were not provided. |
| Active-Low behavior | Approximately 24 V was observed as inactive and approximately 0 V as active. | These are approximate behavioral observations, not precision limits or a complete electrical characterization. |
| CM35 status inputs and sensors | No additional actual result is recorded here. | No complete CN5 OUT1–OUT8 or four-sensor NO/NC channel record was provided; these items are not marked PASS. |

No test date, operator, serial number, exact measurement value, instrument model, current, ripple, waveform, abnormal-power result, EMC/surge result, isolation-withstand result, or complete system PASS is inferred where none was supplied.

# Part B — Recommended Bring-up & Hardware Test Plan

## How to Use This Plan

Execute the following steps on a clearly identified PCB/PCBA and firmware version. Record actual values as they are measured. Values described as **design expectation** must not be converted to PASS criteria until they have been checked against the applicable device documentation, CM35 documentation, sensor documentation, firmware behavior, and system requirements. Stop immediately for an unexplained short, reversed polarity, unexpected current, voltage collapse, smoke, odor, sound, or rapid temperature rise.

Recommended sequence:

```text
Pre-power inspection
-> current-limited power validation
-> STM32 minimum system
-> isolated USB-UART
-> CM35 control outputs
-> CM35 status inputs
-> photoelectric sensors
-> integrated system test
```

## B1. Debug Preparation and Pre-power Checks

### Purpose and setup

Use good lighting, magnification, a DMM, the current schematic/PCB documents, and connector pinout records. Disconnect the 24 V source, USB cable, ST-Link, CM35, sensors, and other field wiring before resistance or continuity checks. Discharge the board before interpreting resistance readings.

### Inspection and measurement order

1. Record the PCB/PCBA identity, visible revision/marking, assembly state, and intended firmware.
2. Inspect both sides for missing or wrong parts, solder bridges, insufficient solder, tombstoned parts, contamination, damaged traces, foreign metal, and connector damage.
3. Check orientation/polarity for U1/U2/U3/U4, Q25, D9/D10/D12, other diodes/TVS devices, polarized parts, USB-C, SWD, CN1–CN6, and the 24 V input connector against the authoritative EDA and assembly information.
4. Verify the 24 V input terminal polarity before attaching leads.
5. With all power removed, check for unexplained low resistance or hard continuity at:
   - `3V3` to PCB `GND`;
   - `24V_PROTECTED` to PCB `GND`;
   - `24V_IN_RAW` to `GND_IN_RAW` at the input terminal;
   - `USB_GND` to PCB `GND`, which must not have an unintended direct connection.
6. Reverse the DMM leads and allow readings to settle where appropriate. MOSFET body-diode paths, TVS devices, semiconductor junctions, and charging capacitors can produce polarity-dependent or time-varying readings; continuity beeps alone are not a sufficient short-circuit diagnosis.

The negative-input protection boundary is:

```text
GND_IN_RAW -> Q25 -> PCB GND
```

`GND_IN_RAW` and PCB `GND` are not an ordinary hard-wired common before Q25. Do not bypass Q25 with a jumper, instrument lead, supply return, or field wiring. When diagnosing this path, compare the measured behavior with the Q25 MOSFET topology and board power state rather than requiring simple zero-ohm continuity.

Record the inspected locations, DMM mode, lead polarity, settled reading/behavior, and disposition. If a suspected short cannot be explained from the circuit, do not apply power; isolate the affected rail by schematic section and inspect components before retesting.

## B2. Current-limited Power-up and Staged Power Validation

The implemented positive-rail path is:

```text
24V_IN_RAW -> F1 -> D9 -> 24V_PROTECTED -> LMR36510 -> 3V3
```

The return path crosses Q25 as described in B1.

### Initial supply setup

- Initially disconnect USB, ST-Link, CM35, sensors, and controllable external loads unless a specific test requires them.
- Set the bench supply to 24.0 V with output disabled, verify lead polarity at the loose connector, then connect it to the PCB 24 V input.
- Choose the initial current limit from the expected unloaded board consumption plus margin. If no prior current baseline exists, **0.10 A is only a conservative engineering starting point for an unloaded-board trial, not an acceptance limit**. Increase in small recorded steps only after checking that CC operation is caused by benign startup charging rather than a fault and that no abnormal heating occurs.
- The fitted 0.5 A fuse is an overcurrent protection component with its own time-current behavior; it is not the bench-supply current-limit setting and does not define normal board current.

### Power-up observations and nodes

1. Enable the supply while watching input current and the CV/CC indication. A brief charging transient and steady-state current are different observations; record both when the instrument supports it.
2. If the supply remains in CC, the voltage collapses, current rises unexpectedly, or a component heats rapidly, disable the output immediately. Recheck polarity and narrow the fault in the order input/protection, `24V_PROTECTED`, then `3V3`.
3. Measure the input terminal between `24V_IN_RAW` and `GND_IN_RAW`.
4. Measure `24V_PROTECTED` relative to PCB `GND` at a positively identified, mechanically safe access point.
5. Measure the top-side `3V3` test pad relative to the adjacent PCB `GND` test pad.
6. Compare the rail progression with the design path and the relevant component data. Account for D9 and Q25 conduction losses; do not invent a voltage-drop limit from nominal labels alone.

If the F1 output/D9 anode, D9 cathode, or another internal node is not safely accessible, power down and identify a safe large pad/test fixture before measuring. Do not require live probing of dense U2, D9, Q25, or neighboring pads where a slipped tip can short 24 V into another net.

### Output quality, startup, and load testing

- **DC accuracy:** record `3V3` with the DMM at no external load and at each defined operating load. Establish the allowable range from STM32 and connected-device requirements plus the power design target.
- **Ripple/noise:** use an oscilloscope probe with a short ground spring at the 3V3/GND test points. Record probe ratio, coupling, bandwidth limit, time base, load, and peak-to-peak result. A long ground lead can create a misleading waveform.
- **Startup:** capture `24V_PROTECTED` and `3V3` during supply enable. Check monotonic behavior, rise time, overshoot/undershoot, and reset release against the relevant device requirements. No waveform criterion is declared PASS until a limit is documented.
- **Load:** increase only with a known electronic load or known system loads, while recording input current, rail voltage, ripple, and temperatures. Remain within the ratings of F1, D9, Q25, LMR36510, L1, connectors, and wiring. Stop for instability or abnormal heating.
- **Abnormal supply tests:** reverse polarity, brownout, hot-plug, overvoltage, surge, and repeated power cycling require a separately reviewed setup and limits. They are not implied by ordinary 24 V bring-up.

## B3. STM32 Minimum-system Verification

### Connection

1. Confirm stable `3V3` at the board test point and normal boot strapping (`BOOT0` LOW and `BOOT1`/PB2 at its default LOW) before attaching the debugger.
2. With the target supply off, connect ST-Link `VTREF`, `GND`, `SWDIO` (PA13), `SWCLK` (PA14), and `NRST`; then power the target in the intended order.
3. Treat SWD `VTREF` as the target-voltage reference. Do not use it as the default power source for the complete 24 V industrial board.

### Test and expected behavior

- Confirm the debugger detects the target at the observed `VTREF` voltage.
- Record device identity, programming tool/version, firmware build or checksum, programming/verify result, and reset method.
- Verify boot from main flash after debugger reset and after a controlled board power cycle.
- Exercise the manual reset path and confirm the intended firmware restarts.
- Check the normal BOOT condition and, only when needed, the documented service-boot condition; restore BOOT0 before ordinary operation.
- Before enabling field functions, confirm firmware GPIO initialization matches the routing-driven mapping below and preserves Active-Low semantics.
- During reset and early initialization, measure the CM35 control terminals as specified in B5; the design expectation is that the external outputs remain inactive.

Failure to connect should be localized through `3V3/VTREF`, target GND, SWDIO/SWCLK continuity, NRST behavior, BOOT state, and firmware/tool settings. Do not erase or change hardware merely to mask an unstable power or reset condition.

## B4. USB-UART and Isolation Communication

The isolation boundary is:

```text
USB side:    USB_VBUS / USB_GND -> CH340C -> ISO7721 side 1
Machine side: 3V3 / GND         -> STM32  -> ISO7721 side 2
```

`USB_GND` and PCB `GND` must remain separate unless a deliberately reviewed external system connection creates a common path.

### Basic test

1. Power only the USB side and confirm USB VBUS at an accessible USB-domain point relative to `USB_GND`.
2. Confirm CH340C enumeration in the host OS and record the device/port identity and driver state.
3. Power the machine side from the protected 24 V input and confirm ISO7721 side 2 has `3V3` relative to PCB `GND`.
4. Run a bidirectional UART test with known baud, framing, message pattern, duration, and error count. Record transmitted and received data rather than only noting that a port opened.

### Required power-sequence matrix

Repeat communication/recovery checks for:

- USB first, then industrial/machine power;
- industrial/machine power first, then USB;
- both sides powered;
- USB-side removal while the machine side remains powered;
- machine-side removal while USB remains powered;
- USB unplug/replug and restoration of both enumeration and UART communication.

For each case, observe whether the UART idle state remains inactive/HIGH, whether spurious commands occur, and whether recovery needs a reset or application restart.

A normal non-isolated ST-Link connects its computer-side ground to PCB `GND`. If the same computer or grounded instruments are also connected to the USB domain, external cable/shield/earth paths may bridge `USB_GND` and PCB `GND`, defeat the intended isolation, or carry unwanted current. Before isolation-related testing, disconnect ST-Link or use an appropriately isolated debug arrangement and verify the complete grounding topology.

Successful enumeration and UART data exchange prove basic communication only. They do not prove isolation withstand, creepage compliance, ESD/EMC performance, or surge immunity.

## B5. Industrial Control Outputs — CN6 / CM35 IN11–IN18

Use the locked routing-driven mapping:

| CN6 signal | STM32 GPIO | Commanded expectation |
| --- | --- | --- |
| IN11 | PA8 | GPIO LOW = control active; GPIO HIGH = inactive |
| IN12 | PA11 | GPIO LOW = control active; GPIO HIGH = inactive |
| IN13 | PA12 | GPIO LOW = control active; GPIO HIGH = inactive |
| IN14 | PA15 | GPIO LOW = control active; GPIO HIGH = inactive |
| IN15 | PB4 | GPIO LOW = control active; GPIO HIGH = inactive |
| IN16 | PB5 | GPIO LOW = control active; GPIO HIGH = inactive |
| IN17 | PB6 | GPIO LOW = control active; GPIO HIGH = inactive |
| IN18 | PB7 | GPIO LOW = control active; GPIO HIGH = inactive |

CN6 is the CM35 IN11–IN18 connector. For voltage checks, use CM35 `G/24G` (PSU B `-V`, the same I/O-domain reference as PCB `GND`) as the 24 V-side reference. Do not reference these terminals to CM35 system `0V`/PSU A `-V`, `USB_GND`, PE, or an arbitrary oscilloscope earth.

For each channel:

1. Start with the host command inactive and record the host state, MCU logical state, GPIO level if observable, and CN6/CM35 terminal voltage.
2. Command only that channel active and repeat the measurements.
3. Return it inactive before moving to the next channel.
4. Confirm the application label and physical terminal agree with the table.

The design expectation is a 24 V-side HIGH/inactive state for GPIO HIGH and a pulled-low/active state for GPIO LOW. The prior practical debug observed approximately 24 V inactive and approximately 0 V active, but exact acceptance bands must come from the CM35 input specification and measured system conditions.

Also record all eight terminal states during MCU reset, before GPIO initialization, after firmware reset, during machine-side brownout, and during controlled power-down. The hardware design target is that MCU high-impedance/reset leaves the 2N7002 off and the CM35 input inactive; this remains a test requirement, not an assumed measured PASS.

## B6. CM35 Status Inputs — CN5 / OUT1–OUT8

Use the locked routing-driven mapping:

| CN5 signal | STM32 GPIO | Physical/software expectation |
| --- | --- | --- |
| OUT1 | PA2 | CM35 active pulls MCU input LOW; software reports active |
| OUT2 | PA3 | CM35 active pulls MCU input LOW; software reports active |
| OUT3 | PA4 | CM35 active pulls MCU input LOW; software reports active |
| OUT4 | PA5 | CM35 active pulls MCU input LOW; software reports active |
| OUT5 | PA6 | CM35 active pulls MCU input LOW; software reports active |
| OUT6 | PA7 | CM35 active pulls MCU input LOW; software reports active |
| OUT7 | PB10 | CM35 active pulls MCU input LOW; software reports active |
| OUT8 | PB11 | CM35 active pulls MCU input LOW; software reports active |

CN5 is the CM35 OUT1–OUT8 connector. Exercise one known CM35 output at a time using the correct PSU-B I/O-domain common. For both inactive and active states, record the field-terminal voltage, MCU-side logic level when safely observable, raw firmware value, interpreted software state, and host display. The physical input is Active-Low; the application meaning should be positive (for example, `active = true`) only after firmware inversion.

Complete a channel-by-channel table for OUT1 through OUT8, then test any combinations required by the application. A correct principle or one working channel is not evidence that all eight channels pass.

## B7. Photoelectric Sensor NO/NC Inputs

CN1–CN4 are Sensors 1–4. Each connector supplies `24V_PROTECTED` and PCB `GND` and accepts one NPN NO signal and one NPN NC signal. The final mapping is:

| Sensor | NO GPIO | NC GPIO |
| --- | --- | --- |
| Sensor 1 / CN1 | PB8 | PB9 |
| Sensor 2 / CN2 | PA0 | PA1 |
| Sensor 3 / CN3 | PB12 | PB13 |
| Sensor 4 / CN4 | PB14 | PB15 |

For each sensor:

1. Verify brown/blue/black/white wiring against the connector pinout before power is applied.
2. Record `24V_PROTECTED` at the connector relative to PCB `GND` with the sensor connected.
3. Record NO and NC field voltages, MCU-side logic values, and host indications in the untriggered state.
4. Trigger the sensor using a repeatable target and record the same data.
5. Repeat several transitions and confirm the steady states are complementary after the switching interval.

The field outputs are NPN Active-Low. A sinking/asserted field output is expected to produce MCU LOW; a released output is expected to produce MCU HIGH. NO/NC can be briefly non-complementary while switching, so distinguish a short transition from persistent both-active, both-inactive, open-wire, swapped-wire, or stuck-channel behavior. The NO/NC principle is not a substitute for actual validation of all eight inputs.

## B8. System Integration

The project uses three relevant supply domains:

```text
PSU A system domain:
  PSU A +24 V / -V -> CM35 system 24V / 0V

PSU B isolated I/O domain:
  PSU B +24 V / -V -> CM35 V / G / 24G
  PSU B +24 V / -V -> PCB 24V_IN_RAW / GND_IN_RAW
  PCB 24V_PROTECTED / GND -> M4 pull-ups and CN1-CN4 sensors
  PCB 3V3 / GND -> STM32 and ISO7721 machine side

USB domain:
  Host USB -> USB_VBUS / USB_GND -> CH340C and ISO7721 USB side
```

PSU A `-V` must not be assumed equal to PSU B `-V`; the CM35 system side and isolated I/O side must follow the CM35 wiring documentation. CM35 `V/G/24G` is cabinet-powered from PSU B, not supplied through PCB F1. The USB domain is separately powered by the host.

After B1–B7 are individually satisfactory, integrate in this order:

1. Apply PSU A and PSU B according to the reviewed CM35/system wiring procedure; verify the intended domain references before connecting USB or instruments.
2. Confirm PCB power and MCU boot.
3. Establish USB-UART and confirm no unintended cross-domain ground path.
4. Exercise one CM35 control output, then all required controls.
5. Exercise one CM35 status output, then all required status inputs.
6. Connect and validate one sensor, then Sensors 1–4.
7. Run the host workflow while correlating commands, physical terminal voltages, CM35 states, sensor states, and host indications.

Keep **basic functional testing** separate from **extended validation**. Basic testing demonstrates intended commands and indications under nominal conditions. Extended validation covers all channels, repeated cycles, timing, long-duration operation, load extremes, supply sequencing/brownout, thermal behavior, cable effects, ESD/EMC, surge, and isolation withstand; each requires explicit conditions and limits.

## B9. Multimeter and Instrument Safety

- For voltage, place the red lead in the `V/Ω` jack and measure in parallel across the node and the correct domain reference.
- For current, use the correctly rated current jack/range and insert the meter in series. Confirm meter fuse/rating and expected current before energizing.
- For resistance or continuity, use the `V/Ω` jack with all sources removed and capacitors discharged.
- After any current measurement, return the lead to the `V/Ω` jack before the next voltage measurement.
- Never place a DMM configured for current directly in parallel across the 24 V supply or a powered rail.
- Select the reference for the domain being measured: `GND_IN_RAW` for the raw input pair, PCB `GND`/PSU B `-V`/CM35 `G/24G` for the machine I/O domain, `USB_GND` for the USB domain, and PSU A `-V`/CM35 `0V` only for the CM35 system domain.
- A conventional bench-oscilloscope ground clip is normally earth-referenced. Attaching it can short two nominally isolated domains or bypass Q25. Determine the complete grounding path before connection; use appropriate differential or isolated measurement equipment when needed.
- Use insulated probe tips, one-hand/controlled probing practices where appropriate, secure the return lead first, and power down before moving clips in dense areas.

## B10. Abnormal Debugging and Record Requirements

Use this closed-loop response for every anomaly:

```text
Abnormal symptom
-> stop at the defined safety condition and remove power
-> identify the smallest affected domain or signal path
-> inspect and measure with power removed first
-> make one controlled repair or configuration correction
-> repeat the affected pre-power and functional checks
-> record the evidence, result, remaining risk, and next action
```

Do not repeatedly increase the current limit, bypass F1/Q25/isolation, substitute grounds, or enable multiple channels to make a symptom disappear. After any solder repair or wiring change, repeat the relevant short check and staged power-up before returning to system testing.

Each actual test row should include at least:

| Field | Required record |
| --- | --- |
| Test item | Rail, interface, channel, sequence, or fault being checked |
| Test conditions | PCB/PCBA identity, firmware, connected loads, domain power state, environment |
| Instrument/power settings | Instrument identity if available, mode/range, 24 V setting, current limit, probe setup |
| Measurement point/reference | Exact node or terminal and the selected ground/reference domain |
| Expected result | Requirement, design expectation, source, and tolerance/limit if established |
| Actual result | Numeric value, waveform/log, state transition, or observation; leave untested items unfilled |
| Judgment | PASS / FAIL / NOT TESTED / LIMITED, with the decision basis |
| Anomaly/action | Symptom, stop condition, localization, repair/change, and retest result |

Suggested per-session header:

| Date/operator | PCB/PCBA/revision | Git/EDA/firmware identity | Supply and load configuration | Instruments | Session objective |
| --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |

Suggested result row:

| Test item | Conditions | Instrument/settings | Point/reference | Expected | Actual | Judgment | Anomaly/action |
| --- | --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  |  |

Do not prefill missing results. A future formal acceptance record belongs in `docs/test_report.md` only after test conditions, limits, measurements, and acceptance decisions are available.
