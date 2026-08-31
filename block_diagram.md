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
24 V machine supply                 │
        │                    ┌───────↕────────┐
        ▼                    │ M2 — STM32F103 │
┌───────────────────┐        │ minimum system │
│ M1 — F1 / STPS /  │        └───↕────────↕───┘
│ SMBJ30A / LMR36510│            │        │
│ Protection + 3V3 │            │        │
└──────┬────────────┘            │        │
       │ protected 24 V          │        │
       ├─────────────────────────┘        │
       │                                  │
       ▼                                  ▼
┌──────────────────────┐       ┌───────────────────────────┐
│ M5 — 4 × Sensor      │       │ M4 — CM35 Industrial I/O │
│ 4 × (NO + NC)        │       │ 8 × STM32 → IN11–IN18    │
│ = 8 sensor inputs    │       │ 8 × OUT1–OUT8 → STM32    │
└──────────↕───────────┘       └────────────↕──────────────┘
  4 × AN-LS18-40-N                         CM35 controller

M6 — Connectors / SWD / Indicators / Test Points spans power,
MCU, communication, CM35 and sensor service boundaries.
```

这是当前 board architecture boundary。M1 / M2 / M3 current-session module design and EDA capture closeout are acceptable；这不表示 Stage 3 complete、ERC PASS、Stage 4 review 或接口性能验证已完成。

## Modules

| Module | Responsibility | Inputs | Outputs | Power Domain | Open Risk |
| --- | --- | --- | --- | --- | --- |
| M1 | 0.5 A Slo-Blo F1、STPS2H100A、SMBJ30A-TR、protected 24 V bus 与 LMR36510FADDAR 3.3 V | Machine 24 V DC | Protected 24 V、machine-side 3.3 V | 24 V / low voltage | Current module closeout acceptable；startup/inrush、capacitor qualification、thermal、surge and layout verification remain |
| M2 | MCU、最小系统、safe startup、SWD/debug 边界 | Low-voltage power、USART1、CM35/sensor states | CM35 controls、UART status | Machine-side logic | Current module closeout acceptable；pin allocation frozen；M4 safe-state contract remains to implement |
| M3 | USB-C + USBLC6-2SC6 + CH340C ↔ ISO7721DR ↔ STM32 USART1 | PC USB、STM32 PA9/PA10 | Isolated UART TX/RX | `USB_VBUS/USB_GND` ↔ isolation barrier ↔ `3V3/GND` | Current module closeout acceptable；USB-C mechanics、actual enumeration/power sequencing、EMC/ESD and PCB isolation geometry remain |
| M4 | 8 路 CM35 control + 8 路 status；本板使用 IN11–IN18 / OUT1–OUT8 | STM32 controls、CM35 OUT1–OUT8 | CM35 IN11–IN18、STM32 status | CM35 V/G I/O domain / logic | active-low input、≥2 ms filter、sinking output topology 已确认；exact parameters 与 V/G domain connection 留待 Stage 3 |
| M5 | 4 个传感器供电、接线与 NO+NC 输入接收 | Protected 24 V、8 路 NO/NC field signals | 8 路 MCU sensor states | 24 V field / logic | 具体 frontend 待 qualification |
| M6 | 现场端子、SWD、指示与测试可达性 | 各模块 service signals | External wiring/debug access | Multiple | connector / indicators / mechanics 待定 |

## Cross-module Flows

- Energy flow（能量流）：机器 24 V → 0.5 A F1 → STPS2H100A → protected 24 V bus → SMBJ30A-TR、CM35/Sensor interface 与 4 个传感器；LMR36510FADDAR → machine-side `3V3` → MCU 与相关逻辑。M3 的 USB side 由 `USB_VBUS` 供电，machine side 由 `3V3` 供电，`USB_GND` 与 `GND` 不直接相连。CM35 的 V/G I/O supply domain 与 controller 24V/0V system supply 的具体关系必须在 Stage 3 明确。
- Signal flow（信号流）：C# ↔ USB-C ↔ USBLC6-2SC6 ↔ CH340C ↔ ISO7721DR isolation boundary ↔ STM32 USART1 PA9/PA10；STM32 PB0/PB1/PB5/PB6/PB7/PA8/PA11/PA12 → M4 → CM35 IN11–IN18；CM35 OUT1–OUT8 → M4 → STM32 PA0–PA7；4 × (NO+NC) → M5 → STM32 PB8–PB15。
- Control and feedback boundaries（控制与反馈边界）：协议层 `1=Active`；CM35 控制与回读的 STM32 物理 GPIO 均采用 Active-Low 语义，firmware 负责极性转换。控制输出在 reset/boot/not-ready 时必须 inactive。
