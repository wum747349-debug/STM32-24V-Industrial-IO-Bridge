# M5 — Photoelectric Sensor Interface

## Module Status and Boundary

- Responsibility: power 4 × AN-LS18-40-N sensors and acquire each sensor's NPN NO and NC outputs, for 8 MCU inputs total.
- Per-channel frontend baseline: **CAPTURED / REVIEWED ACROSS ALL 8 CHANNELS**.
- EDA capture status: **CLOSEOUT ACCEPTABLE**. Sensor 1–4 NO / NC have all been captured and passed the current-session screenshot-level completeness review.
- This conclusion is limited to the visible implementation evidence. It does not claim `.SchDoc` object parsing, reference-designator or footprint verification, ERC PASS, Stage 4 PASS, PCB Layout approval, EMC/surge compliance, or hardware-test results.

## Sensor Connectors and GPIO Mapping

Each sensor uses one Cixi Kefa Elec `KF2EDGR-3.81-4P` PCB header, LCSC/JLCPCB `C441184`, with identical field wiring:

| Pin | PCB net / function | Sensor wire |
| --- | --- | --- |
| 1 | `24V_PROTECTED` | Brown |
| 2 | `GND` | Blue |
| 3 | NO field signal | Black |
| 4 | NC field signal | White |

The matching removable 3.81 mm plug is required; its exact MPN remains a procurement/mechanical confirmation item. Exact connector reference designators remain governed by the current `.SchDoc`.

| Sensor signal | STM32 GPIO |
| --- | --- |
| SENSOR1_NO | PB8 |
| SENSOR1_NC | PB9 |
| SENSOR2_NO | PB10 |
| SENSOR2_NC | PB11 |
| SENSOR3_NO | PB12 |
| SENSOR3_NC | PB13 |
| SENSOR4_NO | PB14 |
| SENSOR4_NC | PB15 |

## Per-channel Frontend Baseline

Each NO or NC field signal uses one Nexperia `2N7002,215` and the following topology:

```text
FIELD signal -> 100 ohm -> 24 V-side node -> 2N7002 Drain
                           |
24V_PROTECTED -> 10 kohm --+

2N7002 Gate -> 3V3
2N7002 Source -> MCU-side signal -> STM32 GPIO
                                  |
                       3V3 -> 10 kohm

FIELD signal -> SMF30A cathode
GND          -> SMF30A anode
```

The TVS belongs on the connector side of the 100 Ω resistor and physically close to the field connector, with a short return to `GND`. NPN output asserted / sinking produces MCU GPIO LOW; output released produces MCU GPIO HIGH. Firmware converts this Active-Low physical state to positive application semantics.

NO and NC are acquired together to support complementary-state diagnostics. Firmware may use disagreement from the expected complementary relationship to detect wiring, sensor, or stuck-signal anomalies, but must allow for brief non-complementary states during switching and must not declare a fault immediately from a transient mismatch. No diagnostic coverage or functional-safety claim is made at this stage.

## Protection and Filtering Decision

- Series resistor: `100 Ω`, fitted baseline.
- TVS: Littelfuse `SMF30A`, unidirectional, SOD-123FL, LCSC `C720060`, fitted on every NO and NC field signal.
- Littelfuse official data: `VRWM = 30 V`; `VBR = 33.3–36.8 V @ 1 mA`; maximum `VC = 48.4 V @ 4.1 A` for a 10/1000 µs pulse; 200 W peak-pulse class.
- Suitability basis: 30 V stand-off is above the nominal 24 V signal, while the specified 48.4 V clamp point is below the 2N7002's 60 V `VDS` rating. This provides a useful schematic-level transient-protection margin for ESD, insertion, and occasional field-cable transients.
- Limitation: that comparison does not prove a system surge or EMC level. Actual source impedance, pulse shape, cable/trace inductance, TVS tolerance, placement, and MOSFET terminal overshoot remain later verification items.
- RC/filter capacitor: **NOT FITTED**, with no DNP capacitor footprint required in Rev.A. Current installation evidence does not show sustained noise that justifies hardware RC filtering; later waveform evidence may instead lead to software filtering or a measured hardware change.
- M5, the sensors, the PCB, and CM35 I/O all belong to the isolated PSU-B I/O domain. PSU B directly powers CM35 `V/G` and feeds the PCB `24V/GND` input; the sensors receive `24V_PROTECTED/GND` through the PCB branch. No per-channel galvanic isolation or PCB isolated DC/DC is added.

The SMF30A is an ordinary Stage-3 support/protection component decision. Its verified selection does not reopen Stage 2 because it does not change the architecture, safety boundary, or interface voltage class.

## Closeout and Evidence Boundary

- Current-session screenshots show all four `KF2EDGR-3.81-4P` sensor connectors and all eight NO/NC frontends, including 8 × 100 Ω series resistors, 8 × field-side SMF30A TVS devices, 8 × 2N7002, 24 V-side 10 kΩ pull-ups, `3V3` gates, MCU-side 10 kΩ pull-ups, and the SENSOR1–SENSOR4 NO/NC GPIO mapping.
- The TVS remains on the connector side of each 100 Ω resistor. The repeated implementation preserves `3V3`, `24V_PROTECTED`, TVS polarity, resistor placement, and GPIO mapping.
- Screenshot review does not equal `.SchDoc` object parsing. Complete object/net connectivity, exact reference designators, footprints, ERC, EMC/surge performance, and measured hardware behavior remain outside this closeout evidence.
