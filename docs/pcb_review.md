# PCB Review

Document Status: **STAGE 5 PLACEMENT PASS / CLOSED — STAGE 6 ROUTING/COPPER REVIEWED — PCB FABRICATION RELEASED — JLCPCB MANUFACTURING ORDER RELEASED / AWAITING PRODUCTION**

Project Stage: **Stage 6 — Routing and Copper**

## Evidence Boundary

This record is based on user-provided Altium Designer PCB screenshots, exported Design Rule Verification reports, the confirmed repository schematic/design baseline, the final JLCPCB Gerber/CAM Viewer preview, the JLCPCB production-artwork comparison, and the user's final confirmation that the manufacturing order has been released. The current `.PcbDoc` remains the PCB implementation authority.

The available evidence is sufficient to record the routing/copper decisions, final DRC disposition, Solder/Paste normalization, test-point and Top Overlay finalization, PCB fabrication release, and the current operational manufacturing status. This record does **not** claim a formal zero-violation DRC PASS, an independent exhaustive SMT orientation/placement PASS beyond the reviewed manufacturing evidence, assembly fit, hardware test, EMC/surge compliance, or system validation PASS.

Current Project Stage remains Stage 6; this review does not itself execute a Stage transition.

## Stage 5 Closed Mechanical Baseline

- Board outline: **100 mm × 80 mm**.
- Corner treatment: **R3 mm**.
- Mounting: **4 × M3 NPTH**, 3.20 mm drill, No Net.
- Mounting-hole copper/mechanical exclusion: approximately **Ø7.0 mm solid Keepout Region** around each mounting hole.
- The earlier 110 mm × 80 mm working outline was reduced to 100 mm × 80 mm before routing; no later evidence required reopening the board outline or full-board placement.

## Stage 6 Routing / Copper Implementation Record

### Layer Use

Current two-layer routing strategy:

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

Bottom was not treated as a general-purpose signal layer indiscriminately; crossovers were accepted where they avoided large Top detours while preserving useful GND continuity.

### Final Routing-Driven GPIO Baseline

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

These assignments supersede earlier placement-era mappings and are part of the locked PCB routing baseline.

### USB / UART / Isolation

The top-center functional sequence remains:

```text
USB-C
-> USB protection
-> CH340C
-> ISO7721
-> STM32
```

Locked implementation decisions:

- USB D+/D- and USB_VBUS routing are complete and retained.
- `USB_GND != GND` remains mandatory.
- The USB domain uses Bottom `USB_GND` copper as its primary reference and also has Top `USB_GND` copper.
- ISO7721 remains the galvanic isolation boundary between `USB_VBUS / USB_GND` and `3V3 / GND`.
- Explicit copper exclusion / polygon cutout is present on both Top and Bottom through the isolation corridor.
- USB_GND vias remain on the USB side; machine GND vias remain on the machine side.
- No via is intentionally placed inside the isolation corridor.
- IN11 remains `PA8`; its local conflict was solved with a short Bottom crossover outside the isolation exclusion rather than reopening GPIO allocation.
- The Stage 6 schematic corrective review fixed CH340C mapping to `TXD -> CH340_TX` and `RXD <- CH340_RX`; PCB connectivity was updated while retaining ISO7721 directionality.

The final JLCPCB CAM preview did not show a new copper bridge across the intended USB isolation region.

### SWD / Debug Routing

- SWDIO, SWCLK and MCU_NRST use necessary Bottom routing because of local crossing topology.
- The MCU_NRST Bottom trace passes beneath the projection of MCU pin 39; this remains acceptable because pin 39 is a Top SMD pad while the NRST segment is on Bottom.
- Earlier true local Track/Via clearance findings around the MCU/debug area were cleared during the 2026-09-04 DRC cleanup.
- No SWDIO/SWCLK length matching or differential-pair treatment is required.

### Buck Power Ground / Current Loops

- U2 exposed-pad / GND thermal-via implementation is retained.
- C11/C12 input-capacitor GND uses compact local Top GND copper with multiple GND vias.
- C14/C15/C16 output-capacitor GND uses broad local GND with multiple vias to the Bottom plane.
- `SW_NODE` remains local.
- R37/R42 feedback routing remains away from the switching node.
- `GND_IN_RAW` must pass through Q25 before becoming PCB `GND`.
- The dedicated 20 mil `GND_IN_RAW` ↔ `GND` DRC rule is clean in the Final DRC.
- The Stage 6 schematic corrective review fixed U2 `EN -> 24V_PROTECTED` and unused `PG -> GND`; PCB connectivity was updated before final DRC.

The final JLCPCB CAM preview did not expose an obvious manufacturing-data bypass around the intended Q25 ground boundary.

### HSE Crystal Area

- X1/C2/C4 remain close to the MCU.
- OSC routing remains short, local, Top-layer and without intentional signal vias.
- X1 case/GND pads and C2/C4 GND pads use local GND vias.
- A **10 mil Top GND guard track** surrounds the local oscillator region.
- Guard/local oscillator GND vias connect to the Bottom GND structure.
- Top Polygon Pour Cutout excludes broad Top GND fill from the oscillator area so the guard remains explicit.
- Bottom copper below/around the oscillator remains a local GND return/shield region without unrelated noisy crossover routing.
- Final DRC still reports **6 Net Antennae** in this region; object-level screenshot evidence identified these as the intentional HSE GND guard tracks and GND stitching vias rather than dead signal stubs.

These six findings remain accepted intentional findings; the guard structure should not be removed solely to force a numeric zero-violation report.

## PCB Solder / Paste Mask Review — 2026-09-04

A systematic imported-footprint mask-property issue was identified during final PCB review. Several pads originating from the JLCPCB / EasyEDA-to-Altium flow carried fixed/manual Solder or Paste shapes instead of following project rules.

### Solder Mask normalization

- Ordinary solderable pads were restored to `Solder -> Rule Expansion` where imported fixed shapes were inappropriate.
- Current board rule: `Solder Mask Expansion = 2 mil`.
- Altium / 3D evidence showed expected pad openings after normalization.

### Paste Mask normalization

Project Paste baseline:

```text
SMD pads: Paste enabled
TH pads: Top Paste disabled / Bottom Paste disabled
Method: Absolute
Paste Mask Expansion: 0 mil
Ordinary SMD pad mode: Paste -> Rule Expansion
```

The imported defect appeared as pad-level fixed Paste geometry such as `Round 0 × 0 mil`. This is not equivalent to `Rule Expansion + 0 mil` and could suppress a usable stencil aperture. PCB Filter / Properties evidence was used to normalize the ordinary SMT population while special devices were reviewed separately.

### Special-device review

- U2 `LMR36510FADDAR`: ordinary pads and exposed-pad Paste state were checked separately; current implementation has valid Paste aperture geometry.
- Q25 `DMT10H015LFG-13 / PowerDI3333-8`: large Pad 9 was separately checked; its PCB net is `GND_IN_RAW`, consistent with the accepted Drain mapping, and a valid Paste aperture is present.
- TYPE-C-31-M-12: SMD contacts receive Paste; plated shell/fixing holes remain outside the ordinary SMD Paste population.
- SW1 `TS-1088-AR02016`: ordinary SMT pads are included in Rule Expansion normalization.

Current disposition:

```text
Current .PcbDoc Solder/Paste mask normalization: PASS / CLOSED
Top Paste single-layer visual review: PASS
Systematic Round 0 x 0 mil Paste defect in current .PcbDoc: RESOLVED
Q25 Pad 9 Drain net mapping: PASS — GND_IN_RAW
Source PCB1.PcbLib root-cause cleanup: PENDING unless separately confirmed
```

Source-library normalization remains a later maintainability task; it does not block the current released PCB fabrication data.

## PCB Finalization — Test Points and Top Overlay

The planned finalization pass has been completed.

### 3V3 / GND test points

Two accessible Top-side probe pads were added near the SWD/top-left machine-side area:

```text
3V3 test pad:
- Top copper only
- round, approximately 2.0 mm diameter
- no drill
- Top Paste disabled
- Top Solder uses Rule Expansion
- net = 3V3

GND test pad:
- same physical construction
- net = GND
```

The pads are intended for multimeter/scope probing rather than SMT assembly. Their function labels are present on Top Overlay. They must not be populated as ordinary SMT parts or receive stencil Paste.

### Critical Top Overlay

The final Top Overlay pass prioritizes field use and debug readability over retaining every dense repeated-channel RefDes. Critical functional marking includes, as applicable and where space permits:

- power input and polarity (`24V IN`, `+24V`, `24V-`);
- `3V3` / `GND` probe points;
- `SWD` and debug signal identification;
- `USB-UART`;
- `BOOT0` and `RESET`;
- `SENSOR1`–`SENSOR4` and available pin/function marking;
- left `CM35 IN` and right `CM35 OUT` identification;
- Pin-1 / polarity / orientation cues where needed.

Not every repeated Sensor pin has a full textual `NO` label because of local space constraints. This was accepted because the connector identity/orientation and available pin-function markings remain sufficient; no electrically accepted component was moved merely to make dense silkscreen cosmetic changes.

## Active Altium DRC Baseline

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

The detailed rule baseline is owned by `docs/pcb_design_rules.md`.

## Final DRC Review — 2026-09-04 21:42

Final exported Altium Design Rule Verification Report after test-point / Top Overlay finalization:

```text
Warnings:        0
Rule Violations: 76
```

Critical electrical / connectivity / routing rules:

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

The finalization edits introduced no new ordinary electrical/copper/hole blocker.

### Remaining Findings / Disposition

**4 × Clearance — M3 NPTH versus own Keepout Region**

All four remaining ordinary 6 mil Clearance findings are the known `Pad Free-2` mounting-hole pads colliding with their intentionally centered Keepout Regions. This is an intentional geometry / DRC-scope artifact, not evidence of foreign copper or routing entering the keepout.

**66 × Minimum Solder Mask Sliver**

The conservative 6 mil working rule continues to report fine-pitch mask-dam findings dominated by:

- U1 STM32 adjacent-pad mask geometry around 0.128–0.129 mm;
- Q25 adjacent-pad geometry around 0.128–0.129 mm;
- USB-C fine-pitch contact geometry around 0.098–0.099 mm;
- a small number of remaining Pad↔Via mask checks.

These are manufacturing/mask interpretation findings rather than evidence of an electrical short. U1/Q25/USB-C copper footprints are not to be distorted solely to force the 6 mil working rule to zero.

**6 × Net Antennae — HSE GND guard**

These remain the previously confirmed intentional HSE GND guard track / local GND via structure.

### Final DRC Conclusion

**No currently reported violation is identified as an ordinary electrical routing/connectivity blocker.** The raw report remains nonzero because of the documented intentional/mechanical and mask-manufacturing findings, therefore a formal numeric zero-violation `DRC PASS` is still **not claimed**.

## Gerber / JLCPCB CAM Review — 2026-09-04

Final Gerber manufacturing data was generated by the user and uploaded to the JLCPCB Gerber/CAM Viewer. The user provided the resulting full-board CAM preview for final review.

The available CAM evidence was checked for the following release-sensitive items:

- overall 100 mm × 80 mm board outline and rounded-corner interpretation;
- four M3 mounting holes;
- major Top/Bottom copper interpretation;
- absence of an obvious `USB_GND` ↔ machine `GND` bridge through the ISO7721 isolation corridor;
- absence of an obvious `GND_IN_RAW` bypass around Q25 in the manufacturing interpretation;
- presence and readability of critical Top Overlay labels;
- presence of the new `3V3` / `GND` probe pads;
- no obvious CAM-level board-outline or drill corruption.

No new fabrication blocker was identified from that CAM preview.

Evidence limitation: the supplied CAM screenshot is sufficient for the current bare-board release judgment but does not replace hardware inspection/test evidence.

## JLCPCB Manufacturing Release Confirmation — 2026-09-05

The user completed the final JLCPCB production-artwork confirmation and released the current order to manufacturing. The reviewed production artwork remained consistent with the accepted board geometry and did not expose a new PCB fabrication blocker.

Current order / assembly configuration recorded from the manufacturing workflow:

```text
PCB quantity:              5 pcs
PCBA quantity:             2 pcs
Assembly service:          Economic
Assembly side:             Top Side only
Coordinate mode:           Single Board
BOM groups total:          34
JLCPCB assembled groups:   29
DNP / hand-solder groups:  5
```

The five DNP groups correspond to nine THT parts that remain intentionally unassembled by JLCPCB and will be hand-soldered later:

- `BOOT0`
- `SWD`
- `CM35_IN / CM35_OUT`
- `SENSOR1~4`
- `24V_IN`

BOM matching was completed before release. Recorded matching corrections include:

- `X1 -> C20617233` — 8 MHz passive crystal
- `C11 -> C577211` — 2.2 µF / 100 V
- `C12 -> C513710` — 220 nF / 100 V
- `L1 -> C83454`

Key directional / release-sensitive components reviewed at the available manufacturing-preview level include U1 STM32F103C8T6, U2 LMR36510FADDAR, U3 CH340C, U4 ISO7721DR, Q25 DMT10H015LFG-13, X1, USB-C TYPE-C-31-M-12, D9/D10/D11/D12 and other polarity-sensitive parts. The selected JLCPCB polarity-handling option asks the JLCPCB engineer to use the board silkscreen to assist with direction confirmation/correction.

The final Altium schematic-to-PCB ECO check performed immediately before production confirmation showed only metadata/organization deltas: component-designator synchronization plus removal proposals for PCB-side Net Classes / Differential Pair objects. No Add/Remove Component, Add/Remove Net, pin-connectivity change or footprint replacement was present in the displayed ECO. The released manufacturing baseline was therefore not regenerated merely to normalize those metadata items.

Manufacturing-release interpretation:

```text
JLCPCB production artwork:       CONFIRMED
PCB fabrication order:           RELEASED
PCBA manufacturing order:        RELEASED
Current external state:           AWAITING PRODUCTION
New known manufacturing blocker: 0
```

This operational release record does not fabricate a separate exhaustive independent SMT orientation PASS beyond the reviewed evidence and JLCPCB engineer confirmation workflow. It also does not claim assembly fit, hardware behavior, EMC/surge, continuity, power-on or system validation results before physical boards are received.

## Stage 6 Routing Decisions That Are Locked

Unless later assembly/manufacturing evidence exposes a real defect, do not reopen the following merely for cosmetic cleanup:

- 100 mm × 80 mm board / Stage 5 placement baseline;
- routing-driven GPIO assignments listed above;
- left `CN6 = IN11–IN18`, right `CN5 = OUT1–OUT8` topology;
- USB D+/D- and USB_VBUS routing;
- Top/Bottom USB_GND strategy with explicit ISO7721 isolation cutout;
- IN11 short Bottom crossover while retaining `IN11 -> PA8`;
- SWDIO / SWCLK / NRST Bottom routing;
- Buck local GND/current-loop refinements;
- HSE local placement, GND guard, guard vias and polygon exclusion approach;
- current `.PcbDoc` Solder/Paste normalization;
- final 3V3/GND test-point geometry and critical Top Overlay unless new evidence shows a real manufacturing/assembly conflict.

## Manufacturing Status / Next Activity

The current PCB / PCBA order has been released. Do not proactively reopen already accepted routing, copper, mask, BOM or placement while the order is in production.

During manufacturing, only a new vendor query that exposes a real substitution, polarity, DFM, placement or assembly blocker should reopen the corresponding bounded review item.

After boards are received, the next engineering work should start from physical incoming evidence rather than another design re-review. Expected follow-up includes:

1. incoming visual inspection and component-population check;
2. continuity / short checks before power application;
3. controlled power-on bring-up and 3V3 verification;
4. USB-UART / isolation functional check;
5. STM32 SWD / reset / clock bring-up;
6. sensor / CM35 I/O functional validation;
7. Stage transition only when the applicable Framework / Gate evidence is actually satisfied.

## Minor / Later Mechanical Note

- `CN5` versus the bottom-right M3 screw/head/washer and removable-plug envelope should still be checked later with 3D / courtyard / real mechanical evidence when convenient.
- This is not presently a PCB fabrication blocker from the available evidence.

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

PCB finalization:
COMPLETE — 3V3/GND test points + critical Top Overlay + repour/final DRC cycle

Final DRC:
EXECUTED — 2026-09-04 21:42
Warnings 0 / Rule Violations 76
4 intentional M3 self-keepout clearance findings
66 manufacturing/mask-sliver findings
6 intentional HSE GND-guard antennae findings

Formal zero-violation DRC PASS:
NOT CLAIMED

JLCPCB Gerber/CAM review:
REVIEWED — NO NEW PCB FABRICATION BLOCKER IDENTIFIED

JLCPCB production artwork:
CONFIRMED — 2026-09-05

PCB fabrication release:
RELEASED / AWAITING PRODUCTION

PCBA / SMT manufacturing order:
RELEASED / AWAITING PRODUCTION
Top Side only; intentional THT DNP population retained for hand solder

Independent exhaustive SMT orientation PASS:
NOT SEPARATELY CLAIMED — release relies on reviewed manufacturing evidence plus selected JLCPCB engineer polarity confirmation workflow

Hardware / bring-up / validation:
NOT YET CLAIMED

Project Stage transition:
NOT PERFORMED
```