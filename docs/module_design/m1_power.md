# M1 — 24 V Input / Protection / 3.3 V Power

## Module Status and Boundary

- Responsibility: accept machine 24 V, provide overcurrent and reverse-polarity protection, establish `24V_PROTECTED`, suppress transients, and generate the machine-side `3V3` rail.
- Current Stage-4 M1 review disposition: reverse-polarity correction **MODIFIED / PENDING FINAL EDA VERIFICATION**; the current-session schematic screenshot visually supports the topology, while Q25 symbol-to-footprint pad mapping remains pending.
- This record does not claim `.SchDoc` parsing, pin/footprint verification, ERC PASS, measured startup, surge compliance, Stage 3 completion, Stage 4 PASS, or PCB Layout approval.

## Structured Connection Facts

```text
P1 WJ500V-5.08-2P positive input -> 24V_IN_RAW
P1 WJ500V-5.08-2P negative input -> GND_IN_RAW
24V_IN_RAW -> F1 0468.500NRHF -> D1 STPS2H100A anode
D1 cathode -> 24V_PROTECTED
Q25 DMT10H015LFG-13 Drain -> GND_IN_RAW
Q25 Source -> PCB GND
R65 10 kohm: 24V_IN_RAW -> Q25 Gate
R66 100 kohm: Q25 Gate -> Q25 Source / PCB GND
D12 MMSZ5242B-7-F cathode -> Q25 Gate
D12 anode -> Q25 Source / PCB GND
D2 SMBJ30A-TR cathode -> 24V_PROTECTED
D2 anode -> GND

U2 LMR36510FADDAR PGND / EP -> GND
U2 VIN / EN -> 24V_PROTECTED
U2 PG -> intentionally open
C11 2.2 uF / 100 V / X7R: 24V_PROTECTED <-> GND
C12 220 nF / 100 V / X7R: 24V_PROTECTED <-> GND
C13 1 uF / X7R / >=16 V: U2 VCC <-> GND
U2 BOOT capacitor -> SW_NODE
U2 SW -> SW_NODE -> L1 SWPA6045S220MT -> 3V3
3V3 -> R37 100 kohm / 1% -> U2 FB -> R38 43.2 kohm / 1% -> GND
C14 / C15 / C16, each Samsung CL31B226KPHNNNE / LCSC C87996 / 22 uF / 10 V / X7R / 1206: 3V3 <-> GND
```

P1 is the current capture choice, not final enclosure/mechanical approval. No additional mandatory large input bulk capacitor is fitted or selected; a possible future DNP footprint is not part of the present baseline.

## Key Parameter Decisions

- Output target: 3.3 V. The `100 kΩ / 43.2 kΩ` divider is the current 1% baseline.
- L1 is frozen as Sunlord `SWPA6045S220MT`, LCSC `C83454`, 22 µH ±20%, shielded SMD power inductor, approximately 6 × 6 × 4.5 mm.
- Sunlord official SWPA data lists DCR 116 mΩ max / 89 mΩ typ, saturation current 2.05 A min / 2.20 A typ, and heat-rating current 1.80 A max / 2.00 A typ. Manufacturer data is the electrical authority; LCSC is procurement evidence.
- C14/C15/C16 are frozen as Samsung `CL31B226KPHNNNE`, LCSC `C87996`, 22 uF, 10 V, X7R, 1206. Effective capacitance under DC bias remains a validation item.

## Engineering Basis and Interfaces

- The accepted protection architecture keeps `24V_IN_RAW -> F1 -> STPS2H100A -> 24V_PROTECTED` on the positive rail and inserts Q25 in the negative return between `GND_IN_RAW` and PCB `GND`.
- R65 turns Q25 on for correct polarity, R66 provides gate-source bias, and D12 is the Q25 gate-source clamp. `GND_IN_RAW` is not PCB `GND` and must not bypass Q25.
- `EN` tied to `24V_PROTECTED` establishes always-on behavior when protected input power is present; `PG` is intentionally unused.
- Outputs are `24V_PROTECTED` for field/interface loads and `3V3` for M2 and machine-side logic.
- Follow TI placement guidance during layout: minimize the VIN/PGND input loop, SW/BOOT loop, and output switching-current loop; keep FB sensing away from `SW_NODE`.

## Remaining Validation

- Full-board startup/inrush and F1 time-current coordination are unmeasured.
- C14/C15/C16 effective capacitance under DC bias, diode/MOSFET loss, ripple, and thermal behavior remain to be checked as applicable.
- Independently verify Q25 schematic-symbol Drain/Gate/Source pin numbering against the selected footprint pad mapping before final Stage 4 closure; the screenshot does not prove this mapping.
- PCB placement/routing has not started; switch-current-loop layout is not verified.
- No source-impedance, surge-waveform, IEC, or other compliance result is claimed.
