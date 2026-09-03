# PCB Design Rules

Document Status: **CONFIRMED RULE BASELINE — STAGE 6 ROUTING/COPPER IMPLEMENTED — DRC EXECUTED — FINAL PCB REVIEW PENDING**

Project Stage: **Stage 6 — Routing and Copper**

This file owns the Project PCB rule and routing/copper baseline. Stage 4 Formal Schematic Review is **PASS / CLOSED** and Stage 5 Placement is **PASS / CLOSED**. Stage 6 routing, polygon implementation and GND-via stitching are substantially complete from user-provided Altium evidence. The active `.PcbDoc` remains the implementation authority. DRC has now been executed, but a formal all-violations-cleared DRC PASS and manufacturing release are not yet claimed.

## Current Inputs and Evidence Boundary

- Current complete schematic: `hardware/outputs/SCH_Schematic1_2026-09-01.pdf`.
- Current BOM: `hardware/outputs/BOM_Board1_Schematic1_2026-09-01.xlsx`.
- Formal schematic review: `docs/schematic_review.md`.
- Placement / routing / copper review record: `docs/pcb_review.md`.
- Hardware Revision: `TBD`.
- User-provided Altium screenshots and exported DRC reports are valid interactive engineering evidence.
- The current `.PcbDoc` remains the object-level PCB implementation authority.
- No Gerber/manufacturing-output PASS, hardware-test PASS, EMC/surge result, or final manufacturing release is claimed here.

## Confirmed Electrical and Domain Constraints

| Area | Confirmed constraint | PCB implication |
| --- | --- | --- |
| M1 positive input | `24V_IN_RAW -> F1 -> D9 -> 24V_PROTECTED` | Preserve protection sequence and direct current path |
| M1 negative input | `GND_IN_RAW -> Q25 -> PCB GND` | `GND_IN_RAW` must never bypass Q25 into PCB `GND` through copper, polygon, via, mounting feature, shield or harness |
| M1 buck | U2 LMR36510 VIN/PGND, SW/BOOT, output and FB loops | Keep input/current loops compact; keep `SW_NODE` local; keep FB away from switching copper |
| M2 MCU | STM32F103C8T6 decoupling, VDDA, HSE, reset, SWD | Preserve local routing/return structure; no noisy crossing through protected HSE area |
| M3 isolation | `USB_GND != GND` across ISO7721DR | No copper, plane, via, shield path, test point, mounting feature or other object may bridge domains |
| M3 USB | USB-C -> USB protection -> CH340C -> ISO7721 | Keep D+/D- short/local; preserve ESD return and domain boundary |
| M4 supply domain | PCB `GND = CM35 G / 24G = PSU B -V` | Must remain separate from CM35 system `0V`, PSU A `-V`, PE and chassis |
| M4 connectors | left `CN6 = IN11–IN18`; right `CN5 = OUT1–OUT8` | Preserve current physical topology and routing-driven mapping |
| M5 connectors | `CN1`–`CN4` = Sensors 1–4 | Preserve local frontend / edge topology unless final review finds a real defect |

## Manufacturing and Stackup Baseline

| Item | Current value |
| --- | --- |
| Target fabricator / service | JLCPCB standard 2-layer manufacturing / SMT assembly target |
| Material | FR-4 |
| Layer count | 2 |
| Finished thickness | 1.6 mm |
| Copper | Top 1 oz / Bottom 1 oz |
| Controlled impedance | Not declared; USB geometry is routing guidance, not an impedance guarantee |
| Special via process | No blind/buried vias; no via-in-pad |

## Mechanical Baseline

| Item | Current value / status |
| --- | --- |
| Board | **100 mm × 80 mm**, R3 corner fillets |
| Mounting | **4 × M3 NPTH**, 3.20 mm drill, No Net |
| Nominal hole positions | centers 4 mm from adjacent board edges: `(4,4)`, `(96,4)`, `(4,76)`, `(96,76)` mm when lower-left is origin |
| Mounting keepout | approximately **Ø7.0 mm solid Keepout Region**, restricting copper / track / via / pads around each mounting hole |
| Connector topology | CN1–CN6, P1 and USB-C remain at board edges according to current Stage 5/6 topology |
| Remaining mechanical note | later check `CN5` versus bottom-right M3 screw/head/washer/mating-plug envelope using 3D / courtyard / real mechanical evidence |

## Applicable Altium Rule Baseline

The active Altium DRC configuration shown in the latest user-provided report is the current Stage 6 working rule baseline. Manufacturing limits are not automatically adopted as design targets.

| Rule / intent | Current value | Scope / note |
| --- | --- | --- |
| Default electrical clearance | **6 mil** | whole-board default |
| `GND_IN_RAW` ↔ `GND` clearance | **20 mil** | explicit higher-priority exception |
| Default routing width | **6 / 6 / 15 mil** | min / preferred / max |
| `SW_NODE` width | **16 / 20 / 24 mil** | min / preferred / max |
| `NC_POWER` width | **8 / 20 / 32 mil** | min / preferred / max |
| `NC_POWER` Net Class | `24V_IN_RAW`, `24V_PROTECTED`, `3V3`, `USB_VBUS`, `GND_IN_RAW` | `VDDA`, `GND`, `USB_GND` are not members |
| Typical power routing | 20 mil | preferred where local copper is not more appropriate; 8 mil is accepted as the configured local minimum |
| Default routing via | 0.60 mm diameter / 0.30 mm drill | whole-board default routing via |
| USB pair geometry | width 8 mil / gap 8 mil / max uncoupled 200 mil | routing guidance only; no controlled-impedance claim |
| Power-plane / relief connect | 4 entries, 10 mil conductor, 10 mil air gap, 20 mil expansion | current DRC-reported connection rule |
| Polygon connect intent | SMD Direct; Via Direct; preserve intentional THT relief and all domain boundaries | implementation must not bridge isolated nets |
| Hole size | **10–240 mil** | applicable drilled holes |
| Hole-to-hole clearance | **8 mil** | keep at 8 mil for current project baseline |
| Minimum solder-mask sliver | **6 mil** | current DRC baseline; latest report has 0 violations |
| Silk-to-solder-mask clearance | **6 mil** | documentation / manufacturability cleanup item when violated |
| Silk-to-silk clearance | **6 mil** | documentation / legibility cleanup item; not an electrical blocker by itself |
| Net Antennae tolerance | **0 mil** | retain checker; intentional HSE GND guard branches are explicitly dispositioned in `docs/pcb_review.md` |
| PTH minimum annular ring | 10 mil | applicable plated holes |
| Board-outline clearance | 12 mil | applicable copper / object clearance |
| Component clearance | 20 mil | component-to-component baseline |

## Implemented Stage 6 Layer / Copper Strategy

```text
Top:
- primary GPIO / local signals
- local power and critical loops
- broad machine-side GND polygon where useful
- USB-domain Top USB_GND copper in the isolated USB region
- HSE signal routing and local GND guard with dedicated Top cutout

Bottom:
- machine-side GND reference plane as the dominant use
- isolated USB-domain USB_GND polygon
- limited regional 3V3 trunks
- only necessary short GPIO / SWD / NRST crossovers
```

Do not reroute already-accepted regions merely to force every signal onto Top. Conversely, do not expand Bottom signal usage if it unnecessarily fragments the GND plane.

## Routing-Driven GPIO Baseline

```text
IN11 -> PA8
IN12 -> PA11
IN13 -> PA12
IN14 -> PA15
IN15 -> PB4
IN16 -> PB5
IN17 -> PB6
IN18 -> PB7

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

These are now PCB routing facts. Reopening them requires final-review evidence of a real electrical / DRC / routing defect.

## USB / Isolation Copper Baseline

- USB D+/D- and USB_VBUS routing are complete at screenshot level and should remain frozen unless final review finds a defect.
- The isolated USB area uses **Bottom USB_GND polygon** as its primary reference/return copper.
- A **Top USB_GND polygon/copper area is now implemented** in the USB domain to improve local return connectivity; this supersedes the earlier note that no broad Top USB_GND copper had been added.
- Top and Bottom USB-domain copper remain confined to the USB side of the ISO7721 boundary.
- USB-domain GND pads connect locally by short copper / vias into the Top/Bottom USB_GND structure.
- ISO7721 is the boundary between `USB_VBUS / USB_GND` and `3V3 / GND`.
- **Top and Bottom polygon-pour cutouts / copper exclusion remain through the ISO7721 isolation region.** No via is intentionally placed inside the isolation corridor.
- `USB_GND` stitching vias may be used inside the USB domain; machine `GND` vias remain on the machine side. No cross-boundary via fence is required.
- `IN11 -> PA8` is retained; the isolation-area conflict is solved by a short Bottom crossover that stays machine-side and outside the ISO7721 exclusion region.

## Buck Ground / Switching Baseline

- U2 exposed pad uses multiple GND / thermal vias.
- C11/C12 input-capacitor GND is implemented as a compact local Top GND copper connection with multiple vias into the Bottom GND plane.
- C14/C15/C16 output-capacitor GND uses broad local GND copper and multiple vias.
- Preserve the compact C11/C12 -> U2 VIN/PGND high-current input loop.
- `SW_NODE` must remain local; do not expand the switch-node copper during cosmetic cleanup.
- R37/R42 FB routing is a small-signal path and must remain away from `SW_NODE`.
- Final copper review must explicitly prove `GND_IN_RAW` does not bypass Q25.

## HSE Crystal Baseline

- X1/C2/C4 placement is frozen unless DRC or electrical review identifies a real problem.
- OSC traces remain short, local, Top-layer and without intentional vias.
- X1 GND/case pads and C2/C4 GND pads use local GND vias.
- Top uses a **10 mil GND guard track** around the local oscillator region.
- Guard/local-ground vias connect the oscillator GND structure into Bottom GND.
- A **Top Polygon Pour Cutout** excludes the oscillator zone from broad Top GND fill so the guard structure remains explicit.
- Bottom under/around the oscillator is reserved as a quiet local GND return/shield area; unrelated GPIO, SWD, UART, NRST, 3V3 trunks or other crossovers must not traverse it.
- The latest DRC reports six `Net Antennae` findings in this area. User-provided object-level screenshot evidence confirms they are the intentional GND guard tracks / GND stitching vias, not unassigned copper or unrouted signal stubs. They are accepted review findings; an Altium waiver object is not claimed unless separately created.

## Debug Routing Baseline

- SWDIO, SWCLK and MCU_NRST use Bottom routing where required by crossing topology.
- The NRST Bottom segment may pass under the projection of MCU pin 39 because the MCU pad is a Top SMD object; actual clearances are now covered by the executed DRC.
- SWDIO / SWCLK do not require differential or length-matching rules.

## Whole-Board GND / Polygon Baseline

Machine-side GND-via stitching is now substantially complete at screenshot level. USB-domain stitching has also been added without bridging the isolation boundary.

Before Stage 6 closeout, final repour/review must still confirm:

- Bottom machine `GND` remains broadly continuous despite Bottom 3V3 trunks and short crossovers.
- No disconnected / orphan copper islands remain.
- No narrow GND neck is created around MCU fanout or long parallel Bottom traces.
- `USB_GND` and machine `GND` remain isolated.
- `GND_IN_RAW` and machine `GND` remain separated except through Q25 as designed.
- HSE Bottom GND remains quiet and free of unrelated signal crossings.
- Buck, MCU decoupling, VDDA, SWD/UART and connector return paths remain sensible after final repour.
- M3 mounting-hole keepouts remain free of unintended copper / vias / tracks.

## Latest DRC Evidence — 2026-09-03 20:33

Latest user-provided Altium Design Rule Verification Report:

```text
Warnings: 0
Rule Violations: 29

Electrical / connectivity blockers:
Short-Circuit: 0
Un-Routed Net: 0
Default Width: 0
SW_NODE Width: 0
NC_POWER Width: 0
GND_IN_RAW <-> GND 20 mil Clearance: 0
Hole Size: 0
Hole-to-Hole: 0
Minimum Solder Mask Sliver: 0
Modified Polygon: 0
```

Remaining 29 findings are currently dispositioned as:

- **4 × Clearance**: each M3 NPTH `Free-2` pad intersects its own intentionally centered solid Keepout Region. This is an intentional mounting-hole geometry / rule-scope collision, not evidence of copper entering the keepout. Preserve the M3 hole and keepout; handle with targeted exception / waiver if a clean numeric DRC is required.
- **2 × Silk-to-Solder-Mask**: Q12 top-overlay geometry is too close to the pad solder-mask opening. Non-electrical cleanup; easy to correct and recommended before manufacturing output.
- **17 × Silk-to-Silk**: reference-designator / footprint-silkscreen spacing. Non-electrical legibility cleanup; do not move components merely to clear these.
- **6 × Net Antennae**: confirmed intentional HSE GND guard tracks / GND vias. Preserve the guard structure; treat as accepted intentional findings or targeted waiver.

Therefore, **no currently reported violation represents a confirmed electrical routing/connectivity blocker**, but a formal DRC PASS is not claimed while the report still contains 29 findings.

## Stage 6 Final Review / Closeout Requirements

Stage 6 is **not yet closed**. The next activity is final PCB review and DRC disposition, not more routine routing.

Required evidence before any closeout / manufacturing transition:

1. No unintended unrouted nets or incomplete connections — latest DRC currently shows 0.
2. Full-board Top / Bottom routing review.
3. Final Bottom `GND` and `USB_GND` polygon continuity / island / narrow-neck review.
4. `USB_GND != GND` verification across ISO7721 after final repour.
5. `GND_IN_RAW != GND` / Q25 non-bypass verification.
6. Buck critical-loop / `SW_NODE` / FB review.
7. HSE guard / return / no-crossing review; preserve intentional guard antennae findings.
8. MCU decoupling / VDDA / NRST / SWD return review.
9. Board-edge / M3 keepout / connector mechanical review.
10. Final disposition of the 4 intentional M3 self-keepout collisions, 6 intentional HSE antennae findings, and remaining silkscreen cleanup findings.

## Current Conclusion

**Stage 5 Placement remains PASS / CLOSED. Stage 6 routing, polygons and GND-via implementation are complete at user/screenshot level. DRC has been executed and no electrical blocker remains in the latest report, but formal DRC PASS, final routed-copper PASS and manufacturing release remain pending until final whole-board review and disposition of the remaining intentional / silkscreen findings.**
