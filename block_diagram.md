# Block Diagram

本文件描述模块、能量流、信号流和系统边界；它不证明器件已选择或 EDA 已实现。

## System Boundary

```text
                         PC / C# upper computer
                                  ↕ USB
                    ┌───────────────────────────────┐
                    │ M3 — Board-mounted USB-UART   │
                    │ PC-side USB power / ground    │
                    └───────────────↕ UART──────────┘
                         ║ galvanic isolation ║
                         ║   boundary (UART)  ║
                    ┌───────────────↕───────────────┐
                    │ Machine-side isolated UART    │
                    │ PC GND ≠ machine 24 V 0V      │
                    └───────────────↕───────────────┘
                                    │
24 V machine supply                 │
        │                    ┌───────↕────────┐
        ▼                    │ M2 — STM32F103 │
┌───────────────────┐        │ minimum system │
│ M1 — 24V Input /  │        └───↕────────↕───┘
│ Protection / LV   │            │        │
│ Power             │            │        │
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

这是 Stage 1 architecture boundary，不表示已经选择具体器件、完成原理图或验证接口性能。

## Modules

| Module | Responsibility | Inputs | Outputs | Power Domain | Open Risk |
| --- | --- | --- | --- | --- | --- |
| M1 | 24 V 输入保护、protected 24V bus 与低压供电边界 | Machine 24 V DC | Protected 24 V、machine-side low voltage | 24 V / low voltage | 保护与 DC/DC 架构待定 |
| M2 | MCU、最小系统、safe startup、SWD/debug 边界 | Low-voltage power、UART、CM35/sensor states | CM35 controls、UART status | Machine-side logic | pin allocation 与外围待定 |
| M3 | PC USB ↔ isolated UART ↔ STM32 UART | PC USB、machine-side UART TX/RX | Isolated UART TX/RX | PC USB / machine-side logic，galvanically isolated | USB connector、USB-UART 与 digital isolator 待 qualification |
| M4 | 8 路 CM35 control + 8 路 status；CM35 可用范围为 IN1–IN18 / OUT1–OUT8，本板不控制 IN1–IN10 | STM32 controls、CM35 OUT1–OUT8 | CM35 IN11–IN18、STM32 status | 24 V field / logic | 当期接口器件需重新 qualification |
| M5 | 4 个传感器供电、接线与 NO+NC 输入接收 | Protected 24 V、8 路 NO/NC field signals | 8 路 MCU sensor states | 24 V field / logic | 具体 frontend 待 qualification |
| M6 | 现场端子、SWD、指示与测试可达性 | 各模块 service signals | External wiring/debug access | Multiple | connector / indicators / mechanics 待定 |

## Cross-module Flows

- Energy flow（能量流）：机器 24 V → M1 → protected 24V bus → CM35/Sensor interface 与 4 个传感器；M1 → machine-side low voltage → MCU 与相关逻辑。PC side 与 machine side 在 UART 处 galvanically isolated，PC USB ground 不与 machine-side 24 V `0V` 直接相连，USB 不得反向供电机器侧。
- Signal flow（信号流）：C# ↔ USB ↔ board-mounted USB-UART ↔ galvanic isolation boundary ↔ STM32 UART；STM32 → M4 → CM35 IN11–IN18；CM35 OUT1–OUT8 → M4 → STM32；4 × (NO+NC) → M5 → 8 路 STM32 sensor inputs。
- Control and feedback boundaries（控制与反馈边界）：协议层 `1=Active`；CM35 控制与回读的 STM32 物理 GPIO 均采用 Active-Low 语义，firmware 负责极性转换。控制输出在 reset/boot/not-ready 时必须 inactive。
