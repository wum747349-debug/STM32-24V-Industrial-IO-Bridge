# M2 — STM32F103C8T6 Minimum System

## Module Status and Boundary

- Responsibility: STM32F103C8T6 LQFP48 power, clock, reset, boot, SWD, USART1, board-level GPIO allocation, and startup interface contract.
- Stage 3 module conclusion remains **CLOSEOUT ACCEPTABLE**; Stage 4 Formal Schematic Review is **PASS / CLOSED** and PCB Layout entry is approved.
- Actual hardware bring-up has since included a 3.3 V check, ST-Link connection, STM32 firmware programming, and basic runtime/host communication. See [`docs/bringup_log.md`](../bringup_log.md). Firmware identity, programming log, reset/BOOT coverage, quantified timing, long-duration operation, EMC, and surge behavior were not provided and are not claimed PASS.

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

| Function          | STM32 pins                                                                                                                         |
| ----------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| CM35 status sense | OUT1→PA2, OUT2→PA3, OUT3→PA4, OUT4→PA5, OUT5→PA6, OUT6→PA7, OUT7→PB10, OUT8→PB11                                                   |
| Sensor inputs     | SENSOR1_NO→PB8, SENSOR1_NC→PB9, SENSOR2_NO→PA0, SENSOR2_NC→PA1, SENSOR3_NO→PB12, SENSOR3_NC→PB13, SENSOR4_NO→PB14, SENSOR4_NC→PB15 |
| CM35 controls     | IN11→PA8, IN12→PA11, IN13→PA12, IN14→PA15, IN15→PB4, IN16→PB5, IN17→PB6, IN18→PB7                                                |
| Debug             | PA13 SWDIO, PA14 SWCLK                                                                                                             |
| HSE               | PD0 OSC_IN, PD1 OSC_OUT                                                                                                            |
| Reserved / spare  | PB0/PB1 spare; PB2 BOOT1; PB3 spare/SWO; PC13 spare; PC14/PC15 spare with LSE unused                                               |

This table is the locked Stage 6 routing-driven GPIO baseline from `README.md` and `docs/pcb_review.md` and supersedes the earlier placement-era allocation. PA15/PB3/PB4 are SWJ/JTAG-related at reset; firmware must release the relevant JTAG resources before using PA15 and PB4 as ordinary GPIO while retaining the required SWD access.

## Cross-module Safe-startup Contract

M2 does not rely on MCU reset GPIO state alone to guarantee CM35 inactivity. M4 must implement:

```text
MCU GPIO high-Z -> 3.3 V-side pull-up -> 2N7002 OFF
-> 24 V side HIGH -> CM35 input inactive
```

This is the implemented cross-module design contract, not a claim that reset, initialization, brownout, and power-down behavior have all been measured on every output.

## Remaining Validation

- The current record is based on user-reported/reviewed EDA capture and engineering decisions; the `.SchDoc` was not parsed or modified by Codex.
- Final reset switch and SWD header mechanical selections remain open.
- Programming and basic operation have been performed, but complete reset/BOOT coverage, GPIO startup-state measurements, long-duration runtime, and a firmware-to-final-mapping audit remain to be recorded.
