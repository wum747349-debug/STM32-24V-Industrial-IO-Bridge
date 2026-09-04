# PCB Review

Document Status: **STAGE 5 PLACEMENT PASS / CLOSED — STAGE 6 ROUTING/COPPER IMPLEMENTATION REVIEWED — PCB FINALIZATION PENDING**

Project Stage: **Stage 6 — Routing and Copper**

## Evidence Boundary

This record is based on the user-provided Altium Designer PCB screenshots, exported Design Rule Verification reports and the confirmed repository schematic/design baseline. The current `.PcbDoc` remains the PCB implementation authority.

The evidence is sufficient to record the routing/copper decisions, current DRC disposition, completed PCB-side Solder/Paste mask normalization review, and the current conclusion that no ordinary routing/copper blocker remains identified. It does **not** claim Gerber/manufacturing release, assembly fit, hardware test, EMC/surge compliance, or a formal zero-violation DRC PASS. Additional planned PCB edits — 3V3/GND test points and critical silkscreen labeling — still require a final repour and Final DRC afterward.

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
- The Stage 6 schematic corrective review fixed the CH340C UART-side mapping to `TXD -> CH340_TX` and `RXD <- CH340_RX`; PCB connectivity was updated by the user while retaining the correct ISO7721 directions.

Final manufacturing-data review must still verify there is no accidental domain bridge through polygon repour, via, track, shield, mounting feature, or other copper object.

### SWD / Debug Routing

The SWD / debug interface routing is complete at screenshot level.

- SWDIO, SWCLK and MCU_NRST use necessary Bottom routing because of the local top-layer crossing topology.
- The MCU_NRST Bottom trace passes beneath the projection of MCU pin 39; this is acceptable because pin 39 is a Top SMD pad while the NRST segment is on Bottom.
- Earlier true local Track/Via clearance findings in the MCU/debug area were removed during the 2026-09-04 DRC cleanup iteration.
- No requirement exists for SWDIO / SWCLK length matching or differential-pair treatment.

### Buck Power Ground / Current Loops

The lower-left LMR36510 power area was refined during Stage 6:

- U2 exposed-pad / GND thermal-via implementation is retained.
- C11/C12 input-capacitor GND is implemented as a compact local Top GND copper area with multiple GND vias rather than long individual GND traces.
- The intended current-loop requirement remains: C11/C12 return, U2 VIN/PGND and the switching loop must remain compact.
- C14/C15/C16 output-capacitor GND uses a broad local GND connection with multiple vias to the Bottom GND plane.
- `SW_NODE` remains local and must not be enlarged by later copper edits.
- R37/R42 feedback routing remains a small-signal path and must remain away from the switching node.
- `GND_IN_RAW` must still pass through Q25 before becoming PCB `GND`; latest DRC shows 0 violations for the dedicated 20 mil `GND_IN_RAW` ↔ `GND` clearance rule.
- The Stage 6 schematic corrective review fixed U2 `EN -> 24V_PROTECTED` and unused `PG -> GND`; PCB connectivity was updated by the user before the final DRC iterations.

### HSE Crystal Area

The STM32 HSE area received dedicated routing / ground treatment during Stage 6:

- X1 was moved slightly left/down to improve local routing space while remaining close to the MCU.
- OSC routing remains short, local, Top-layer and without intentional signal vias.
- X1 case/GND pads and C2/C4 GND pads use local GND vias.
- A **10 mil Top GND guard track** surrounds the local X1/C2/C4 oscillator area.
- Guard / local oscillator GND vias connect the guard and crystal-ground points into the Bottom GND structure.
- A Top Polygon Pour Cutout excludes the local oscillator area from broad Top GND fill so the guard structure remains explicit.
- Bottom copper under / around the oscillator is treated as a local GND return/shield region; unrelated Bottom signals, 3V3 trunks, SWD/UART/GPIO crossovers, or other noisy nets should not traverse the protected crystal area.
- The latest DRC still reports **6 Net Antennae** findings in this region. User-provided object-level screenshot evidence confirms that these are the intentional GND guard tracks and GND stitching vias, not dead signal stubs or unassigned copper. Preserve them; treat them as accepted intentional findings / targeted waiver candidates.

No further placement change is currently recommended for X1/C2/C4.

### Whole-Board GND Status

Machine-side GND-via stitching is substantially complete. USB-domain stitching has also been added while preserving the ISO7721 boundary.

Current screenshot-level review and the latest DRC iterations have not identified a reason to reopen ordinary routing. Final manufacturing-data review must still inspect polygon repour and return paths for:

- disconnected / orphan copper islands;
- narrow GND necks created by Bottom 3V3 trunks or signal crossovers;
- unintended `USB_GND` ↔ `GND` bridging;
- unintended `GND_IN_RAW` ↔ `GND` bypass around Q25;
- broken return paths below important signal corridors;
- excessive copper removal around the MCU, SWD/UART paths, HSE region or power stage;
- isolated vias or GND pads not actually connected after repour.

## PCB Solder / Paste Mask Review — 2026-09-04

A systematic imported-footprint mask-property issue was identified during final PCB review. Several pads originating from the JLCPCB / EasyEDA-to-Altium flow carried fixed/manual Solder or Paste shapes instead of following the project rules.

### Solder Mask normalization

- Ordinary solderable pads were restored to `Solder -> Rule Expansion` where imported fixed shapes were inappropriate.
- The current board rule remains `Solder Mask Expansion = 2 mil`.
- User-provided Altium / 3D evidence showed the expected pad openings after normalization.

### Paste Mask normalization

The project Paste baseline is:

```text
SMD pads: Paste enabled
TH pads: Top Paste disabled / Bottom Paste disabled
Method: Absolute
Paste Mask Expansion: 0 mil
Ordinary SMD pad mode: Paste -> Rule Expansion
```

The imported defect presented as pad-level `Round` / fixed Paste geometry with `0 × 0 mil` dimensions. This is not equivalent to `Rule Expansion + 0 mil`; it can suppress the usable stencil aperture even while the board rule itself is correct.

PCB Filter / Properties evidence was used to select the ordinary SMT pad population and normalize the pad-level Paste mode to `Rule Expansion`, while special power / exposed-pad devices were reviewed separately rather than blindly grouped with ordinary SMD pads.

### Special-device review

- U2 `LMR36510FADDAR`: ordinary pads and the exposed-pad Paste state were checked separately; the current `.PcbDoc` has a valid Paste aperture rather than the imported zero-size manual shape.
- Q25 `DMT10H015LFG-13 / PowerDI3333-8`: the large Pad 9 was separately checked. Its PCB net is confirmed as `GND_IN_RAW`, consistent with the Q25 Drain connection, and a valid Paste aperture is present in the current board implementation.
- TYPE-C-31-M-12: SMD contacts receive Paste; plated shell / fixing holes remain outside the SMD Paste population and do not receive ordinary Paste openings.
- SW1 `TS-1088-AR02016`: ordinary SMT pads are included in the Rule Expansion normalization.

### Top Paste visual evidence

User-provided Altium `Top Paste (Single)` full-board evidence confirms that ordinary SMD resistors, capacitors, diodes, MOSFETs, MCU / IC leads, USB-domain SMD contacts and the reviewed special devices now have visible Paste apertures, while mounting holes and ordinary THT connector pads are not populated with unintended Paste openings.

Current disposition:

```text
Current .PcbDoc Solder/Paste mask normalization: PASS / CLOSED
Top Paste single-layer visual review: PASS
Systematic Round 0 x 0 mil Paste defect in current .PcbDoc: RESOLVED
Q25 Pad 9 Drain net mapping: PASS — GND_IN_RAW
Final GTP / GBP or equivalent manufacturing Paste output: PENDING
Source PCB1.PcbLib root-cause cleanup: PENDING unless separately confirmed
```

The manufacturing release is therefore **not** being claimed by this mask closeout. Final generated Paste / Gerber output remains a Stage 7 manufacturing-data evidence item. The source footprint library should also be normalized separately so a later library update or footprint replacement does not reintroduce the imported fixed mask properties.

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
Net Antennae Tolerance:       0 mil
Paste Mask Expansion:         0 mil Absolute; ordinary SMD -> Rule Expansion; TH Paste disabled
```

Silk-to-Solder-Mask and Silk-to-Silk are no longer treated as blocking Batch-DRC noise during the current electrical/copper closeout; critical silkscreen content is instead handled in the dedicated finalization pass before manufacturing output.

The detailed rule baseline is owned by `docs/pcb_design_rules.md`.

## Latest DRC Review — 2026-09-04 18:30

Latest exported Altium Design Rule Verification Report:

```text
Warnings:        0
Rule Violations: 76
```

Critical electrical / connectivity / routing rules are currently clean:

```text
GND_IN_RAW <-> GND 20 mil:        0
Short-Circuit:                    0
Un-Routed Net:                    0
Modified Polygon:                 0
Default Width:                    0
SW_NODE Width:                    0
NC_POWER Width:                   0
Hole Size:                        0
Hole-to-Hole:                     0
Height:                           0
```

The ordinary 6 mil Clearance rule reports 4 findings, but all four are the known M3 mounting-hole pad versus its own centered Keepout Region collisions. Earlier true Track/Pad/Via clearance findings have been cleared.

### Remaining Findings / Disposition

**4 × Clearance — M3 NPTH versus own Keepout Region**

All four remaining clearance findings are `Pad Free-2` mounting-hole pads colliding with the intentionally centered solid Keepout Region around the same mounting hole. This is an intentional geometry / DRC-scope artifact. It does **not** indicate copper, routing or a foreign via has entered the keepout. Do not move the M3 hole out of its own keepout and do not delete the keepout merely to clear these findings. Use a targeted rule exception / waiver if a numeric zero-violation report is required.

**66 × Minimum Solder Mask Sliver**

The current mask-sliver rule remains the conservative 6 mil working threshold. The remaining findings are dominated by:

- U1 STM32 fine-pitch adjacent-pad mask-dam geometry around 0.128–0.129 mm;
- Q25 adjacent-pad geometry around 0.128–0.129 mm;
- USB-C fine-pitch contact geometry around 0.098–0.099 mm;
- a small number of Pad↔Via checks that were deliberately moved farther apart during the DRC cleanup, with the remaining examples no longer identified as routing/copper blockers.

Do **not** distort the U1, Q25 or USB-C copper footprint solely to force a 6 mil mask-sliver zero. These are manufacturing/mask interpretation findings, not evidence of an electrical short. The final Top Solder Mask / CAM interpretation remains a manufacturing-data review item.

**6 × Net Antennae — HSE GND guard**

Confirmed by the user with object-level PCB screenshot evidence as the intentional HSE GND guard track / local GND via structure. These are accepted intentional findings. The underlying guard and GND vias should remain.

### DRC Conclusion

**No currently reported violation is identified as an ordinary electrical routing/connectivity blocker.** The true Track/Pad/Via clearance findings discovered during the iterative DRC cleanup have been corrected. The raw Altium report still contains intentional/mechanical and manufacturing-mask findings, so this document does not label it a formal zero-violation `DRC PASS`.

Because the user still plans to add 3V3/GND test points and update critical silkscreen labels, this 18:30 report is a **pre-finalization routing/copper checkpoint**, not the final release DRC.

## Stage 6 Routing Decisions That Are Now Locked

Unless the later finalization edits expose a real defect, do not reopen the following merely for visual cleanup:

- 100 mm × 80 mm board / Stage 5 placement baseline;
- routing-driven GPIO assignments listed above;
- left `CN6 = IN11–IN18`, right `CN5 = OUT1–OUT8` topology;
- USB D+/D- and USB_VBUS routing;
- Top/Bottom USB_GND copper strategy with explicit ISO7721 Top/Bottom isolation cutout;
- IN11 short Bottom crossover while retaining `IN11 -> PA8`;
- SWDIO / SWCLK / NRST Bottom routing;
- Buck local GND/current-loop refinements;
- HSE local placement, GND guard, guard vias and polygon exclusion approach;
- current `.PcbDoc` ordinary-pad Solder / Paste `Rule Expansion` normalization unless later manufacturing evidence identifies a real defect.

## PCB Finalization — Next Activity

Ordinary routing / copper work can now stop. The next task is a bounded finalization pass:

1. Add an accessible `3V3` test point and a nearby `GND` test point; keep them outside connector/mechanical interference and preserve local copper clearances.
2. Add / clean critical Top Overlay labels for power, ground, connector function, Pin 1, polarity, SWD/debug, Sensors and IN/OUT identification.
3. Do not move electrically accepted components solely to clear non-critical silkscreen appearance.
4. Repour polygons after any test-point copper edits.
5. Rerun a complete Final DRC and verify that the test-point / overlay changes introduced no new Short, Un-Routed, copper Clearance, Width, Hole, domain-isolation or Net Antennae blocker.
6. Preserve/document the four M3 self-keepout findings and six confirmed HSE guard findings unless rule scoping is refined.
7. At manufacturing-output generation, inspect final Gerber / Drill / Top+Bottom Solder Mask / Top+Bottom Paste and confirm the mask normalization survived export.
8. Review the actual JLCPCB CAM / Gerber interpretation before manufacturing release.

Only after the finalization edit + Final DRC should Stage 6 closeout or transition toward manufacturing preparation be judged.

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

Stage 6 routing / copper review:
READY — NO CURRENT ORDINARY ELECTRICAL ROUTING BLOCKER IDENTIFIED

PCB-side Solder/Paste mask normalization:
PASS / CLOSED

Top Paste visual evidence:
PASS

Latest DRC:
EXECUTED — 2026-09-04 18:30
Warnings 0 / Rule Violations 76
4 intentional M3 self-keepout clearance findings
66 manufacturing/mask-sliver findings
6 intentional HSE GND-guard antennae findings

Formal zero-violation DRC PASS:
NOT CLAIMED

PCB finalization:
PENDING — 3V3/GND test points + critical silkscreen + repour + Final DRC

Final manufacturing Paste/Gerber/CAM review:
PENDING

Manufacturing release:
NOT YET APPROVED
```