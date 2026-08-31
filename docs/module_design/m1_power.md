# M1 — 24 V Input / Protection / 3.3 V Power

## Module Status and Boundary

- Responsibility: accept machine 24 V, provide overcurrent and reverse-polarity protection, establish `24V_PROTECTED`, suppress transients, and generate the machine-side `3V3` rail.
- Current Stage-3 conclusion: **CLOSEOUT ACCEPTABLE** for module design / current-session EDA capture reviewed by the user with ChatGPT.
- This record does not claim `.SchDoc` parsing, pin/footprint verification, ERC PASS, measured startup, surge compliance, Stage 3 completion, Stage 4 PASS, or PCB Layout approval.

## Structured Connection Facts

```text
P1 WJ500V-5.08-2P pin 1 -> 24V_IN
P1 WJ500V-5.08-2P pin 2 -> GND
24V_IN -> F1 0468.500NRHF -> D1 STPS2H100A anode
D1 cathode -> 24V_PROTECTED
D2 SMBJ30A-TR cathode -> 24V_PROTECTED
D2 anode -> GND

U2 LMR36510FADDAR PGND / EP -> GND
U2 VIN / EN -> 24V_PROTECTED
U2 PG -> intentionally open
C11 2.2 uF / 100 V / X7R: 24V_PROTECTED <-> GND
C12 220 nF / 100 V / X7R: 24V_PROTECTED <-> GND
C13 1 uF / X7R / >=16 V: U2 VCC <-> GND
C14 100 nF / X7R / >=16 V: U2 BOOT <-> SW_NODE
U2 SW -> SW_NODE -> L1 SWPA6045S220MT -> 3V3
3V3 -> R37 100 kohm / 1% -> U2 FB -> R38 43.2 kohm / 1% -> GND
C15 / C16 / C17, each 22 uF / X7R: 3V3 <-> GND
```

P1 is the current capture choice, not final enclosure/mechanical approval. No additional mandatory large input bulk capacitor is fitted or selected; a possible future DNP footprint is not part of the present baseline.

## Key Parameter Decisions

- Output target: 3.3 V. The `100 kΩ / 43.2 kΩ` divider is the current 1% baseline.
- L1 is frozen as Sunlord `SWPA6045S220MT`, LCSC `C83454`, 22 µH ±20%, shielded SMD power inductor, approximately 6 × 6 × 4.5 mm.
- Sunlord official SWPA data lists DCR 116 mΩ max / 89 mΩ typ, saturation current 2.05 A min / 2.20 A typ, and heat-rating current 1.80 A max / 2.00 A typ. Manufacturer data is the electrical authority; LCSC is procurement evidence.
- Exact capacitor MPNs and output-capacitor DC-bias performance are not frozen by this record.

## Engineering Basis and Interfaces

- The protection order keeps F1 ahead of the series reverse-polarity diode and places the unidirectional TVS on `24V_PROTECTED` with cathode to the protected rail.
- `EN` tied to `24V_PROTECTED` establishes always-on behavior when protected input power is present; `PG` is intentionally unused.
- Outputs are `24V_PROTECTED` for field/interface loads and `3V3` for M2 and machine-side logic.
- Follow TI placement guidance during layout: minimize the VIN/PGND input loop, SW/BOOT loop, and output switching-current loop; keep FB sensing away from `SW_NODE`.

## Remaining Validation

- Full-board startup/inrush and F1 time-current coordination are unmeasured.
- Exact capacitor DC-bias/capacitance, diode loss, ripple, and thermal behavior remain to be checked as applicable.
- PCB placement/routing has not started; switch-current-loop layout is not verified.
- No source-impedance, surge-waveform, IEC, or other compliance result is claimed.
