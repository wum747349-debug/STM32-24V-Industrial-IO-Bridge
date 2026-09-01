# M2 — STM32F103C8T6 Minimum System

## Module Status and Boundary

- Responsibility: STM32F103C8T6 LQFP48 power, clock, reset, boot, SWD, USART1, board-level GPIO allocation, and startup interface contract.
- Stage 3 module conclusion remains **CLOSEOUT ACCEPTABLE**; Stage 4 Formal Schematic Review is **PASS / CLOSED** and PCB Layout entry is approved.
- This record does not claim `.SchDoc` parsing, broader full-board pin/footprint verification, ERC PASS, hardware-test PASS, or EMC/surge compliance.

## Power, Clock, Reset, and Boot

```text
VDD_1 / VDD_2 / VDD_3 -> 3V3; each VDD has 100 nF local decoupling to GND
3V3 -> 10 uF MCU rail bulk -> GND
3V3 -> R19 0 ohm -> VDDA
VDDA -> 100 nF + 1 uF local decoupling -> GND
VSS_1 / VSS_2 / VSS_3 / VSSA -> GND
3V3 -> VBAT; VBAT -> 100 nF -> GND

PD0 / OSC_IN <-> TKD SX32Y008000BC1T001 8 MHz SMD3225 CL=12 pF
crystal <-> R6 0 ohm <-> PD1 / OSC_OUT
each crystal side -> 15 pF C0G/NP0 -> GND

NRST -> 100 nF -> GND
NRST -> manual normally-open reset switch -> GND
NRST -> SWD NRST
BOOT0 -> 10 kohm -> GND; service jumper/header may pull BOOT0 to 3V3
PB2 / BOOT1 -> R28 10 kohm -> GND
```

- R19 is the fitted 0 Ω VDDA-link baseline and preserves later filtering flexibility; no ferrite bead is currently fitted.
- No separate RTC battery and no LSE are fitted. The reset network has no external NRST pull-up.
- R6 is fitted at 0 Ω and retained as the HSE crystal series/damping tuning provision.
- Normal boot is BOOT0 LOW + BOOT1 LOW/default -> Main Flash. Reset-switch and service-header mechanical MPNs are not frozen and do not block current module closeout.

## SWD and USART1

```text
PA13 -> SWDIO
PA14 -> SWCLK
SWD 1x5 -> VTREF / 3V3, SWDIO, SWCLK, GND, NRST
PA9  -> MCU_UART_TX -> later ISO7721DR / CH340C path
PA10 <- MCU_UART_RX <- later ISO7721DR / CH340C path
```

`VTREF / 3V3` is primarily a target-voltage reference. The interface is not documented as a default means for ST-Link to power the complete 24 V industrial board. Final header MPN/mechanics remain open.

## Board-level GPIO Allocation

| Function          | STM32 pins                                                                                                                           |
| ----------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| CM35 status sense | OUT1→PA0, OUT2→PA1, OUT3→PA2, OUT4→PA3, OUT5→PA4, OUT6→PA5, OUT7→PA6, OUT8→PA7                                                       |
| Sensor inputs     | SENSOR1_NO→PB8, SENSOR1_NC→PB9, SENSOR2_NO→PB10, SENSOR2_NC→PB11, SENSOR3_NO→PB12, SENSOR3_NC→PB13, SENSOR4_NO→PB14, SENSOR4_NC→PB15 |
| CM35 controls     | IN11→PB0, IN12→PB1, IN13→PB5, IN14→PB6, IN15→PB7, IN16→PA8, IN17→PA11, IN18→PA12                                                     |
| Debug             | PA13 SWDIO, PA14 SWCLK                                                                                                               |
| HSE               | PD0 OSC_IN, PD1 OSC_OUT                                                                                                              |
| Reserved / spare  | PB2 BOOT1; PA15 spare; PB3 spare/SWO; PB4 spare; PC13 spare; PC14/PC15 spare with LSE unused                                         |

PA0–PA7 map the eight CM35 status inputs to EXTI0–EXTI7, while PB8–PB15 map the eight sensor inputs to EXTI8–EXTI15. This keeps all 16 external-input EXTI line numbers conflict-free. PA15/PB3/PB4 are SWJ/JTAG-related at reset; using them as ordinary GPIO later requires firmware to release the relevant JTAG resources.

## Cross-module Safe-startup Contract

M2 does not rely on MCU reset GPIO state alone to guarantee CM35 inactivity. M4 must implement:

```text
MCU GPIO high-Z -> 3.3 V-side pull-up -> 2N7002 OFF
-> 24 V side HIGH -> CM35 input inactive
```

This is a cross-module contract, not a claim that the unfinished M4 exact network has been verified.

## Remaining Validation

- The current record is based on user-reported/reviewed EDA capture and engineering decisions; the `.SchDoc` was not parsed or modified by Codex.
- Final reset switch and SWD header mechanical selections remain open.
- ERC, complete pin mapping against exported schematic evidence, footprint mapping, and PCB layout remain unverified.
