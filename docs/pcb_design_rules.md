# PCB Design Rules

Document Status: **CONFIRMED RULE BASELINE — STAGE 5 PLACEMENT CLOSED / STAGE 6 ACTIVE**

Project Stage: **Stage 6 — Routing and Copper**

This file owns the PCB rule and layout/routing constraints. Stage 4 Formal Schematic Review is **PASS / CLOSED**. Stage 5 full-board Placement has now been reviewed from the user-provided Altium placement and Ratsnest evidence and is **PASS / CLOSED**. The confirmed manufacturing, rule, and mechanical baseline below is the routing-entry baseline; the `.PcbDoc` remains the implementation authority.

## Current Inputs and Evidence Boundary

- Current complete schematic: `hardware/outputs/SCH_Schematic1_2026-09-01.pdf`.
- Current BOM: `hardware/outputs/BOM_Board1_Schematic1_2026-09-01.xlsx`.
- Formal schematic review: `docs/schematic_review.md`, conclusion **可以进入 PCB Layout**.
- Stage 5 placement review record: `docs/pcb_review.md`.
- Hardware Revision: `TBD`.
- The user-provided full-board Altium placement / Ratsnest screenshots are the current Stage 5 placement evidence; they are not a substitute for `.PcbDoc` object parsing or DRC.
- `.PcbDoc` is the authoritative PCB implementation source.
- No DRC PASS, routed-copper PASS, manufacturing-output PASS, hardware-test PASS, or EMC/surge result is claimed by this baseline.

## Confirmed Electrical and Domain Constraints

| Area | Confirmed constraint | Layout / rule implication | Current state |
| --- | --- | --- | --- |
| M1 positive input path | `24V_IN_RAW -> F1 -> D9 STPS2H100A -> 24V_PROTECTED` | Preserve the protection sequence and short, direct fault-current path | Placement closed; routing pending |
| M1 negative input path | `GND_IN_RAW -> Q25 DMT10H015LFG-13 -> PCB GND` | `GND_IN_RAW` must not bypass Q25 into PCB `GND` through copper, plane, polygon, via, harness, mounting feature, or rule scope | Placement closed; routing pending |
| Q25 mapping | Schematic symbol D/G/S ↔ PowerDI3333-8 footprint pads ↔ manufacturer pinout was finally checked by the user in Altium | Preserve the verified mapping during PCB implementation | CLOSED in Stage 4 |
| M1 buck | U2 LMR36510 input, switching, bootstrap, output, and feedback paths | Keep VIN/PGND input loop, SW/BOOT loop, and output switching-current loop compact; keep FB path away from `SW_NODE` | Placement closed; routing pending |
| M2 MCU | STM32F103C8T6 decoupling, VDDA link, HSE crystal, reset, SWD | Preserve the already-reviewed local decoupling/crystal placement; keep HSE and VDDA routing away from switching/noisy paths | Placement closed; routing pending |
| M3 isolation | `USB_GND != GND` across ISO7721DR | No copper, plane, mounting feature, shield path, test point, or other object may bridge the two domains | Placement closed; copper/routing boundary remains mandatory |
| M3 USB | USB connector -> USBLC6-2SC6 -> CH340C | Keep ESD return short, avoid long D+/D- stubs, and preserve the existing connector/protection/UART ordering | Placement closed; routing pending |
| M4 power domain | PSU B `+24V -> P1 -> 24V_IN_RAW -> protection -> 24V_PROTECTED`; PSU B `-V -> P1 -> GND_IN_RAW -> Q25 -> PCB GND` | PCB `GND = CM35 G / 24G` and must remain separate from CM35 system `0V` | Confirmed; routing/copper pending |
| M4 connectors | `CN6` = CM35 IN11–IN18; `CN5` = CM35 OUT1–OUT8 | Preserve the Stage 5 physical topology: left-side `CN6 -> IN circuitry -> MCU`, and `MCU -> OUT circuitry -> right-side CN5` | Placement PASS / locked for routing |
| M5 connectors | `CN1`–`CN4` = Sensors 1–4 | Preserve current board-edge connector placement and nearby frontend grouping unless routing evidence reveals a real blocker | Placement PASS / locked for routing |
| M4/M5 MOSFET | Current 2N7002 is LCSC `C7420321`; Nexperia `2N7002,215` is qualification history/reference | Do not impose a mandatory substitution during layout/routing | Confirmed |
| M1 output capacitors | C14/C15/C16 = Samsung `CL31B226KPHNNNE`, LCSC `C87996`, 22 uF / 10 V / X7R / 1206 | Preserve the compact buck output-current loop | Placement closed; routing pending |

## Manufacturing and Stackup Baseline

| Item | Rule / value | Unit | Basis | Scope | Altium priority / configuration |
| --- | --- | --- | --- | --- | --- |
| Target fabricator / service | JLCPCB standard 2-layer manufacturing / SMT assembly target | N/A | Confirmed PCB baseline | Whole board | Documented; ordering configuration not claimed |
| Material | FR-4 | N/A | Confirmed PCB baseline | Whole board | Documented |
| Layer count | 2 | layers | Confirmed PCB baseline | Whole board | Documented |
| Finished board thickness | 1.6 | mm | Confirmed PCB baseline | Whole board | Documented |
| Copper weight | Top = 1; Bottom = 1 | oz | Confirmed PCB baseline | Top / Bottom copper | Documented |
| Controlled impedance declaration | No controlled impedance | N/A | Confirmed PCB baseline; USB geometry below is routing guidance only | Whole board | No impedance rule required |
| Special processes | No blind/buried vias; no via-in-pad | N/A | Confirmed PCB baseline | Whole board | Documented |

Project design defaults must be distinguished from the selected fabricator's published manufacturing limits. No numerical rule may be adopted solely because it is a stated manufacturing minimum; design margin must be selected for this Project.

## Mechanical Baseline

The dimensions below are the current **Stage 5 closed placement baseline**. The board was intentionally reduced from 110 mm × 80 mm to 100 mm × 80 mm before routing because the right-side placement had usable excess width and could be tightened without creating a routing blocker.

| Item | Current value | Status |
| --- | --- | --- |
| Board outline / dimensions / corner treatment | **100 mm × 80 mm**, rectangular with **R3 mm** corner fillets | Confirmed Stage 5 closed baseline |
| Width-reduction decision | Previous working outline **110 mm × 80 mm** -> current **100 mm × 80 mm**, primarily by reducing the right side and moving the right-side placement group / mounting holes inward | Accepted; further width reduction is not recommended before routing |
| Mounting-hole count / type | **4 × M3 NPTH**, round, **3.20 mm drill**, non-plated, No Net | Confirmed mechanical baseline |
| Mounting-hole nominal coordinates | Hole centers **4 mm from the two adjacent board edges**. For a 100 × 80 mm outline with lower-left origin: `(4,4)`, `(96,4)`, `(4,76)`, `(96,76)` mm | Nominal closed baseline; final `.PcbDoc` position remains implementation authority |
| Mounting-hole keepout | Each M3 hole uses an approximately **Ø7.0 mm solid Keepout Region** centered on the hole, on **Keep-Out Layer**, restricting **Via / Track / Copper / SMD Pad / TH Pad** | Confirmed mechanical/copper keepout baseline |
| Enclosure / rail / latch / height constraints | No fixed enclosure, rail, latch, or board-size constraint is currently imposed; maintain practical component and wiring access | No blocking external constraint identified |
| Connector placement | CN1–CN6, P1 and USB-C are positioned at board edges according to their functional topology; current placement is locked for Stage 6 unless routing evidence exposes a real blocker | Stage 5 PASS |
| Mechanical follow-up | `CN5` versus the bottom-right M3 screw/head/washer/mating-plug envelope should be checked later in 3D / final mechanical review | Minor note; does not block Stage 6 |
| Test-point and debug-access envelope | Current placement accepted from 2D evidence; final assembly/debug access remains later verification | Not a Stage 6 blocker |

The M3 keepout is a mechanical/electrical exclusion zone for the screw/head/washer area and does not replace the board-edge clearance rule. The four mounting holes are ordinary mechanical mounting points and are not intentional chassis/PE/GND connections.

## Applicable Rule Configuration Baseline

The rule baseline is configuration-first and applicability-driven: define the smallest maintainable set of rules that express the current Project's real electrical, routing, plane/copper, mechanical, and manufacturing constraints. Do not create a rule, Scope, Class, or higher-priority exception solely because an EDA category exists.

| Rule / configuration intent | Value / setting | Unit | Scope / members | Basis / current state | Altium priority / configuration |
| --- | --- | --- | --- | --- | --- |
| Default electrical clearance | 8 | mil | Whole-board default | Confirmed PCB baseline | Documented |
| `GND_IN_RAW` ↔ PCB `GND` clearance | 20 | mil | Explicit exception between `GND_IN_RAW` and `GND` only | Confirmed PCB baseline; preserves Q25 boundary | Must override the default clearance |
| Default routing width | 6 / 8 / 12 | mil (min / preferred / max) | Whole-board default | Confirmed PCB baseline | Documented |
| `SW_NODE` routing width | 16 / 20 / 24 | mil (min / preferred / max) | `SW_NODE` | Confirmed PCB baseline | Must override the default width |
| `NC_POWER` routing width | 10 / 20 / 32 | mil (min / preferred / max) | `NC_POWER` members listed below | Confirmed PCB baseline | Must override the default width |
| Routing via style | 0.60 diameter / 0.30 drill | mm | Default routing vias | Confirmed PCB baseline | Documented |
| `NC_POWER` Net Class | `24V_IN_RAW`, `24V_PROTECTED`, `3V3`, `USB_VBUS`, `GND_IN_RAW` | N/A | Exact members only; `VDDA`, `GND`, and `USB_GND` are not members | Confirmed PCB baseline | Documented |
| `GND_IN_RAW` to PCB `GND` non-bypass constraint | No copper, plane, polygon, via, harness, mounting feature, or rule scope may collapse the Q25 boundary | N/A | `GND_IN_RAW` and PCB `GND` objects around Q25 | Confirmed Project constraint | Mandatory during routing/copper |
| `USB_GND` to machine-side `GND` isolation constraint | No copper, plane, mounting feature, shield path, test point, or other object may bridge the domains | N/A | `USB_GND` and machine-side PCB `GND` across ISO7721DR | Confirmed Project constraint | Mandatory during routing/copper |
| USB differential-pair routing | Width = 8; gap = 8; maximum uncoupled length = 200 | mil | `USB_DP_RAW` / `USB_DM_RAW` and `USB_DP` / `USB_DM` | Confirmed routing-geometry guidance; not a controlled-impedance guarantee | Documented |
| Buck regulator critical loop / feedback routing | Relative placement and routing constraint; numerical values `TBD` where needed | mm or rule setting as applicable | U2 LMR36510 VIN/PGND input loop, SW/BOOT loop, output loop, `SW_NODE`, and FB path | Confirmed Project constraint | Routing pending |
| Polygon connect style | THT = Relief Connect, 4 conductors, conductor width = 10 mil, air gap = 8 mil; SMD = Direct Connect; Via = Direct Connect | mil / N/A | Applicable polygon connections; preserve `GND_IN_RAW != GND` and `USB_GND != GND` | Confirmed PCB baseline | Documented |
| Hole size | minimum = 10; maximum = 240 | mil | Applicable drilled holes | Confirmed PCB baseline | Documented |
| Hole-to-hole clearance | 8 | mil | Applicable drilled holes | Confirmed PCB baseline | Documented |
| PTH minimum annular ring | 10 | mil | Applicable plated through holes | Confirmed PCB baseline | Documented |
| Board outline clearance | 12 | mil | Applicable copper / object clearance to board outline | Confirmed PCB baseline | Documented |
| Component clearance | 20 | mil | Component-to-component baseline | Confirmed PCB baseline | Documented |
| Package-specific fabrication details | `TBD` where applicable | mm or N/A | Only pads/packages with real solder-mask, paste, courtyard, height, thermal-pad, or assembly differences | Remaining assembly/manufacturing review item | Not a Stage 6 entry blocker unless a real package issue is found |

## Stage 6 Routing Entry Strategy

Stage 6 should proceed incrementally rather than by completing one connector indiscriminately. Current routing order is:

```text
critical / module-local networks
-> MCU fanout / escape
-> inter-module signals
-> power distribution
-> GND / copper / stitching
```

Within that sequence:

- Keep USB and isolation-domain routing local to M3 and do not bridge `USB_GND` to machine-side `GND`.
- Keep the LMR36510 VIN/PGND, SW/BOOT, output-current, and FB routing local and compact; ordinary signal routing must not cross the sensitive switching area without a justified return-path plan.
- Preserve the Stage 5 connector topology: left `CN6` = IN11–IN18, right `CN5` = OUT1–OUT8, and CN1–CN4 = Sensors 1–4.
- Use the available MCU-side routing corridors for fanout before deciding that any already-locked module must be moved.
- Treat GND/polygon work as a planned copper stage, while preserving return paths during signal and power routing; do not allow later copper to collapse the Q25 or ISO7721 isolation boundaries.

## Stage 6 Open Verification Items

- Confirm the active `.PcbDoc` implements the **100 × 80 mm / R3 / 4 × M3 NPTH** baseline and the intended keepouts before substantial routing progresses.
- Preserve and periodically re-check `GND_IN_RAW != GND` and `USB_GND != GND` while tracks, vias, polygons and stitching are added.
- Review each completed routing group from Altium screenshots / network highlighting before moving to the next high-density group when useful.
- Run and record applicable DRC later; no current DRC PASS is claimed.
- Check `CN5` versus the bottom-right M3 mechanical envelope in 3D / final mechanical review when suitable evidence is available.
- Final connector mate access, component height, manufacturing output and hardware behavior remain later-stage verification items.

## Current Conclusion

**Stage 5 Placement: PASS / CLOSED. PCB baseline is 100 mm × 80 mm with R3 corners and 4 × M3 NPTH mounting holes / keepouts. No full-board placement blocker was found in the reviewed Altium Ratsnest evidence. Stage 6 — Routing and Copper may proceed.**
