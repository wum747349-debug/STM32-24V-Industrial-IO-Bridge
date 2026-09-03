# PCB Review

Document Status: **STAGE 5 PLACEMENT PASS / CLOSED — STAGE 6 ROUTING/COPPER IMPLEMENTATION COMPLETE AT SCREENSHOT LEVEL — FINAL PCB REVIEW PENDING**

Project Stage: **Stage 6 — Routing and Copper**

## Evidence Boundary

This record is based on the user-provided Altium Designer PCB screenshots and the confirmed repository schematic/design baseline. The current `.PcbDoc` remains the PCB implementation authority.

The evidence is sufficient to record the routing decisions and to begin the final PCB review, but it does **not** claim `.PcbDoc` object-level parsing, DRC PASS, Gerber/manufacturing release, assembly fit, hardware test, EMC/surge compliance, or final routed-copper PASS.

## Stage 5 Closed Mechanical Baseline

- Board outline: **100 mm × 80 mm**.
- Corner treatment: **R3 mm**.
- Mounting: **4 × M3 NPTH**, 3.20 mm drill, No Net.
- Mounting-hole copper/mechanical exclusion: approximately **Ø7.0 mm solid Keepout Region** around each mounting hole.
- The earlier 110 mm × 80 mm working outline was reduced to 100 mm × 80 mm before routing; no later routing evidence has required reopening the board outline or full-board placement.

## Stage 6 Routing / Copper Implementation Record

### Layer Use

Current two-layer routing strategy implemented during Stage 6:

```text
Top:
- primary GPIO / local signal routing
- local power routing
- critical local loops

Bottom:
- primary machine-side GND reference plane
- USB-domain USB_GND plane in the isolated USB area
- limited regional 3V3 trunks
- necessary short GPIO / debug crossovers
```

Bottom was not treated as a signal-routing layer indiscriminately; crossover use was accepted where it avoided large top-layer detours while preserving useful GND continuity.

### Final Routing-Driven GPIO Baseline

The current routing-driven MCU allocation is:

```text
CN6 / CM35 IN11–IN18
IN11 -> PA8
IN12 -> PA11
IN13 -> PA12
IN14 -> PA15
IN15 -> PB4
IN16 -> PB5
IN17 -> PB6
IN18 -> PB7

Right-side outputs / sensors
SENSOR2_NO -> PA0
SENSOR2_NC -> PA1
OUT1 -> PA2
OUT2 -> PA3
OUT3 -> PA4
OUT4 -> PA5
OUT5 -> PA6
OUT6 -> PA7
OUT7 -> PB10
OUT8 -> PB11
SENSOR1_NO -> PB8
SENSOR1_NC -> PB9
SENSOR3_NO -> PB12
SENSOR3_NC -> PB13
SENSOR4_NO -> PB14
SENSOR4_NC -> PB15
```

These assignments supersede earlier placement-era mappings where different GPIO choices were still being explored. They are now part of the PCB routing baseline and must not be casually reverted during final review.

### USB / UART / Isolation

The top-center functional sequence remains:

```text
USB-C
-> USB protection
-> CH340C
-> ISO7721
-> STM32
```

Current Stage 6 implementation decisions:

- USB D+/D- routing was completed and retained after local review; no unnecessary layer transitions or large reroute was introduced.
- USB_VBUS routing was completed locally around the USB-domain devices and bypass capacitors.
- `USB_GND != GND` remains mandatory.
- The USB domain uses a **Bottom USB_GND polygon** as its primary return plane; a full-area Top USB_GND polygon was intentionally not added.
- USB-domain GND pads use short local connections / vias into the Bottom USB_GND area.
- ISO7721 remains the galvanic isolation boundary between `USB_VBUS / USB_GND` and `3V3 / GND`.
- The ISO7721 isolation zone uses copper exclusion on both Top and Bottom; neither `USB_GND` nor machine `GND` may bridge this boundary.
- IN11 remains `PA8`. The local routing conflict near the isolation zone was solved with a short Bottom crossover outside the ISO7721 copper-exclusion region rather than reopening the GPIO allocation.

Final PCB review must still verify there is no accidental domain bridge through polygon repour, via, track, shield, mounting feature, or other copper object.

### SWD / Debug Routing

The SWD / debug interface routing is complete at screenshot level.

- SWDIO, SWCLK and MCU_NRST use necessary Bottom routing because of the local top-layer crossing topology.
- The MCU_NRST Bottom trace passes beneath the projection of MCU pin 39; this is acceptable because pin 39 is a Top SMD pad while the NRST segment is on Bottom.
- The actual NRST via / nearby SMD-pad clearance remains subject to final DRC.
- No requirement exists for SWDIO / SWCLK length matching or differential-pair treatment.

### Buck Power Ground / Current Loops

The lower-left LMR36510 power area was refined during Stage 6:

- U2 exposed-pad / GND thermal-via implementation is retained.
- C11/C12 input-capacitor GND is implemented as a compact local Top GND copper area with multiple GND vias rather than long individual GND traces.
- The intended current-loop requirement remains: C11/C12 return, U2 VIN/PGND and the switching loop must remain compact.
- C14/C15/C16 output-capacitor GND uses a broad local GND connection with multiple vias to the Bottom GND plane.
- `SW_NODE` remains local and must not be enlarged by later copper edits.
- R37/R42 feedback routing remains a small-signal path and must remain away from the switching node.
- `GND_IN_RAW` must still pass through Q25 before becoming PCB `GND`; final polygon review must prove no bypass was introduced.

### HSE Crystal Area

The STM32 HSE area received dedicated routing / ground treatment during Stage 6:

- X1 was moved slightly left/down to improve local routing space while remaining close to the MCU.
- OSC routing remains short, local, Top-layer and without intentional vias.
- X1 case/GND pads and C2/C4 GND pads use local GND vias.
- A **10 mil Top GND guard track** surrounds the local X1/C2/C4 oscillator area.
- Guard / local oscillator GND vias connect the guard and crystal-ground points into the Bottom GND structure.
- A Top Polygon Pour Cutout excludes the local oscillator area from later broad Top GND fill so the guard structure is not swallowed by a full-area polygon.
- Bottom copper under / around the oscillator is treated as a local GND return/shield region; final PCB review must confirm that unrelated Bottom signals, 3V3 trunks, SWD/UART/GPIO crossovers, or other noisy nets do not traverse the protected crystal area.

No further placement change is currently recommended for X1/C2/C4.

### Whole-Board GND Status

The user reports that the remaining machine-side GND points have now been provided with GND vias to the Bottom GND plane. This marks the transition from interactive routing to final PCB review.

This statement means **GND-via implementation is complete at user/screenshot level**; it does not yet mean final GND-plane quality is accepted. The final review must inspect polygon repour and return paths for:

- disconnected / orphan copper islands;
- narrow GND necks created by Bottom 3V3 trunks or signal crossovers;
- unintended `USB_GND` ↔ `GND` bridging;
- unintended `GND_IN_RAW` ↔ `GND` bypass around Q25;
- broken return paths below important signal corridors;
- excessive copper removal around the MCU, SWD/UART paths, HSE region or power stage;
- isolated vias or GND pads not actually connected after repour.

## Stage 6 Routing Decisions That Are Now Locked

Unless the final PCB review or DRC exposes a real defect, do not reopen the following merely for visual cleanup:

- 100 mm × 80 mm board / Stage 5 placement baseline;
- routing-driven GPIO assignments listed above;
- left `CN6 = IN11–IN18`, right `CN5 = OUT1–OUT8` topology;
- USB D+/D- and USB_VBUS routing;
- Bottom USB_GND polygon strategy with no broad Top USB_GND polygon;
- ISO7721 Top/Bottom copper isolation zone;
- IN11 short Bottom crossover while retaining `IN11 -> PA8`;
- SWDIO / SWCLK / NRST Bottom routing;
- Buck local GND/current-loop refinements;
- HSE local placement, guard routing and polygon exclusion approach.

## Final PCB Review Checklist — Next Activity

The next task is **not additional routine routing**. Perform a full Stage 6 PCB review using current Altium evidence, including at minimum:

1. Full-board unrouted-net / connection completeness check.
2. Full-board Top and Bottom routing review.
3. Bottom GND / USB_GND polygon continuity and island / neck review after final repour.
4. `USB_GND != GND` isolation verification around ISO7721.
5. `GND_IN_RAW != GND` / Q25 non-bypass verification.
6. Buck VIN/PGND/SW/BOOT/output/FB loop review.
7. HSE oscillator ground / return / no-crossing review.
8. MCU decoupling / VDDA / NRST / SWD local return review.
9. Board-edge, M3 keepout and connector/mechanical-clearance review.
10. Applicable Altium DRC execution and review of every remaining violation / waiver.

Only after this review and the required DRC evidence should Stage 6 be considered for closeout or transition toward manufacturing preparation.

## Minor / Later Mechanical Note

- `CN5` versus the bottom-right M3 screw/head/washer and removable-plug envelope should still be checked later with 3D / courtyard / real mechanical evidence when convenient.
- This is not presently a routing blocker from the available 2D screenshots.

## Conclusion

```text
Stage 5 — PCB Placement:
PASS / CLOSED

Board baseline:
100 × 80 mm, R3, 4 × M3 NPTH + keepouts

Stage 6 routing / GND-via implementation:
COMPLETE AT USER / SCREENSHOT LEVEL

Stage 6 final PCB review:
READY / PENDING

DRC:
NOT YET CLAIMED PASS

Manufacturing release:
NOT YET APPROVED
```
