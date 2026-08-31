# M3 — USB-C / CH340C / Isolated UART

## Module Status and Boundary

- Responsibility: provide the PC USB device interface, USB data-line ESD protection, USB-to-UART conversion, and galvanically isolated bidirectional UART connection to STM32 USART1.
- Current Stage-3 conclusion: **CLOSEOUT ACCEPTABLE** for module design and current-session EDA capture reviewed from the user-provided Altium schematic screenshot.
- This record does not claim `.SchDoc` parsing, footprint verification, ERC PASS, USB enumeration test, measured isolation performance, EMC/ESD compliance, Stage 3 completion, Stage 4 PASS, or PCB Layout approval.

## Power Domains and Structured Connection Facts

```text
USB domain: USB_VBUS / USB_GND
Machine domain: 3V3 / GND
Hard boundary: USB_GND != GND
```

### USB-C receptacle — TYPE-C-31-M-12

```text
A1/B12 + B1/A12 GND -> USB_GND
A4/B9 + B4/A9 VBUS -> USB_VBUS
A5 CC1 -> R39 5.1 kohm / 1% -> USB_GND
B5 CC2 -> R40 5.1 kohm / 1% -> USB_GND
A6 DP1 + B6 DP2 -> USB_DP_RAW
A7 DN1 + B7 DN2 -> USB_DM_RAW
A8 SBU1 -> NC
B8 SBU2 -> NC
EH / shield pins -> USB_GND (current baseline)
```

The current receptacle remains mechanically conditional until board-edge, enclosure, and cable-access constraints are frozen. No chassis/PE domain is currently defined, so the shield baseline is direct connection to `USB_GND`; an RC shield network is not part of the present design.

### USBLC6-2SC6

```text
pin 1 I/O1 -> USB_DP_RAW
pin 6 I/O1 -> USB_DP -> CH340C pin 5 D+
pin 3 I/O2 -> USB_DM_RAW
pin 4 I/O2 -> USB_DM -> CH340C pin 6 D-
pin 2 GND -> USB_GND
pin 5 VBUS -> USB_VBUS
C18 100 nF X7R: USB_VBUS <-> USB_GND
```

### CH340C

```text
pin 1 GND -> USB_GND
pin 16 VCC -> USB_VBUS
C19 100 nF X7R: USB_VBUS <-> USB_GND
pin 4 V3 -> C20 100 nF X7R -> USB_GND
pin 5 D+ -> USB_DP
pin 6 D- -> USB_DM
pin 2 TXD -> CH340_TX
pin 3 RXD <- CH340_RX
pin 7 NC -> NC
pin 8 OUT# -> NC
pins 9-14 modem/status signals -> NC
pin 15 R232 -> NC
```

CH340C uses its internal clock; no external crystal is fitted. The present baseline does not add external USB D+/D- series resistors or UART pull resistors.

### ISO7721DR

```text
USB side:
pin 1 VCC1 -> USB_VBUS
pin 4 GND1 -> USB_GND
C21 100 nF X7R: VCC1 <-> GND1

Machine side:
pin 8 VCC2 -> 3V3
pin 5 GND2 -> GND
C22 100 nF X7R: VCC2 <-> GND2

PC -> MCU direction:
CH340C TXD -> CH340_TX -> pin 3 INB
pin 6 OUTB -> MCU_UART_RX -> STM32 PA10

MCU -> PC direction:
STM32 PA9 -> MCU_UART_TX -> pin 7 INA
pin 2 OUTA -> CH340_RX -> CH340C RXD
```

The isolator is powered independently on both sides: `USB_VBUS / USB_GND` on side 1 and `3V3 / GND` on side 2. No isolated DC/DC is required solely for M3 because the two sides already have independent power sources.

## Startup, Idle, and Power-off Behavior

- UART idle is HIGH. The selected non-F ISO7721 variant has a default-HIGH output behavior when the corresponding input side is unavailable, which is compatible with the UART idle requirement.
- With USB unplugged while machine-side `3V3` remains powered, the machine-side UART receive path is intended to remain at the inactive/HIGH state rather than create a false start bit.
- With machine-side power removed while USB remains present, the USB-side UART receive path is likewise intended to remain inactive/HIGH.
- Each active transmitter and its local ISO7721 supply side share the same local power domain in normal operation: CH340C with `USB_VBUS`, STM32 with `3V3`. This avoids the ordinary operating case of a powered UART transmitter directly driving an unpowered isolator input-side supply domain.
- These are schematic-level design conclusions; actual plug/unplug, brownout, enumeration, and powered/unpowered behavior remain to be verified on hardware.

## Engineering Basis and Layout-sensitive Constraints

- `USB_GND` and machine `GND` must remain electrically separate across the ISO7721 barrier. No wire, copper pour, test point, mounting feature, shield connection, or other net may unintentionally bridge them.
- Place USBLC6-2SC6 close to the USB-C receptacle and keep the ESD current return to `USB_GND` short. Route D+/D- through the protection device without long stubs.
- Keep CH340C VCC/V3 bypass capacitors close to their corresponding pins.
- Keep C21 and C22 close to the ISO7721 VCC/GND pin pairs on their respective sides.
- Preserve the isolator package creepage/clearance region in PCB implementation; the Project does not currently claim a specific reinforced-safety, mains-isolation, or system compliance rating.
- Direct shield-to-`USB_GND` termination is the present baseline. Revisit only if a chassis/PE domain is introduced or later EMC/ESD evidence justifies a different termination network.

## Remaining Validation

- USB-C receptacle mechanical/enclosure qualification remains open.
- Actual USB enumeration, sustained UART communication, unplug/replug behavior, and simultaneous/independent domain power sequencing are untested.
- ERC, complete pin/footprint mapping against exported schematic evidence, PCB isolation geometry, signal integrity, EMC/ESD, and system-level isolation compliance remain unverified.
