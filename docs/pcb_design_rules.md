# PCB Design Rules

Document Status: **INITIAL BASELINE — Layout Preflight IN PROGRESS**

Project Stage: **Stage 5 — PCB Layout**

This file is the owning record for PCB rule and layout-preflight constraints. Stage 4 Formal Schematic Review is **PASS / CLOSED**, so the Project may enter Stage 5 Layout Preflight. Formal placement/layout work is not yet approved by this record because the manufacturing, mechanical, applicable rule, and Altium configuration items marked below remain pending.

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
| Target fabricator / service | JLCPCB / LCSC and SMT / PCBA preferred; exact service and capability source pending Layout Preflight | N/A | Project intent | Whole board | Not configured / not claimed |
| Material | `TBD / pending Layout Preflight` | N/A | Manufacturer selection pending | Whole board | Not configured / not claimed |
| Layer count | `TBD / pending Layout Preflight` | layers | Stackup decision pending | Whole board | Not configured / not claimed |
| Finished board thickness | `TBD / pending Layout Preflight` | mm | Mechanical and stackup decision pending | Whole board | Not configured / not claimed |
| Copper weight | `TBD / pending Layout Preflight` | oz or µm | Current/fabrication decision pending | Per copper layer | Not configured / not claimed |
| Assembly side(s) | `TBD / pending Layout Preflight` | N/A | Placement and PCBA decision pending | Whole board | Not configured / not claimed |
| Controlled impedance declaration | `TBD / pending Layout Preflight` | N/A | USB routing and stackup decision pending | Applicable nets only | Not configured / not claimed |
| Special processes | `TBD / pending Layout Preflight` | N/A | Fabrication/assembly needs pending | As applicable | Not configured / not claimed |

Project design defaults must be distinguished from the selected fabricator's published manufacturing limits. No numerical rule may be adopted solely because it is a stated manufacturing minimum; design margin must be selected during Layout Preflight.

## Mechanical Baseline

| Item | Current value | Status |
| --- | --- | --- |
| Board outline / dimensions / corner treatment | `TBD / pending Layout Preflight` | Blocking formal placement approval |
| Mounting-hole count, type, diameter, coordinates, and keepouts | `TBD / pending Layout Preflight` | Blocking formal placement approval |
| Enclosure / rail / latch / height constraints | `TBD / pending Layout Preflight` | Pending |
| Connector board-edge positions, orientation, mating and wiring clearance | `TBD / pending Layout Preflight` | Pending; applies to CN1–CN6, P1, USB-C, SWD and user-accessible items |
| Test-point and debug-access envelope | `TBD / pending Layout Preflight` | Pending |

## Applicable Rule Configuration Baseline

The first rule baseline is configuration-first and applicability-driven: define the smallest maintainable set of rules that express the current Project's real electrical, routing, plane/copper, mechanical, and manufacturing constraints. Do not create a rule, Scope, Class, or higher-priority exception solely because a checklist, fabricator page, or EDA category exists.

| Rule / configuration intent | Value / setting | Unit | Scope / members | Basis / current state | Altium priority / configuration |
| --- | --- | --- | --- | --- | --- |
| Default electrical clearance | `TBD / pending Layout Preflight` | mm | Whole-board default plus justified exceptions only | Fabricator capability and project design-margin decision pending | Not configured / not claimed |
| Power/load trace width | `TBD / pending Layout Preflight` | mm | Default, 3V3, 24 V, and load-specific scopes only where current/thermal behavior differs | Current, temperature rise, copper weight, and route-length decision pending | Not configured / not claimed |
| Routing via style | `TBD / pending Layout Preflight` | mm | Default vias plus power/thermal exceptions only if justified | Stackup, fabricator capability, and current/thermal decision pending | Not configured / not claimed |
| 24 V input/protection separation | `TBD / pending Layout Preflight` | mm or rule setting as applicable | `24V_IN_RAW`, `24V_PROTECTED`, `GND_IN_RAW`, PCB `GND`, and Q25 protection boundary | Project safety/domain constraint confirmed; numerical value pending | Not configured / not claimed |
| `GND_IN_RAW` to PCB `GND` non-bypass constraint | No copper, plane, polygon, via, harness, mounting feature, or rule scope may collapse the Q25 boundary | N/A | `GND_IN_RAW` and PCB `GND` objects around Q25 | Confirmed Project constraint | Not configured / not claimed |
| `USB_GND` to machine-side `GND` isolation constraint | No copper, plane, mounting feature, shield path, test point, or other object may bridge the domains | N/A | `USB_GND` and machine-side PCB `GND` across ISO7721DR | Confirmed Project constraint | Any applicable exception must override overlapping defaults when configured; not configured / not claimed |
| USB D+/D- routing | `TBD / pending Layout Preflight` | mm / ohm if applicable | Current USB data nets only, after reliable netlist/EDA confirmation | Stackup, controlled-impedance intent, and official routing basis pending | Not configured / not claimed |
| Buck regulator critical loop / feedback routing | Relative placement and routing constraint; numerical values `TBD` where needed | mm or rule setting as applicable | U2 LMR36510 VIN/PGND input loop, SW/BOOT loop, output loop, `SW_NODE`, and FB path | Confirmed Project constraint; placement/routing pending | Not configured / not claimed |
| Polygon / plane connection strategy | `TBD / pending Layout Preflight` | N/A | Per actual power and ground domain; must preserve `GND_IN_RAW != GND` and `USB_GND != GND` | Layer strategy, thermal relief, and current-return decision pending | Not configured / not claimed |
| Mechanical and manufacturing clearances | `TBD / pending Layout Preflight` | mm | Board outline, mounting features, connector access, and other mechanical objects that are actually present | Board outline, mounting holes, enclosure, and selected service pending | Not configured / not claimed |
| Package-specific fabrication details | `TBD / pending Layout Preflight` where applicable | mm or N/A | Only pads/packages with real solder-mask, paste, courtyard, height, thermal-pad, or assembly differences | Remaining footprint and assembly review pending | Not configured / not claimed |

## Planned Scope and Priority Work

- Establish the simplest maintainable default rules only after the fabricator, stackup, copper, and board-mechanical baseline are confirmed.
- Create Net Classes, Object Classes, explicit scopes, or higher-priority exception rules only where members share a real electrical, routing, manufacturing, mechanical, or verification behavior. Candidate groupings such as 24 V power, 3V3 power, USB data, `USB_GND`, PCB `GND`, and raw input nets are not claimed as configured classes.
- Keep `GND_IN_RAW` distinct from PCB `GND`; no rule, polygon, or class assignment may collapse this boundary around Q25.
- Keep `USB_GND` distinct from machine-side `GND`; any isolation-specific rule must have a precise Scope and higher Priority than an overlapping default rule when the user configures it.
- Define special rules only where actual current, voltage, return-path, differential, thermal, mechanical, or verification needs justify them.
- Do not mechanically expand Annular Ring, Mask, Paste, Silkscreen, Board-edge, or other rule categories unless the current Project facts, selected manufacturing path, package needs, or mechanical implementation make them applicable.
- The user must configure applicable rules in Altium Designer and manually confirm Scope coverage and Priority before formal placement approval. Documentation alone is not implementation evidence.

## Layout Preflight Open Items

- Confirm exact board/hardware revision and traceable relationship among `.SchDoc`, current PDF/BOM, and the target `.PcbDoc`.
- Confirm fabricator/service, official capability source, material, layer count, finished thickness, copper weight, assembly side(s), and controlled-impedance intent.
- Freeze board outline, mounting holes, enclosure constraints, connector orientation, insertion paths, and wiring/debug access.
- Verify remaining critical footprints, polarity, Pin 1, pad mapping, thermal-pad, courtyard, height, solder-mask, and paste requirements in Altium. The closed Q25 mapping is not a claim that all other footprints are verified.
- Select only applicable rule values/settings with stated units, basis, Scope, and Priority. Known candidates include clearance, width, via/hole, USB routing, polygon/plane strategy, 24 V/protection-domain constraints, isolation-domain constraints, buck layout constraints, and any package/manufacturing/mechanical rules made applicable by the selected stackup, service, footprints, board outline, or mounting features.
- Have the user configure and manually check the applicable Altium rules, Scope, and Priority.

## Current Layout Preflight Conclusion

**Stage 5 Layout Preflight may proceed. Formal placement/layout approval is pending the open items above.** Initial DRC is not required for Layout Preflight entry, and no DRC status is recorded.
