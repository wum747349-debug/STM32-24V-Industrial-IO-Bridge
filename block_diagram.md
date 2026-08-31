# Block Diagram

本文件描述模块、能量流、信号流和系统边界；它不证明器件已选择或 EDA 已实现。

## System Boundary

```text
                         PC / C# upper computer
                                  ↕ USB
                    ┌───────────────────────────────┐
                    │ M3 — USBLC6 + CH340C          │
                    │ USB_VBUS / USB_GND domain     │
                    └───────────────↕ UART──────────┘
                         ║ galvanic isolation ║
                         ║   boundary (UART)  ║
                    ┌───────────────↕───────────────┐
                    │ ISO7721 isolated UART         │
                    │ USB_GND ≠ machine GND         │
                    └───────────────↕───────────────┘
                                    │
PSU B isolated I/O supply          │
  +24 V / -V                ┌───────↕────────┐
        │                   │ M2 — STM32F103 │
        ▼                   │ minimum system │
┌───────────────────┐       └───↕────────↕───┘
│ M1 — F1 / STPS /  │           │        │
│ SMBJ30A / LMR36510│           │        │
│ Protection + 3V3 │           │        │
└──────┬────────────┘           │        │
       │ 24V_PROTECTED / 3V3    │        │
       ├────────────────────────┘        │
       │                                 │
       ▼                                 ▼
┌──────────────────────┐       ┌───────────────────────────┐
│ M5 — 4 × Sensor      │       │ M4 — CM35 Industrial I/O │
│ 4 × (NO + NC)        │       │ 8 × STM32 → IN11–IN18    │
│ = 8 sensor inputs    │       │ 8 × OUT1–OUT8 → STM32    │
└──────────↕───────────┘       └────────────↕──────────────┘
  4 × AN-LS18-40-N                  CM35 I/O V/G domain

M6 — Connectors / SWD / Indicators / Test Points spans power,
MCU, communication, CM35 and sensor service boundaries.
```

这是当前 board architecture boundary。M1–M5 current-session module design and EDA capture closeout 均为 acceptable；Stage 3 结论为 `READY FOR SCHEMATIC REVIEW`，但这不表示 ERC PASS、Stage 4 PASS、PCB Layout approval 或接口性能验证已完成。

## External Cabinet Wiring and Isolation Boundaries

```text
PSU A (isolated output)                     CM35 system power
  +24 V ----------------------------------> 24V
  -V    ----------------------------------> 0V

                PSU A -V   X   PSU B -V
                     no direct connection

PSU B (independent isolated output)          CM35 I/O power
  +24 V ------------------+----------------> V
  -V    ------------------+----------------> G / 24G
                           |
                           +---------------> PCB 24V INPUT
                           +---------------> PCB GND

PCB branch:
  PCB 24V INPUT -> M1 -> F1 -> reverse-polarity protection
                 -> 24V_PROTECTED -> M4 pull-ups / M5 sensors
                 -> LMR36510 -> 3V3

Reference rules:
  PCB GND = CM35 G / 24G = PSU B -V
  PCB GND / CM35 G  X  CM35 0V / PSU A -V / PE / chassis
  USB_GND           X  PCB / I/O-domain GND
```

CM35 `V/G` is distributed directly from PSU B at cabinet terminals and does not pass through PCB F1 or `24V_PROTECTED`. This documentation diagram is the External Wiring authority for the current system architecture; a complex cabinet wiring drawing is not required in the schematic for Stage 3 closeout.

## Modules

| Module | Responsibility | Inputs | Outputs | Power Domain | Open Risk |
| --- | --- | --- | --- | --- | --- |
| M1 | 0.5 A Slo-Blo F1、STPS2H100A、SMBJ30A-TR、protected 24 V bus 与 LMR36510FADDAR 3.3 V | PSU-B PCB branch 24 V DC | Protected 24 V、I/O-domain 3.3 V | Isolated PSU-B I/O domain / low voltage | Current module closeout acceptable；startup/inrush、capacitor qualification、thermal、surge and layout verification remain |
| M2 | MCU、最小系统、safe startup、SWD/debug 边界 | Low-voltage power、USART1、CM35/sensor states | CM35 controls、UART status | I/O-domain logic | Current module closeout acceptable；pin allocation frozen；M4 safe-state contract closed |
| M3 | USB-C + USBLC6-2SC6 + CH340C ↔ ISO7721DR ↔ STM32 USART1 | PC USB、STM32 PA9/PA10 | Isolated UART TX/RX | `USB_VBUS/USB_GND` ↔ isolation barrier ↔ `3V3/GND` | Current module closeout acceptable；USB-C mechanics、actual enumeration/power sequencing、EMC/ESD and PCB isolation geometry remain |
| M4 | 8 路 CM35 control + 8 路 status；本板使用 IN11–IN18 / OUT1–OUT8 | STM32 controls、CM35 OUT1–OUT8 | CM35 IN11–IN18、STM32 status | Isolated PSU-B I/O domain / logic | 16-channel topology、mapping、safe startup 与 power-domain boundary closeout acceptable；exact CM35 electrical limits remain later review inputs |
| M5 | 4 个传感器供电、接线与 NO+NC 输入接收 | Protected 24 V、8 路 NO/NC field signals | 8 路 MCU sensor states | Isolated PSU-B I/O domain / logic | 全 8 路 screenshot-level completeness review complete；EMC/surge、footprints、ERC and measured behavior remain unverified |
| M6 | 现场端子、SWD、指示与测试可达性 | 各模块 service signals | External wiring/debug access | Multiple | connector / indicators / mechanics 待定 |

## Cross-module Flows

- Energy flow（能量流）：PSU A → CM35 system `24V/0V`；独立 PSU B 在机柜端直接分配至 CM35 I/O `V/G` 和 PCB `24V/GND`。PCB branch 为 PSU B +24 V → 0.5 A F1 → STPS2H100A → `24V_PROTECTED` → M4 pull-ups / sensors，并由 LMR36510FADDAR 产生 `3V3`。M3 USB side 由 `USB_VBUS` 供电，machine/I/O side 由 `3V3` 供电；`USB_GND != PCB/I/O-domain GND`。
- Signal flow（信号流）：C# ↔ USB-C ↔ USBLC6-2SC6 ↔ CH340C ↔ ISO7721DR isolation boundary ↔ STM32 USART1 PA9/PA10；STM32 PB0/PB1/PB5/PB6/PB7/PA8/PA11/PA12 → M4 → CM35 IN11–IN18；CM35 OUT1–OUT8 → M4 → STM32 PA0–PA7；4 × (NO+NC) → M5 → STM32 PB8–PB15。
- Control and feedback boundaries（控制与反馈边界）：协议层 `1=Active`；CM35 控制与回读的 STM32 物理 GPIO 均采用 Active-Low 语义，firmware 负责极性转换。控制输出在 reset/boot/not-ready 时必须 inactive。
