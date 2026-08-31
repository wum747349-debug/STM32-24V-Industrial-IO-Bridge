# M4 — CM35 Industrial I/O Interface

## Module Status and Boundary

- Responsibility: provide 8 STM32 → CM35 IN11–IN18 control channels and 8 CM35 OUT1–OUT8 → STM32 status channels.
- Current Stage-3 conclusion: **CLOSEOUT ACCEPTABLE** for module design and current-session EDA capture reviewed from user-provided Altium schematic screenshots.
- The Project remains in Stage 3. This record does not claim `.SchDoc` object parsing, footprint verification, ERC PASS, Stage 4 PASS, PCB Layout approval, or hardware-test results.

## Power-domain Decision

Rev.A uses a common-reference implementation. The CM35 controller, CM35 I/O domain, and STM32 board are supplied from the same `MS-120-24` 24 V / 5 A / 120 W supply. PCB `GND` and CM35 I/O `G / 24G` therefore share that supply's 0 V reference; `24V_PROTECTED` is the PCB rail after M1 fuse and reverse-polarity protection.

The CM35 official material recommends isolated, non-common-ground supplies for controller system power and I/O power. Rev.A intentionally accepts the simpler common-reference architecture and does not add 16-channel optocoupler or digital isolation. If stronger galvanic isolation becomes a requirement, first reassess the isolated 24 V power/domain architecture rather than automatically adding isolation independently to all 16 channels.

## Repeated Channel Topology

All 16 channels use Nexperia `2N7002,215`. Each channel follows the same level-translation structure:

```text
3V3 -> 10 kohm -> MCU-side node -> 2N7002 Source
3V3 ----------------------------> 2N7002 Gate
24V_PROTECTED -> 10 kohm -> CM35-side node -> 2N7002 Drain
```

No default RC filtering capacitor is fitted in M4. The present installation evidence does not justify adding per-channel RC filtering to the CM35 cabinet wiring.

### STM32 → CM35 controls

| CM35 input | STM32 GPIO | Physical behavior |
| --- | --- | --- |
| IN11 | PB0 | GPIO LOW = Active; GPIO HIGH = Inactive |
| IN12 | PB1 | GPIO LOW = Active; GPIO HIGH = Inactive |
| IN13 | PB5 | GPIO LOW = Active; GPIO HIGH = Inactive |
| IN14 | PB6 | GPIO LOW = Active; GPIO HIGH = Inactive |
| IN15 | PB7 | GPIO LOW = Active; GPIO HIGH = Inactive |
| IN16 | PA8 | GPIO LOW = Active; GPIO HIGH = Inactive |
| IN17 | PA11 | GPIO LOW = Active; GPIO HIGH = Inactive |
| IN18 | PA12 | GPIO LOW = Active; GPIO HIGH = Inactive |

Safe-startup contract:

```text
MCU reset / GPIO high-Z
  -> MCU-side 10 kohm pulls Source to 3V3
  -> Gate = Source ~= 3.3 V, so VGS ~= 0 V
  -> 2N7002 OFF
  -> 24 V-side 10 kohm keeps the CM35 input HIGH / inactive
```

This hardware default does not depend on firmware initialization timing.

### CM35 → STM32 status

| CM35 output | STM32 GPIO | Physical behavior |
| --- | --- | --- |
| OUT1 | PA0 | CM35 Active → MCU LOW; Inactive → MCU HIGH |
| OUT2 | PA1 | CM35 Active → MCU LOW; Inactive → MCU HIGH |
| OUT3 | PA2 | CM35 Active → MCU LOW; Inactive → MCU HIGH |
| OUT4 | PA3 | CM35 Active → MCU LOW; Inactive → MCU HIGH |
| OUT5 | PA4 | CM35 Active → MCU LOW; Inactive → MCU HIGH |
| OUT6 | PA5 | CM35 Active → MCU LOW; Inactive → MCU HIGH |
| OUT7 | PA6 | CM35 Active → MCU LOW; Inactive → MCU HIGH |
| OUT8 | PA7 | CM35 Active → MCU LOW; Inactive → MCU HIGH |

Firmware remains responsible for translating the physical Active-Low GPIO state to the positive application/protocol semantic.

## Field Connectors

- CM35 IN connector: Cixi Kefa Elec `KF2EDGR-3.81-8P` PCB header, LCSC/JLCPCB `C441188`, pins ordered IN11 through IN18.
- CM35 OUT connector: the same `KF2EDGR-3.81-8P` PCB header, pins ordered OUT1 through OUT8.
- Both headers use the matching removable 3.81 mm plug family. The exact removable-plug MPN remains a procurement/mechanical confirmation item.
- Exact reference designators remain governed by the current `.SchDoc`; this record does not infer them from screenshots or naming convention.

## Evidence and Remaining Validation

- Current-session Altium screenshots support the visible 16-channel topology, rail naming, mapping, and module-level closeout conclusion only.
- The user confirmed correction of prior `24V` labels to `24V_PROTECTED` and all low-voltage rail labels to `3V3`.
- The `.SchDoc` remains the EDA implementation authority. ERC, complete object/net connectivity, reference designators, footprints, connector mate fit, and hardware behavior remain unverified by this documentation sync.
