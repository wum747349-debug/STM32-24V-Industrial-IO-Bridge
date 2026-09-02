# PCB Design Rules

Document Status: **CONFIRMED RULE BASELINE — Layout Preflight IN PROGRESS**

Project Stage: **Stage 5 — PCB Layout**

This file is the owning record for PCB rule and layout-preflight constraints. Stage 4 Formal Schematic Review is **PASS / CLOSED**, so the Project may enter Stage 5 Layout Preflight. The confirmed manufacturing and rule baseline below is ready for Altium configuration; formal placement/layout approval remains pending the applicable mechanical, footprint, and user Altium Scope/Priority configuration checks.

## Current Inputs and Evidence Boundary

- Current complete schematic: `hardware/outputs/SCH_Schematic1_2026-09-01.pdf`.
- Current BOM: `hardware/outputs/BOM_Board1_Schematic1_2026-09-01.xlsx`.
- Formal schematic review: `docs/schematic_review.md`, conclusion **可以进入 PCB Layout**.
- Hardware Revision: `TBD`.
- `.PcbDoc` is the authoritative PCB implementation source when created or updated by the user in Altium Designer.
- No Altium rule configuration, Rule Scope/Priority check, PCB placement/routing, polygon state, DRC result, manufacturing output, hardware test, or EMC/surge result is claimed by this initial baseline.

## Confirmed Electrical and Domain Constraints

| Area | Confirmed constraint | Layout / rule implication | Current state |
| --- | --- | --- | --- |
| M1 positive input path | `24V_IN_RAW -> F1 -> D9 STPS2H100A -> 24V_PROTECTED` | Preserve the protection sequence and short, direct fault-current path | Documented; EDA layout pending |
| M1 negative input path | `GND_IN_RAW -> Q25 DMT10H015LFG-13 -> PCB GND` | `GND_IN_RAW` must not bypass Q25 into PCB `GND` through copper, plane, polygon, via, harness, mounting feature, or rule scope | Documented; EDA layout pending |
| Q25 mapping | Schematic symbol D/G/S ↔ PowerDI3333-8 footprint pads ↔ manufacturer pinout was finally checked by the user in Altium | Preserve the verified mapping during PCB implementation | CLOSED in Stage 4 |
| M1 buck | U2 LMR36510 input, switching, bootstrap, output, and feedback paths | Keep VIN/PGND input loop, SW/BOOT loop, and output switching-current loop compact; keep FB path away from `SW_NODE` | Relative constraint confirmed; placement/routing pending |
| M2 MCU | STM32F103C8T6 decoupling, VDDA link, HSE crystal, reset, SWD | Place local decoupling and crystal support close to their owning pins; keep the HSE cluster away from switching/noisy paths | Relative constraint confirmed; placement pending |
| M3 isolation | `USB_GND != GND` across ISO7721DR | No copper, plane, mounting feature, shield path, test point, or other object may bridge the two domains | Confirmed; Altium implementation pending |
| M3 USB | USB connector -> USBLC6-2SC6 -> CH340C | Place ESD protection close to the connector, keep its `USB_GND` return short, and avoid long D+/D- stubs | Relative constraint confirmed; numerical USB rules pending |
| M4 power domain | PSU B `+24V -> P1 -> 24V_IN_RAW -> protection -> 24V_PROTECTED`; PSU B `-V -> P1 -> GND_IN_RAW -> Q25 -> PCB GND` | PCB `GND = CM35 G / 24G` and must remain separate from CM35 system `0V` | Confirmed; placement/routing pending |
| M4 connectors | `CN5` = CM35 IN11–IN18; `CN6` = CM35 OUT1–OUT8 | Connector direction, mating access, and board-edge location require mechanical confirmation | Designators confirmed; mechanics pending |
| M5 connectors | `CN1`–`CN4` = Sensors 1–4 | Field connector access and nearby protection placement require mechanical confirmation | Designators confirmed; mechanics pending |
| M4/M5 MOSFET | Current 2N7002 is LCSC `C7420321`; Nexperia `2N7002,215` is qualification history/reference | Do not impose a mandatory substitution during layout | Confirmed |
| M1 output capacitors | C14/C15/C16 = Samsung `CL31B226KPHNNNE`, LCSC `C87996`, 22 uF / 10 V / X7R / 1206 | Place for a compact buck output-current loop | Confirmed; placement pending |

## Manufacturing and Stackup Baseline

| Item | Rule / value | Unit | Basis | Scope | Altium priority / configuration |
| --- | --- | --- | --- | --- | --- |
| Target fabricator / service | JLCPCB standard 2-layer manufacturing / SMT assembly target | N/A | Confirmed PCB baseline | Whole board | Documented; Altium / ordering configuration not claimed |
| Material | FR-4 | N/A | Confirmed PCB baseline | Whole board | Documented; Altium stackup configuration not claimed |
| Layer count | 2 | layers | Confirmed PCB baseline | Whole board | Documented; Altium layer-stack configuration not claimed |
| Finished board thickness | 1.6 | mm | Confirmed PCB baseline | Whole board | Documented; Altium stackup configuration not claimed |
| Copper weight | Top = 1; Bottom = 1 | oz | Confirmed PCB baseline | Top / Bottom copper | Documented; Altium stackup configuration not claimed |
| Controlled impedance declaration | No controlled impedance | N/A | Confirmed PCB baseline; USB geometry below is routing guidance only | Whole board | No impedance rule to configure |
| Special processes | No blind/buried vias; no via-in-pad | N/A | Confirmed PCB baseline | Whole board | Documented; actual EDA use not claimed |

Project design defaults must be distinguished from the selected fabricator's published manufacturing limits. No numerical rule may be adopted solely because it is a stated manufacturing minimum; design margin must be selected during Layout Preflight.

## Mechanical Baseline

| Item | Current value | Status |
| --- | --- | --- |
| Board outline / dimensions / corner treatment | No mechanically constrained board size; compact practical placement preferred | Confirmed placement baseline; exact outline and corner treatment remain pending |
| Mounting-hole count, type, diameter, coordinates, and keepouts | `TBD / pending Layout Preflight` | Blocking formal placement approval |
| Enclosure / rail / latch / height constraints | `TBD / pending Layout Preflight` | Pending |
| Connector board-edge positions, orientation, mating and wiring clearance | `TBD / pending Layout Preflight` | Pending; applies to CN1–CN6, P1, USB-C, SWD and user-accessible items |
| Test-point and debug-access envelope | `TBD / pending Layout Preflight` | Pending |

## Applicable Rule Configuration Baseline

The first rule baseline is configuration-first and applicability-driven: define the smallest maintainable set of rules that express the current Project's real electrical, routing, plane/copper, mechanical, and manufacturing constraints. Do not create a rule, Scope, Class, or higher-priority exception solely because a checklist, fabricator page, or EDA category exists.

| Rule / configuration intent | Value / setting | Unit | Scope / members | Basis / current state | Altium priority / configuration |
| --- | --- | --- | --- | --- | --- |
| Default electrical clearance | 8 | mil | Whole-board default | Confirmed PCB baseline | Documented; actual Altium configuration not claimed |
| `GND_IN_RAW` ↔ PCB `GND` clearance | 20 | mil | Explicit exception between `GND_IN_RAW` and `GND` only | Confirmed PCB baseline; preserves Q25 boundary | Must override the default clearance when configured; actual Altium Priority not claimed |
| Default routing width | 6 / 8 / 12 | mil (min / preferred / max) | Whole-board default | Confirmed PCB baseline | Documented; actual Altium configuration not claimed |
| `SW_NODE` routing width | 16 / 20 / 24 | mil (min / preferred / max) | `SW_NODE` | Confirmed PCB baseline | Must override the default width when configured; actual Altium Priority not claimed |
| `NC_POWER` routing width | 10 / 20 / 32 | mil (min / preferred / max) | `NC_POWER` members listed below | Confirmed PCB baseline | Must override the default width when configured; actual Altium Priority not claimed |
| Routing via style | 0.60 diameter / 0.30 drill | mm | Default routing vias | Confirmed PCB baseline | Documented; actual Altium configuration not claimed |
| `NC_POWER` Net Class | `24V_IN_RAW`, `24V_PROTECTED`, `3V3`, `USB_VBUS`, `GND_IN_RAW` | N/A | Exact members only; `VDDA`, `GND`, and `USB_GND` are not members | Confirmed PCB baseline | Documented; actual Altium class assignment not claimed |
| `GND_IN_RAW` to PCB `GND` non-bypass constraint | No copper, plane, polygon, via, harness, mounting feature, or rule scope may collapse the Q25 boundary | N/A | `GND_IN_RAW` and PCB `GND` objects around Q25 | Confirmed Project constraint | Not configured / not claimed |
| `USB_GND` to machine-side `GND` isolation constraint | No copper, plane, mounting feature, shield path, test point, or other object may bridge the domains | N/A | `USB_GND` and machine-side PCB `GND` across ISO7721DR | Confirmed Project constraint | Any applicable exception must override overlapping defaults when configured; not configured / not claimed |
| USB differential-pair routing | Width = 8; gap = 8; maximum uncoupled length = 200 | mil | `USB_DP_RAW` / `USB_DM_RAW` and `USB_DP` / `USB_DM` | Confirmed routing-geometry guidance; not a controlled-impedance guarantee | Documented; actual Altium differential-pair configuration not claimed |
| Buck regulator critical loop / feedback routing | Relative placement and routing constraint; numerical values `TBD` where needed | mm or rule setting as applicable | U2 LMR36510 VIN/PGND input loop, SW/BOOT loop, output loop, `SW_NODE`, and FB path | Confirmed Project constraint; placement/routing pending | Not configured / not claimed |
| Polygon connect style | THT = Relief Connect, 4 conductors, conductor width = 10 mil, air gap = 8 mil; SMD = Direct Connect; Via = Direct Connect | mil / N/A | Applicable polygon connections; preserve `GND_IN_RAW != GND` and `USB_GND != GND` | Confirmed PCB baseline | Documented; polygon state and Altium configuration not claimed |
| Hole size | minimum = 10; maximum = 240 | mil | Applicable drilled holes | Confirmed PCB baseline | Documented; actual Altium configuration not claimed |
| Hole-to-hole clearance | 8 | mil | Applicable drilled holes | Confirmed PCB baseline | Documented; actual Altium configuration not claimed |
| PTH minimum annular ring | 10 | mil | Applicable plated through holes | Confirmed PCB baseline | Documented; actual Altium configuration not claimed |
| Board outline clearance | 12 | mil | Applicable copper / object clearance to board outline | Confirmed PCB baseline | Documented; actual Altium configuration not claimed |
| Component clearance | 20 | mil | Component-to-component baseline | Confirmed PCB baseline | Documented; actual Altium configuration not claimed |
| Package-specific fabrication details | `TBD / pending Layout Preflight` where applicable | mm or N/A | Only pads/packages with real solder-mask, paste, courtyard, height, thermal-pad, or assembly differences | Remaining footprint and assembly review pending | Not configured / not claimed |

## Planned Scope and Priority Work

- Establish the documented default rules and the `NC_POWER` exception scope in Altium; retain the smallest maintainable rule set.
- Create Net Classes, Object Classes, explicit scopes, or higher-priority exception rules only where members share a real electrical, routing, manufacturing, mechanical, or verification behavior. `NC_POWER` is the confirmed Net Class and has only the members listed above; `VDDA`, PCB `GND`, and `USB_GND` are not default members.
- Keep `GND_IN_RAW` distinct from PCB `GND`; no rule, polygon, or class assignment may collapse this boundary around Q25.
- Keep `USB_GND` distinct from machine-side `GND`; any isolation-specific rule must have a precise Scope and higher Priority than an overlapping default rule when the user configures it.
- Define special rules only where actual current, voltage, return-path, differential, thermal, mechanical, or verification needs justify them.
- Do not mechanically expand Annular Ring, Mask, Paste, Silkscreen, Board-edge, or other rule categories unless the current Project facts, selected manufacturing path, package needs, or mechanical implementation make them applicable.
- The user must configure applicable rules in Altium Designer and manually confirm Scope coverage and Priority before formal placement approval. Documentation alone is not implementation evidence.

## Layout Preflight Open Items

- Confirm exact board/hardware revision and traceable relationship among `.SchDoc`, current PDF/BOM, and the target `.PcbDoc`.
- Configure the confirmed JLCPCB standard 2-layer / SMT baseline and applicable documented rules in Altium, then manually check their Scope and Priority.
- Freeze the exact board outline, mounting holes, enclosure constraints, connector orientation, insertion paths, and wiring/debug access; board size itself is not mechanically constrained, and compact practical placement is preferred.
- Verify remaining critical footprints, polarity, Pin 1, pad mapping, thermal-pad, courtyard, height, solder-mask, and paste requirements in Altium. The closed Q25 mapping is not a claim that all other footprints are verified.
- Select only applicable rule values/settings with stated units, basis, Scope, and Priority. Known candidates include clearance, width, via/hole, USB routing, polygon/plane strategy, 24 V/protection-domain constraints, isolation-domain constraints, buck layout constraints, and any package/manufacturing/mechanical rules made applicable by the selected stackup, service, footprints, board outline, or mounting features.
- Have the user configure and manually check the applicable Altium rules, Scope, and Priority.

## Current Layout Preflight Conclusion

**Stage 5 Layout Preflight may proceed. Formal placement/layout approval is pending the open items above.** Initial DRC is not required for Layout Preflight entry, and no DRC status is recorded.
