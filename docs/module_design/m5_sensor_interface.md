# M5 — Photoelectric Sensor Interface

## Module Status and Boundary

- Responsibility: power 4 × AN-LS18-40-N sensors and acquire each sensor's NPN NO and NC outputs, for 8 MCU inputs total.
- Per-channel frontend baseline: **DEFINED / ACCEPTABLE FOR REPLICATION**.
- EDA capture status: **IN PROGRESS**. Only the Sensor 1 NO reference channel has received current-session screenshot-level engineering review.
- M5 is not module `CLOSEOUT ACCEPTABLE`. That decision requires all eight channels to be captured and a screenshot-level completeness review of the replicated implementation.

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
- No additional galvanic isolation is added in M5 under the accepted Rev.A common-reference architecture.

The SMF30A is an ordinary Stage-3 support/protection component decision. Its verified selection does not reopen Stage 2 because it does not change the architecture, safety boundary, or interface voltage class.

## Replication and Evidence Boundary

- Replicate the reviewed Sensor 1 NO channel unchanged for SENSOR1_NC and all six Sensor 2–4 NO/NC channels, preserving `3V3`, `24V_PROTECTED`, TVS polarity, resistor placement, and GPIO mapping.
- After all eight channels are captured, perform a screenshot-level completeness review before considering M5 module `CLOSEOUT ACCEPTABLE`.
- The current screenshot supports only the visible Sensor 1 NO reference channel. This record does not claim `.SchDoc` parsing, complete capture, reference-designator verification, footprint verification, ERC PASS, Stage 4 PASS, PCB Layout approval, EMC/surge compliance, or hardware-test results.
