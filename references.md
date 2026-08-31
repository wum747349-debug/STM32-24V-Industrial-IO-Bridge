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
| CM35 official I/O pages | 用户在本轮提供/确认的官方资料页面 | User-provided Official-Manual Evidence | Reviewed for Stage-2 topology：pull-to-24G active、input filtering ≥ about 2 ms、OUT sinking connection、V/G isolated I/O power domain；exact electrical parameters absent | Conversation/session evidence；raw local PDF is untracked and is not claimed as archived by this commit |
| M3 Altium schematic screenshot | 用户在当前 Stage-3 会话提供的 M3 schematic screenshot | Current-session EDA Evidence | Reviewed for USB-C / USBLC6 / CH340C / ISO7721 connections and domain separation；supports module `CLOSEOUT ACCEPTABLE` only | Conversation record；`.SchDoc` is not parsed or modified by this documentation sync |

Legacy schematic 与 BOM 不自动成为本项目 EDA authority。用户已明确授权复用上一代 MOSFET level-conversion idea；Stage 2 仍以当前器件 official data 重新 qualification，Stage 3 新 `.SchDoc` 才是 implementation authority。

## Official Technical Sources

| Item / Module | Official source | Key facts used | Review Status |
| --- | --- | --- | --- |
| STM32F103C8T6 | STMicroelectronics STM32F103C8 product / datasheet / reference manual | 2.0–3.6 V device family、72 MHz、LQFP-48 option、minimum-system and GPIO/USART/SWD resources | Stage 2 core selection reviewed；M2 Stage-3 implementation decisions recorded, current-session closeout acceptable |
| LMR36510FADDAR | [Texas Instruments LMR36510 product / datasheet](https://www.ti.com/product/LMR36510) | 4.2–65 V input、1 A synchronous buck、400 kHz FPWM orderable option、application and external-component guidance | Reviewed for Primary selection；M1 Stage-3 external implementation recorded, remaining validation bounded |
| SWPA6045S220MT | [Sunlord SWPA Series official datasheet](https://www.sunlordinc.com/uploads/files/20221122/SWPA%20series%20of%20SMD%20Power%20Inductor.pdf) | 22 µH ±20%；DCR 116 mΩ max / 89 mΩ typ；Isat 2.05 A min / 2.20 A typ；Irms 1.80 A max / 2.00 A typ；SWPA6045 = 6 × 6 × 4.5 mm shielded construction | Manufacturer technical source reviewed for M1 L1 decision；end-application thermal/current verification remains |
| LMR36520FADDAR | [Texas Instruments LMR36520 product / datasheet](https://www.ti.com/product/LMR36520) | 4.2–65 V、2 A、400 kHz FPWM、DDA-8；TI states pin compatibility with LMR36510 | Qualified electrical scaling Alternate；purchase-time sourcing recheck required |
| STPS2H100A | STMicroelectronics STPS2H100 product / datasheet | 100 V / 2 A Schottky rectifier、SMA package | Reviewed for series reverse-polarity Primary |
| SMBJ30A-TR | STMicroelectronics SMBJxxA/CA datasheet | 30 V stand-off；600 W class 10/1000 µs TVS；clamp behavior depends on surge waveform/current | Reviewed for Primary selection; system surge margin calculation pending |
| 2N7002,215 | [Nexperia 2N7002 product / datasheet](https://www.nexperia.com/product/2N7002) | 60 V / 300 mA N-MOSFET、logic-level drive、logic-level translator application | Reviewed for legacy-conversion Primary；no exact qualified Alternate currently selected |
| USB Type-C receptacle / CC termination | [USB-IF USB Type-C® Cable and Connector Specification — Document Library](https://www.usb.org/documents?search=usb+type+c) | Official Type-C receptacle / role / CC termination authority；USB 2.0 device/sink baseline uses independent Rd on CC1 and CC2 | Stage 3 M3 `5.1 kΩ` Rd on each CC line reviewed；USB-IF Release 2.5 is current at this review and should be rechecked if Type-C role or power behavior changes |
| ISO7721DR | [Texas Instruments ISO7721 product / datasheet](https://www.ti.com/product/ISO7721) | dual-channel digital isolator、1 forward + 1 reverse、2.25–5.5 V supplies、non-F default-HIGH behavior、independent side supplies | Stage 3 exact M3 side assignment、UART direction、decoupling and intended power-off behavior reviewed；current-session closeout acceptable |
| ISO6721BDR | [Texas Instruments ISO6721 product / datasheet](https://www.ti.com/product/ISO6721) | dual-channel 1 forward + 1 reverse、default HIGH、2.25–5.5 V plus 1.8 V support、SOIC-8；basic-isolation class | Qualified cost-focused Alternate only while Project has no reinforced-isolation requirement；substitution must preserve M3 power-state behavior |
| CH340C | [WCH CH340 official datasheet/download page](https://www.wch-ic.com/downloads/CH340DS1_PDF.html) | USB-to-UART、5 V supply option、V3 decoupling behavior、internal clock variant、SOP-16、USB/UART pins | Stage 3 M3 VCC/V3、D+/D-、TXD/RXD and unused-pin implementation reviewed；current-session closeout acceptable |
| USBLC6-2SC6 | [STMicroelectronics USBLC6-2 official datasheet](https://www.st.com/resource/en/datasheet/usblc6-2.pdf) | 2-line USB 2.0 high-speed ESD protection、I/O1/I/O2 feed-through pin topology、VBUS/GND connection、low line capacitance | Stage 3 M3 exact line/VBUS/GND connection reviewed；current-session closeout acceptable |
| AN-LS18-40-N | User-provided manual; manufacturer provenance not yet confirmed | DC 10–30 V、NPN NO+NC、≤10 mA static current、NO/NC wiring、200 mA max output-load statement | Technical content available; manufacturer authority not confirmed |
| CM35 controller | User-provided official-manual pages | Input pull-to-24G active；anti-interference filtering with ≥about 2 ms signal duration；OUT load between +24 V and output confirms sinking behavior；V/G is isolated I/O supply and is recommended isolated from controller 24V/0V | Stage-2 topology reviewed；exact threshold/current/VOL/leakage remain Stage-3 inputs |
| F1 one-time fuse | [Littelfuse 468 Series datasheet](https://www.littelfuse.com/assetdocs/fuse-468-datasheet?assetguid=6b7857dc-f79c-4aae-8bcc-a9ef11ddef09) | 0468.500NRHF：0.5 A、63 V、1206 Slo-Blo、50 A interrupt at 63 VAC/VDC；25% continuous derating plus temperature re-rating | Reviewed for Primary；final startup/local-temperature check remains Stage 3 |
| F1 resettable Alternate | [Littelfuse 1210L Series PPTC datasheet](https://www.littelfuse.com/assetdocs/resettable-ptcs-1210l-datasheet?assetguid=b3a2be92-83a1-491d-9c6d-dc64451de047) | 1210L035/60PR：0.35 A hold / 0.70 A trip at 20°C、60 V、10 A；hold falls to 0.21 A at 70°C、R1max 1.5 Ω | Alternate architecture only；temperature/heating/residual-current limitations prevent Primary selection |

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
| Input fuse | Littelfuse 0468.500NRHF | C206993 | Listing re-confirmed during 2026-08-30 closeout | Supplier listing confirms MPN/package only；technical qualification uses Littelfuse datasheet |
| PPTC Alternate | Littelfuse 1210L035/60PR | C28661880 | Listing found during 2026-08-30 closeout；availability not frozen | Temperature-dependent hold behavior limits application |
| Buck output inductor | Sunlord SWPA6045S220MT | C83454 | Listing confirmed for the user-frozen L1 selection | Procurement/package evidence only；electrical qualification uses Sunlord official SWPA datasheet |

## Evidence Interpretation Notes

- User measurement of the existing PSU at approximately 24 V is Measured Evidence for the present operating point only. It does not prove regulation tolerance、ripple、surge waveform、OVP threshold or long-term stability.
- The product image for `MS-120-24` is not treated as a manufacturer official datasheet; its 24 V / 5 A / 120 W marking is used only as user-provided equipment identification evidence.
- The external PSU 5 A capability must not be used as the PCB input fuse/current-limit value. Board protection is sized from the board load budget and fault-energy boundary.
- The earlier requirements wording that described legacy CM35 readback as optocoupler-based conflicted with the archived schematic. Stage 2 inspection supports a 2N7002 MOSFET conversion baseline, and `requirements.md` has been corrected accordingly.
- The user-provided CM35 official-manual evidence is sufficient for Stage-2 topology qualification but not for exact electrical parameter claims. A local CM35 PDF present during this work remains untracked and is not represented as repository-archived evidence.
- The current-session M3 screenshot is EDA evidence for the visible connections only. It does not prove the underlying `.SchDoc` object model, footprints, ERC, PCB isolation geometry, enumeration, powered/unpowered behavior, or measured isolation performance.

## Missing Evidence / Remaining Qualification

| Topic | Required Source | Decision Blocked | Priority | Evidence State |
| --- | --- | --- | --- | --- |
| STM32 minimum-system details | ST datasheet/reference manual/application notes | Later formal schematic review and EDA implementation verification | High; needed by Stage 4 | M2 decisions recorded and current-session closeout acceptable；no `.SchDoc` parsing or ERC claim |
| CM35 exact I/O electrical parameters | CM35 official manual/datasheet pages containing threshold/current/VOL/leakage | Exact resistor、RC、ESD/transient/current-limiting and domain implementation | High; needed by Stage 3 and formal review | Topology closed；exact parameters open |
| AN-LS18-40-N manufacturer provenance | Manufacturer official datasheet or confirmed provenance of archived manual | Final sensor input protection/current/filter design | High; needed by Stage 3 | Manual content reviewed; authority open |
| External PSU official tolerance/surge data | Manufacturer official datasheet if obtainable | Required only for tighter PSU-specific or compliance-level surge claims | Medium | User nominal image + ≈24 V measurement available; official spec absent |
| Mechanical envelope | Enclosure, board size, mounting and wiring constraints | Final USB/terminal mechanical selection and PCB outline | High; freeze before Stage 5 | Open；TYPE-C-31-M-12 remains mechanical-conditional |
| M3 implementation validation | Current schematic PDF/BOM/EDA evidence plus later hardware test | ERC/footprint completeness、USB enumeration、UART communication、independent power sequencing、PCB isolation geometry、EMC/ESD | High before applicable later gates | M3 current-session screenshot reviewed；module design closeout acceptable, validation remains open |
| Detailed board power validation | Exact capacitor MPN/DC-bias data、startup/inrush evidence、thermal and layout evidence | F1 startup coordination、capacitor qualification、thermal and switch-current-loop verification | High; needed before the applicable later gates | M1 connections and L1 decision recorded；current-session module closeout acceptable；validation evidence remains open |
