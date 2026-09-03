# PCB Review

Document Status: **STAGE 5 PLACEMENT PASS / CLOSED — STAGE 6 ROUTING/COPPER IMPLEMENTATION COMPLETE — DRC EXECUTED — FINAL PCB REVIEW PENDING**

Project Stage: **Stage 6 — Routing and Copper**

## Evidence Boundary

This record is based on the user-provided Altium Designer PCB screenshots, exported Design Rule Verification reports and the confirmed repository schematic/design baseline. The current `.PcbDoc` remains the PCB implementation authority.

The evidence is sufficient to record the routing/copper decisions and current DRC disposition, but it does **not** claim Gerber/manufacturing release, assembly fit, hardware test, EMC/surge compliance, or final routed-copper PASS. A formal DRC PASS is also not claimed while intentional/non-electrical findings remain in the report.

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
- broad machine-side GND copper where useful
- USB-domain Top USB_GND copper with isolation cutout

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
- The USB domain uses a **Bottom USB_GND polygon** as its primary reference plane.
- A **Top USB_GND polygon/copper area is also implemented** in the USB domain. This supersedes the earlier working note that a broad Top USB_GND polygon had not been added.
- USB-domain GND pads use short local copper / USB_GND vias between Top and Bottom USB-domain copper.
- ISO7721 remains the galvanic isolation boundary between `USB_VBUS / USB_GND` and `3V3 / GND`.
- The ISO7721 isolation zone now uses explicit copper exclusion / polygon cutout on both Top and Bottom. Neither `USB_GND` nor machine `GND` may bridge this boundary.
- No via is intentionally placed inside the isolation corridor; USB_GND vias stay on the USB side and machine GND vias stay on the machine side.
- IN11 remains `PA8`. The local routing conflict near the isolation zone was solved with a short Bottom crossover outside the ISO7721 copper-exclusion region rather than reopening the GPIO allocation.

Final PCB review must still verify there is no accidental domain bridge through polygon repour, via, track, shield, mounting feature, or other copper object.

### SWD / Debug Routing

The SWD / debug interface routing is complete at screenshot level.

- SWDIO, SWCLK and MCU_NRST use necessary Bottom routing because of the local top-layer crossing topology.
- The MCU_NRST Bottom trace passes beneath the projection of MCU pin 39; this is acceptable because pin 39 is a Top SMD pad while the NRST segment is on Bottom.
- The latest DRC no longer reports a clearance problem at this routing area.
- No requirement exists for SWDIO / SWCLK length matching or differential-pair treatment.

### Buck Power Ground / Current Loops

The lower-left LMR36510 power area was refined during Stage 6:

- U2 exposed-pad / GND thermal-via implementation is retained.
- C11/C12 input-capacitor GND is implemented as a compact local Top GND copper area with multiple GND vias rather than long individual GND traces.
- The intended current-loop requirement remains: C11/C12 return, U2 VIN/PGND and the switching loop must remain compact.
- C14/C15/C16 output-capacitor GND uses a broad local GND connection with multiple vias to the Bottom GND plane.
- `SW_NODE` remains local and must not be enlarged by later copper edits.
- R37/R42 feedback routing remains a small-signal path and must remain away from the switching node.
- `GND_IN_RAW` must still pass through Q25 before becoming PCB `GND`; latest DRC shows 0 violations for the dedicated 20 mil `GND_IN_RAW` ↔ `GND` clearance rule, but final copper review still confirms the functional non-bypass boundary.

### HSE Crystal Area

The STM32 HSE area received dedicated routing / ground treatment during Stage 6:

- X1 was moved slightly left/down to improve local routing space while remaining close to the MCU.
- OSC routing remains short, local, Top-layer and without intentional signal vias.
- X1 case/GND pads and C2/C4 GND pads use local GND vias.
- A **10 mil Top GND guard track** surrounds the local X1/C2/C4 oscillator area.
- Guard / local oscillator GND vias connect the guard and crystal-ground points into the Bottom GND structure.
- A Top Polygon Pour Cutout excludes the local oscillator area from broad Top GND fill so the guard structure remains explicit.
- Bottom copper under / around the oscillator is treated as a local GND return/shield region; unrelated Bottom signals, 3V3 trunks, SWD/UART/GPIO crossovers, or other noisy nets should not traverse the protected crystal area.
- The latest DRC reports **6 Net Antennae** findings in this region. User-provided object-level screenshot evidence confirms that these are the intentional GND guard tracks and GND stitching vias, not dead signal stubs or unassigned copper. Preserve them; treat them as accepted intentional findings / targeted waiver candidates.

No further placement change is currently recommended for X1/C2/C4.

### Whole-Board GND Status

Machine-side GND-via stitching is now substantially complete. USB-domain stitching has also been added while preserving the ISO7721 boundary.

Current screenshot-level review has not identified a reason to reopen ordinary routing. Final whole-board review must still inspect polygon repour and return paths for:

- disconnected / orphan copper islands;
- narrow GND necks created by Bottom 3V3 trunks or signal crossovers;
- unintended `USB_GND` ↔ `GND` bridging;
- unintended `GND_IN_RAW` ↔ `GND` bypass around Q25;
- broken return paths below important signal corridors;
- excessive copper removal around the MCU, SWD/UART paths, HSE region or power stage;
- isolated vias or GND pads not actually connected after repour.

## Active Altium DRC Baseline

The current Stage 6 DRC working baseline is the active configuration shown in the user-provided report:

```text
Default Clearance:            6 mil
GND_IN_RAW <-> GND:          20 mil
Default Width:                6 / 6 / 15 mil
SW_NODE Width:               16 / 20 / 24 mil
NC_POWER Width:               8 / 20 / 32 mil
Hole Size:                   10 ... 240 mil
Hole-to-Hole Clearance:       8 mil
Minimum Solder Mask Sliver:   6 mil
Silk-to-Solder-Mask:          6 mil
Silk-to-Silk:                 6 mil
Net Antennae Tolerance:       0 mil
```

The detailed rule baseline is owned by `docs/pcb_design_rules.md`.

## Latest DRC Review — 2026-09-03 20:33

Latest exported Altium Design Rule Verification Report:

```text
Warnings:        0
Rule Violations: 29
```

Critical electrical / connectivity rules are currently clean:

```text
Short-Circuit:                    0
Un-Routed Net:                    0
Modified Polygon:                 0
Default Width:                    0
SW_NODE Width:                    0
NC_POWER Width:                   0
GND_IN_RAW <-> GND 20 mil:        0
Hole Size:                        0
Hole-to-Hole:                     0
Minimum Solder Mask Sliver:       0
```

### Remaining Findings / Disposition

**4 × Clearance — M3 NPTH versus own Keepout Region**

All four remaining clearance findings are `Pad Free-2` mounting-hole pads colliding with the intentionally centered solid Keepout Region around the same mounting hole. This is an intentional geometry / DRC-scope artifact. It does **not** indicate copper, routing or a foreign via has entered the keepout. Do not move the M3 hole out of its own keepout and do not delete the keepout merely to clear these findings. Use a targeted rule exception / waiver if a numeric zero-violation report is required.

**2 × Silk-to-Solder-Mask — Q12**

Q12 Top Overlay geometry is 5.907 mil / 2.692 mil from the pad solder-mask opening against a 6 mil rule. This is non-electrical and easy to clean up; recommended before manufacturing output.

**17 × Silk-to-Silk**

These are reference-designator / footprint-overlay spacing findings. They affect silkscreen legibility/cleanup, not circuit connectivity. Do not move electrically accepted components solely to clear them; move or tidy overlay objects later if desired.

**6 × Net Antennae — HSE GND guard**

Confirmed by the user with object-level PCB screenshot evidence as the intentional HSE GND guard track / local GND via structure. These are accepted intentional findings. The underlying guard and GND vias should remain.

### DRC Conclusion

**No currently reported violation is identified as an electrical routing/connectivity blocker.** However, because the report still contains 29 intentional/non-electrical findings, this document does not label the raw Altium report as a formal zero-violation `DRC PASS`.

## Stage 6 Routing Decisions That Are Now Locked

Unless the final PCB review exposes a real defect, do not reopen the following merely for visual cleanup:

- 100 mm × 80 mm board / Stage 5 placement baseline;
- routing-driven GPIO assignments listed above;
- left `CN6 = IN11–IN18`, right `CN5 = OUT1–OUT8` topology;
- USB D+/D- and USB_VBUS routing;
- Top/Bottom USB_GND copper strategy with explicit ISO7721 Top/Bottom isolation cutout;
- IN11 short Bottom crossover while retaining `IN11 -> PA8`;
- SWDIO / SWCLK / NRST Bottom routing;
- Buck local GND/current-loop refinements;
- HSE local placement, GND guard, guard vias and polygon exclusion approach.

## Final PCB Review Checklist — Next Activity

The next task is **Stage 6 final whole-board PCB review / DRC disposition**, not additional routine routing. Check at minimum:

1. Full-board Top and Bottom routing topology.
2. Final Bottom GND / USB_GND polygon continuity and island / neck review after final repour.
3. `USB_GND != GND` isolation verification around ISO7721.
4. `GND_IN_RAW != GND` / Q25 non-bypass verification.
5. Buck VIN/PGND/SW/BOOT/output/FB loop review.
6. HSE oscillator ground / return / no-crossing review, preserving the accepted GND guard antennae findings.
7. MCU decoupling / VDDA / NRST / SWD local return review.
8. Board-edge, M3 keepout and connector/mechanical-clearance review.
9. Optional cleanup of Q12 silk-to-mask and remaining silk-to-silk findings.
10. Targeted waiver / exception disposition for the four M3 self-keepout collisions and six intentional HSE GND guard antennae if a clean DRC summary is desired.

Only after this final review should Stage 6 be considered for closeout or transition toward manufacturing preparation.

## Minor / Later Mechanical Note

- `CN5` versus the bottom-right M3 screw/head/washer and removable-plug envelope should still be checked later with 3D / courtyard / real mechanical evidence when convenient.
- This is not presently a routing blocker from the available 2D screenshots.

## Conclusion

```text
Stage 5 — PCB Placement:
PASS / CLOSED

Board baseline:
100 × 80 mm, R3, 4 × M3 NPTH + keepouts

Stage 6 routing / polygon / GND-via implementation:
COMPLETE AT USER / SCREENSHOT LEVEL

Latest DRC:
EXECUTED — 0 ELECTRICAL BLOCKERS IDENTIFIED
29 intentional / non-electrical findings remain

Formal zero-violation DRC PASS:
NOT CLAIMED

Stage 6 final PCB review:
READY / PENDING

Manufacturing release:
NOT YET APPROVED
```
