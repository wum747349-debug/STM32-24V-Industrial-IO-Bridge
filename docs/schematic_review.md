# Schematic Review

Review Status: **PASS / CLOSED — POST-REVIEW CORRECTIVE DELTAS RECORDED**

Final Stage 4 review conclusion remains: **可以进入 PCB Layout**. Stage 4 Formal Schematic Review is historically closed. During Stage 6 final PCB review, two schematic implementation defects were identified, corrected by the user in Altium, and visually re-reviewed on 2026-09-04. These later corrections are recorded below without claiming a new full-board ERC or complete Stage 4 rerun.

## Evidence Boundary

- Stage 4 closeout evidence remains the archived complete schematic PDF and BOM in `hardware/outputs/`.
- 2026-09-04 corrective evidence consists of user-provided current Altium schematic screenshots showing the corrected U2 LMR36510 EN/PG connections and corrected U3 CH340C TXD/RXD net mapping.
- User confirmation that Q25 schematic symbol D/G/S ↔ PowerDI3333-8 footprint pads ↔ manufacturer pinout was finally checked in Altium.
- Evidence boundary: no ERC claim, no hardware-test claim, no EMC/surge compliance claim, and no `.SchDoc` parser claim. The targeted corrective checks do not assert a broader full-board footprint-mapping or schematic PASS beyond the documented review scope.

## Findings

| ID | Module | Finding / disposition | Risk | Status | Evidence / remaining check |
| --- | --- | --- | --- | --- | --- |
| SR-M1-001 | M1 reverse-polarity protection | Positive path is `24V_IN_RAW -> F1 -> D9 STPS2H100A -> 24V_PROTECTED`. Negative path is `GND_IN_RAW -> Q25 DMT10H015LFG-13 -> PCB GND`; R65 10 kΩ connects `24V_IN_RAW` to Gate, R66 100 kΩ connects Gate to Source / PCB GND, and D12 `MMSZ5242B-7-F` has Cathode at Gate and Anode at Source / PCB GND. `GND_IN_RAW` must remain isolated from PCB `GND` except through Q25. | High | **CLOSED** | User completed the final Q25 D/G/S ↔ PowerDI3333-8 pads ↔ manufacturer pinout check in Altium. |
| SR-M1-002 | M1 buck output capacitors | C14/C15/C16 are Samsung `CL31B226KPHNNNE`, LCSC `C87996`, 22 uF, 10 V, X7R, 1206. | Medium | **CLOSED** | Current BOM and module records synchronized. |
| SR-M1-003 | M1 LMR36510 control pins | Stage 6 review found U2 `EN` and `PG` previously floating in the current schematic implementation. The user corrected `EN -> 24V_PROTECTED` and unused `PG -> GND`. | High | **CLOSED — CORRECTED 2026-09-04** | Current Altium screenshot evidence visually confirms both corrected connections. No ERC PASS is claimed. |
| SR-M3-001 | M3 CH340C ↔ ISO7721 UART direction | Stage 6 review found the CH340C TXD/RXD net names reversed at U3, which would have produced output-to-output / input-to-input pairing against the ISO7721 channel directions. The user corrected `U3 pin 2 TXD -> CH340_TX` and `U3 pin 3 RXD <- CH340_RX`, preserving the already-correct ISO7721 side mapping. | High | **CLOSED — CORRECTED 2026-09-04** | Current Altium screenshot evidence confirms the U3 correction. The intended path is `CH340 TXD -> ISO7721 INB -> OUTB -> MCU RX` and `MCU TX -> ISO7721 INA -> OUTA -> CH340 RXD`. No ERC or hardware UART test is claimed. |
| SR-M45-001 | M4/M5 2N7002 | LCSC `C7420321` is intentionally retained from the previous working board and is accepted for the present low-current level-translation application. Earlier Nexperia `2N7002,215` qualification remains useful reference history, not a mandatory replacement requirement. | Low | **ACCEPTED / DOCUMENTATION SYNCED** | Project decision and previous-board working evidence; normal purchase-time identity and footprint checks still apply. |

## Closed Q25 Mapping Record

The user completed the final Altium check that the Q25 schematic symbol Drain/Gate/Source mapping agrees with the selected PowerDI3333-8 footprint pads and manufacturer pinout. SR-M1-001 is closed. PCB implementation must preserve this mapping, and no copper, port, harness definition, or footprint connection may bypass Q25 from `GND_IN_RAW` into PCB `GND`.

## Post-Review Corrective Delta — 2026-09-04

Two targeted corrections were made after the historical Stage 4 closeout:

```text
M1 / U2 LMR36510
EN -> 24V_PROTECTED
PG -> GND (unused PG; not left floating)

M3 / U3 CH340C
TXD -> CH340_TX
RXD <- CH340_RX

ISO7721 direction retained:
CH340_TX -> INB -> OUTB -> MCU_UART_RX
MCU_UART_TX -> INA -> OUTA -> CH340_RX
```

These corrections were made before final PCB manufacturing preparation and were propagated into the PCB connectivity by the user. They remove the two functional blockers identified during Stage 6 review. Because the review evidence is targeted screenshot evidence rather than a complete exported ERC report, the repository still does not claim full ERC PASS.

## Conclusion

Stage 4 Formal Schematic Review remains **PASS / CLOSED** as the historical gate, with the 2026-09-04 post-review corrective deltas now explicitly documented and closed. The current engineering review has no known remaining schematic blocker from these two findings. No ERC PASS, broader full-board footprint-mapping PASS, hardware-test PASS, USB/UART functional-test PASS, or EMC/surge compliance PASS is recorded; no `.SchDoc` parser claim is made.