# PCB Review

Document Status: **STAGE 5 PLACEMENT PASS / CLOSED — STAGE 6 ROUTING ACTIVE**

Project Stage: **Stage 6 — Routing and Copper**

## Review Scope

This record captures the current full-board PCB placement closeout and the routing-entry boundary. It is based on the user-provided Altium Designer full-board placement screenshots, including the final full-board Ratsnest view after the board-width reduction.

This review does **not** claim routed-copper correctness, DRC PASS, Gerber/manufacturing release, assembly fit, hardware test, EMC/surge compliance, or `.PcbDoc` object-level parsing.

## Stage 5 Closed Mechanical Baseline

- Board outline: **100 mm × 80 mm**.
- Corner treatment: **R3 mm**.
- Mounting: **4 × M3 NPTH**, 3.20 mm drill, No Net.
- Mounting-hole copper/mechanical exclusion: approximately **Ø7.0 mm solid Keepout Region** around each mounting hole.
- The previous 110 mm × 80 mm working outline was reduced to 100 mm × 80 mm before routing, mainly by tightening the right-side placement and moving the right-side mounting-hole baseline inward.
- Further width reduction is not recommended before routing because the remaining central/right-side open area is useful routing, power-distribution and copper-return space rather than clearly valueless mechanical blank area.

## Full-board Placement Review

### MCU and Minimum System

- U1 STM32F103C8T6 remains near the board center with usable escape space on all sides.
- The reviewed local placement for VDD/VSS decoupling, VDDA/VSSA support, HSE crystal/load capacitors, NRST, RESET and BOOT0 is retained.
- No full-board evidence justifies a large re-placement of the MCU minimum-system cluster before routing.

### CM35 I/O Physical Topology

The current board relationship is:

```text
left side:
CN6 = CM35 IN11–IN18
CN6 -> IN11–IN18 circuitry -> STM32

right side:
CN5 = CM35 OUT1–OUT8
STM32 -> OUT1–OUT8 circuitry -> CN5
```

This mapping is the current placement/routing baseline and supersedes earlier reversed connector wording in stale documentation.

The final Ratsnest review did not show a full 8-channel group placed on the wrong side of the MCU or a placement-driven cross-board routing blocker. The IN and OUT arrays are therefore locked for Stage 6 unless later routing evidence demonstrates a real blocker.

### Sensor Interfaces

- `CN1`–`CN4` remain Sensors 1–4, each serving NO + NC acquisition through its associated frontend.
- Their current edge placement and local frontend grouping use the available MCU GPIO fanout directions without a full-board placement blocker.
- M5 placement is accepted and locked for routing unless later evidence shows a real conflict.

### USB / UART / Isolation

The top-center sequence remains physically coherent:

```text
USB-C
-> USB protection
-> CH340C
-> ISO7721
-> STM32
```

The placement is accepted. Stage 6 must preserve the isolation boundary and must not bridge `USB_GND` to machine-side `GND` with tracks, vias, polygons, mounting features, shield paths or other copper objects.

### 24 V Power

The lower-left M1 placement remains physically coherent around:

```text
P1
-> input / reverse-polarity protection
-> LMR36510 buck
-> 3V3
```

The power placement is accepted. Stage 6 must keep the high-current / switching loops compact, prevent `GND_IN_RAW` from bypassing Q25 into PCB `GND`, keep the `SW_NODE` region local, and keep ordinary signals away from the sensitive buck switching area unless a justified return-path plan exists.

## Ratsnest / Routing-corridor Review

- The final full-board Ratsnest shows many expected MCU fanout lines but no placement-level blocker requiring another full-board re-layout.
- Left-side CN6 / IN11–IN18 connectivity converges toward U1 in the expected direction.
- Right-side U1 / OUT1–OUT8 connectivity converges toward the CN5-side output array in the expected direction.
- Sensor and support-interface connections retain usable corridors.
- The 100 mm width leaves sufficient routing / via / power-distribution / GND-copper space for Stage 6; further compression would reduce routing freedom without a demonstrated mechanical requirement.

## Findings

### Blockers

**NONE** from the reviewed Stage 5 placement evidence.

### Recommended Before / During Routing

- Keep the current 100 mm × 80 mm placement baseline locked unless routed evidence shows a genuine blocker.
- Route incrementally and review dense groups rather than moving modules to eliminate visual Ratsnest crossings.
- Preserve the Q25 raw-return boundary and ISO7721 ground-domain boundary through all routing and copper work.

### Minor / Later Mechanical Note

- `CN5` versus the bottom-right M3 screw/head/washer and removable-plug envelope should be checked later with 3D / courtyard / real mechanical evidence when convenient.
- This is **not** a Stage 6 blocker based on the current 2D evidence.

## Stage 6 Entry Strategy

Current working order:

```text
critical / module-local networks
-> MCU fanout / escape
-> inter-module signals
-> power distribution
-> GND / copper / stitching
```

Routing should be performed interactively in small groups with Altium screenshots / net highlighting used as evidence where useful.

## Conclusion

```text
Stage 5 — PCB Placement:
PASS / CLOSED

Board baseline:
100 × 80 mm, R3, 4 × M3 NPTH + keepouts

Placement blockers:
NONE

PCB width reduction:
110 mm -> 100 mm ACCEPTED
Further reduction before routing: NOT RECOMMENDED

Stage 6 — Routing and Copper:
READY / ACTIVE
```
