# Reference Index

关键参数必须回到 official manufacturer datasheet、reference manual 或 application note 核对。商品页只用于采购与装配信息，不能替代官方技术证据；Legacy Project 资料只作为本 Project 的参考和既有功能证据。

## Project Inputs and Legacy Evidence

| Item | Source | Role | Current State | Local Path or Link |
| --- | --- | --- | --- | --- |
| Project initialization brief | 用户在 2026-08-29 提供的任务说明 | Requirements / interface contract fact input | Reviewed | Conversation record; no local file |
| Previous-generation schematic PDF | 用户提供的上一代原理图 | Legacy Design Reference / Existing Functional Evidence；不是本项目 EDA authority | Stage 2 technical comparison performed；确认主要 24 V ↔ 3.3 V conversion 使用 2N7002 MOSFET networks；legacy power 使用 XL7005A | [references/旧原理图.pdf](references/旧原理图.pdf) |
| Previous-generation BOM spreadsheet | 用户提供的上一代 BOM | Legacy Design Reference；旧器件仍需重新 qualification | Archived; full BOM comparison not performed | [references/旧BOM表.xlsx](references/旧BOM表.xlsx) |
| AN-LS18-40-N photoelectric sensor manual | 用户提供的使用说明书 | External Device Reference | Archived; technical content reviewed for Stage 2, manufacturer provenance still open | [references/激光漫反射光电开关使用说明书.pdf](references/激光漫反射光电开关使用说明书.pdf) |
| Existing 24 V PSU photo + user measurement | 用户在 2026-08-29 会话提供的产品图片和万用表测量 | Current power-source operating-point evidence | Product image shows `MS-120-24`, nominal 24 V / 5 A / 120 W；user measured output ≈24 V and observed stable | Conversation record; no repository file |

Legacy schematic 与 BOM 不自动成为本项目 EDA authority。用户已明确授权复用上一代 MOSFET level-conversion idea；Stage 2 仍以当前器件 official data 重新 qualification，Stage 3 新 `.SchDoc` 才是 implementation authority。

## Official Technical Sources

| Item / Module | Official source | Key facts used in Stage 2 | Review Status |
| --- | --- | --- | --- |
| STM32F103C8T6 | STMicroelectronics STM32F103C8 product / datasheet / reference manual | 2.0–3.6 V device family、72 MHz、LQFP-48 option、GPIO/USART/SWD resource class | Stage 2 core selection reviewed; Stage 3 minimum-system details pending |
| LMR36510FADDAR | Texas Instruments LMR36510 datasheet Rev. B / product page | 4.2–65 V input、1 A synchronous buck、400 kHz FPWM orderable option、high-voltage transient protection features | Reviewed for Primary selection; external-component calculation pending |
| STPS2H100A | STMicroelectronics STPS2H100 product / datasheet | 100 V / 2 A Schottky rectifier、SMA package | Reviewed for series reverse-polarity Primary |
| SMBJ30A-TR | STMicroelectronics SMBJxxA/CA datasheet | 30 V stand-off；600 W class 10/1000 µs TVS；clamp behavior depends on surge waveform/current | Reviewed for Primary selection; system surge margin calculation pending |
| 2N7002,215 | Nexperia 2N7002 product / datasheet | 60 V / 300 mA N-MOSFET、logic-level drive、logic-level translator application | Reviewed for legacy-conversion Primary |
| ISO7721DR | Texas Instruments ISO7721 product / datasheet | dual-channel digital isolator、1 forward + 1 reverse、2.25–5.5 V supplies、default output HIGH option | Reviewed for UART-isolation Primary |
| CH340C | WCH CH340 datasheet / official download page | USB-to-UART、3.3/5 V supply、internal clock variant、SOP-16 | Reviewed for Stage 2 Primary; exact pin/power-state implementation pending |
| USBLC6-2SC6 | STMicroelectronics USBLC6-2 product / datasheet | 2-line USB 2.0 high-speed ESD protection、low line capacitance | Reviewed for USB ESD Primary |
| AN-LS18-40-N | User-provided manual; manufacturer provenance not yet confirmed | DC 10–30 V、NPN NO+NC、≤10 mA static current、NO/NC wiring、200 mA max output-load statement | Technical content available; manufacturer authority not confirmed |
| CM35 controller | Official I/O manual / electrical specification | Required for exact IN/OUT threshold/current/protection qualification | Not collected |

## Procurement Sources — LCSC / JLCPCB

Point-in-time supplier observations must be rechecked before purchasing / PCBA submission.

| Function | Manufacturer / MPN | LCSC C# | Procurement State on 2026-08-29 | Technical Limitation |
| --- | --- | --- | --- | --- |
| MCU | ST STM32F103C8T6 | C8734 | Listing confirmed | Supplier page does not replace ST datasheet |
| USB-UART | WCH CH340C | C84681 | Good / listed with substantial stock during check | Supplier data does not replace WCH datasheet |
| UART isolation | TI ISO7721DR | C366164 | Listing confirmed | Supplier data does not replace TI datasheet |
| USB ESD | ST USBLC6-2SC6 | C7519 | Listing confirmed | Supplier data does not replace ST datasheet |
| USB-C receptacle | Korean Hroparts Elec TYPE-C-31-M-12 | C165948 | Listing confirmed | Mechanical acceptance still depends on enclosure / board-edge constraints |
| MOSFET conversion | Nexperia 2N7002,215 | C65189 | Listing confirmed; multiple 2N7002 alternates exist | Exact alternate must preserve electrical + pin/package constraints |
| 24 V → 3.3 V | TI LMR36510FADDAR | C1858394 | Good / in stock during check | Supplier data does not replace TI design procedure |
| Reverse-polarity diode | ST STPS2H100A | C81548 | Listing confirmed | Final dissipation depends on board current budget |
| 24 V TVS | ST SMBJ30A-TR | C133663 | Good / in stock during check | Surge compliance cannot be inferred from supplier listing |

## Evidence Interpretation Notes

- User measurement of the existing PSU at approximately 24 V is Measured Evidence for the present operating point only. It does not prove regulation tolerance、ripple、surge waveform、OVP threshold or long-term stability.
- The product image for `MS-120-24` is not treated as a manufacturer official datasheet; its 24 V / 5 A / 120 W marking is used only as user-provided equipment identification evidence.
- The external PSU 5 A capability must not be used as the PCB input fuse/current-limit value. Board protection is sized from the board load budget and fault-energy boundary.
- The earlier requirements wording that described legacy CM35 readback as optocoupler-based conflicted with the archived schematic. Stage 2 inspection supports a 2N7002 MOSFET conversion baseline, and `requirements.md` has been corrected accordingly.

## Missing Evidence / Remaining Qualification

| Topic | Required Source | Decision Blocked | Priority | Evidence State |
| --- | --- | --- | --- | --- |
| STM32 minimum-system details | ST datasheet/reference manual/application notes | Stage 3 clock/reset/boot/SWD/VDDA implementation | High; needed by Stage 3 | Core MCU selection done; implementation review open |
| CM35 I/O electrical specification | CM35 official manual/datasheet | Exact input/output current, threshold, resistor and protection network qualification | High; needed by Stage 3 and formal review | Open |
| AN-LS18-40-N manufacturer provenance | Manufacturer official datasheet or confirmed provenance of archived manual | Final sensor input protection/current/filter design | High; needed by Stage 3 | Manual content reviewed; authority open |
| External PSU official tolerance/surge data | Manufacturer official datasheet if obtainable | Required only for tighter PSU-specific or compliance-level surge claims | Medium | User nominal image + ≈24 V measurement available; official spec absent |
| Mechanical envelope | Enclosure, board size, mounting and wiring constraints | Final USB/terminal mechanical selection and PCB outline | High; freeze before Stage 5 | Open |
| Final board load budget | Stage 3 circuit design and component currents | Exact input fuse/PTC rating、diode dissipation、buck thermal margin | High; needed before schematic closeout | Open |
