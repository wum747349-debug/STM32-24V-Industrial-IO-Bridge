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
| CM35 official I/O pages | 用户在当前工程会话提供的官方手册页面 | User-provided Official-Manual Evidence | Reviewed：`V/G` 明确定义为 isolated I/O 24 V positive/24G negative，`24V/0V` 为 controller system supply；手册建议 system 与 I/O 使用 isolated / non-common-ground switching supplies，示例使用两套 24 V switching supplies | Conversation/session evidence；当前本地 manual PDF 未跟踪，不声称已由本 commit 归档 |
| M3 Altium schematic screenshot | 用户在当前 Stage-3 会话提供的 M3 schematic screenshot | Current-session EDA Evidence | Reviewed for USB-C / USBLC6 / CH340C / ISO7721 connections and domain separation；supports module `CLOSEOUT ACCEPTABLE` only | Conversation record；`.SchDoc` is not parsed or modified by this documentation sync |
| M1 reverse-polarity schematic screenshot | 用户在当前 Stage-4 会话提供的 M1 schematic screenshot | Current-session EDA Evidence | Visually reviewed for `24V_IN_RAW` / `GND_IN_RAW`, Q25 `DMT10H015LFG-13`, R65/R66, D12 `MMSZ5242B-7-F`, and the retained positive path to `24V_PROTECTED`；supports `MODIFIED / PENDING FINAL EDA VERIFICATION` | Conversation record；does not prove `.SchDoc` objects, ERC, or Q25 symbol-to-footprint pad mapping |
| M4 Altium schematic screenshots | 用户在当前 Stage-3 会话提供的 M4 schematic screenshots | Current-session EDA Evidence | Visible 16-channel 2N7002 topology、`3V3` / `24V_PROTECTED` rails、mapping and safe-startup reviewed；supports M4 `CLOSEOUT ACCEPTABLE` only | Conversation record；does not prove `.SchDoc` objects、ERC、footprints、Stage 4 or PCB Layout |
| M5 complete 8-channel schematic screenshots | 用户在当前 Stage-3 会话提供的完整 M5 screenshots | Current-session EDA Evidence | Sensor 1–4 NO/NC 共 8 路 visible completeness reviewed：CN3–CN6、8 × 100 Ω、8 × SMF30A、8 × 2N7002、24 V-side / MCU-side pull-ups、`3V3` gates and GPIO mapping；supports M5 `CLOSEOUT ACCEPTABLE` | Conversation record；screenshot review does not prove `.SchDoc` objects、footprints、ERC、Stage 4、EMC/surge or hardware behavior |
| Stage 3 complete schematic PDF + current BOM | 用户于 2026-09-01 放入 `hardware/` 的同日导出件 | Stage-3 closeout evidence | Complete single-sheet schematic PDF visually covers M1–M5；current BOM is readable and includes the complete M5 population；supports `READY FOR SCHEMATIC REVIEW` | Local untracked files `hardware/SCH_Schematic1_2026-09-01.pdf` and `hardware/BOM_Board1_Schematic1_2026-09-01.xlsx`；not claimed as archived by this commit |

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
| 2N7002,215 | [Nexperia 2N7002 product / datasheet](https://www.nexperia.com/product/2N7002) | 60 V / 300 mA N-MOSFET、logic-level drive、logic-level translator application | Retained as useful qualification history/reference envelope；not a mandatory replacement for the accepted current C7420321 device |
| USB Type-C receptacle / CC termination | [USB-IF USB Type-C® Cable and Connector Specification — Document Library](https://www.usb.org/documents?search=usb+type+c) | Official Type-C receptacle / role / CC termination authority；USB 2.0 device/sink baseline uses independent Rd on CC1 and CC2 | Stage 3 M3 `5.1 kΩ` Rd on each CC line reviewed；USB-IF Release 2.5 is current at this review and should be rechecked if Type-C role or power behavior changes |
| ISO7721DR | [Texas Instruments ISO7721 product / datasheet](https://www.ti.com/product/ISO7721) | dual-channel digital isolator、1 forward + 1 reverse、2.25–5.5 V supplies、non-F default-HIGH behavior、independent side supplies | Stage 3 exact M3 side assignment、UART direction、decoupling and intended power-off behavior reviewed；current-session closeout acceptable |
| ISO6721BDR | [Texas Instruments ISO6721 product / datasheet](https://www.ti.com/product/ISO6721) | dual-channel 1 forward + 1 reverse、default HIGH、2.25–5.5 V plus 1.8 V support、SOIC-8；basic-isolation class | Qualified cost-focused Alternate only while Project has no reinforced-isolation requirement；substitution must preserve M3 power-state behavior |
| CH340C | [WCH CH340 official datasheet/download page](https://www.wch-ic.com/downloads/CH340DS1_PDF.html) | USB-to-UART、5 V supply option、V3 decoupling behavior、internal clock variant、SOP-16、USB/UART pins | Stage 3 M3 VCC/V3、D+/D-、TXD/RXD and unused-pin implementation reviewed；current-session closeout acceptable |
| USBLC6-2SC6 | [STMicroelectronics USBLC6-2 official datasheet](https://www.st.com/resource/en/datasheet/usblc6-2.pdf) | 2-line USB 2.0 high-speed ESD protection、I/O1/I/O2 feed-through pin topology、VBUS/GND connection、low line capacitance | Stage 3 M3 exact line/VBUS/GND connection reviewed；current-session closeout acceptable |
| AN-LS18-40-N | User-provided manual; manufacturer provenance not yet confirmed | DC 10–30 V、NPN NO+NC、≤10 mA static current、NO/NC wiring、200 mA max output-load statement | Technical content available; manufacturer authority not confirmed |
| CM35 controller | User-provided official-manual pages | Input pull-to-24G active；anti-interference filtering with ≥about 2 ms signal duration；OUT load between +24 V and output confirms sinking behavior；`V/G` = isolated I/O supply；`24V/0V` = system supply；isolated non-common-ground supplies are recommended and the example uses two 24 V switching supplies | Power-domain interpretation reviewed for Stage 3；exact internal isolation construction/rating and threshold/current/VOL/leakage are not inferred without explicit manual data |
| Littelfuse SMF30A | [Littelfuse SMF Series official datasheet](https://www.littelfuse.com/assetdocs/tvs-diodes-smf-datasheet?assetguid=7eb8a5b6-bdd0-4561-8f19-0c3cc6f9b2af) | Unidirectional `SMF30A`；SOD-123FL；`VRWM=30 V`；`VBR=33.3–36.8 V @ 1 mA`；maximum `VC=48.4 V @ 4.1 A` for 10/1000 µs；200 W class | Reviewed for M5 Stage-3 field-signal TVS baseline；system surge/EMC performance remains unverified |
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
| MOSFET conversion | 2N7002 current supplier listing | C7420321 | Intentionally retained from the previous working board for the current low-current level-translation application | Nexperia `2N7002,215` remains reference history, not a mandatory/current Primary replacement requirement；normal purchase-time identity and footprint checks still apply |
| Buck output capacitors C14/C15/C16 | Samsung CL31B226KPHNNNE, 22 uF / 10 V / X7R / 1206 | C87996 | Current selected output-capacitor record | Supplier identity does not replace DC-bias/effective-capacitance validation |
| 24 V → 3.3 V | TI LMR36510FADDAR | C1858394 | Good / in stock during check | Supplier data does not replace TI design procedure |
| Reverse-polarity diode | ST STPS2H100A | C81548 | Listing confirmed | Final dissipation depends on board current budget |
| 24 V TVS | ST SMBJ30A-TR | C133663 | Good / in stock during check | Surge compliance cannot be inferred from supplier listing |
| Input fuse | Littelfuse 0468.500NRHF | C206993 | Listing re-confirmed during 2026-08-30 closeout | Supplier listing confirms MPN/package only；technical qualification uses Littelfuse datasheet |
| PPTC Alternate | Littelfuse 1210L035/60PR | C28661880 | Listing found during 2026-08-30 closeout；availability not frozen | Temperature-dependent hold behavior limits application |
| Buck output inductor | Sunlord SWPA6045S220MT | C83454 | Listing confirmed for the user-frozen L1 selection | Procurement/package evidence only；electrical qualification uses Sunlord official SWPA datasheet |
| CM35 8P PCB header | Cixi Kefa Elec KF2EDGR-3.81-8P | C441188 | Listing confirmed on 2026-08-31 | Matching removable plug exact MPN and final mate/mechanical acceptance remain to be confirmed |
| Sensor 4P PCB header | Cixi Kefa Elec KF2EDGR-3.81-4P | C441184 | Listing confirmed on 2026-08-31 | Matching removable plug exact MPN and final mate/mechanical acceptance remain to be confirmed |
| Sensor field-signal TVS | Littelfuse SMF30A | C720060 | Exact Littelfuse listing and SOD-123FL package confirmed on 2026-08-31 | Supplier evidence does not replace Littelfuse official electrical data |

## Evidence Interpretation Notes

- User measurement of the existing PSU at approximately 24 V is Measured Evidence for the present operating point only. It does not prove regulation tolerance、ripple、surge waveform、OVP threshold or long-term stability.
- The product image for `MS-120-24` is not treated as a manufacturer official datasheet; its 24 V / 5 A / 120 W marking is used only as user-provided equipment identification evidence.
- The external PSU 5 A capability must not be used as the PCB input fuse/current-limit value. Board protection is sized from the board load budget and fault-energy boundary.
- The earlier requirements wording that described legacy CM35 readback as optocoupler-based conflicted with the archived schematic. Stage 2 inspection supports a 2N7002 MOSFET conversion baseline, and `requirements.md` has been corrected accordingly.
- The user-provided CM35 official-manual evidence is sufficient for Stage-2 topology qualification but not for exact electrical parameter claims. A local CM35 PDF present during this work remains untracked and is not represented as repository-archived evidence.
- The current-session M3 screenshot is EDA evidence for the visible connections only. It does not prove the underlying `.SchDoc` object model, footprints, ERC, PCB isolation geometry, enumeration, powered/unpowered behavior, or measured isolation performance.
- The current-session M4 and complete M5 screenshots support only the visible module implementation and module closeout boundaries. They do not prove `.SchDoc` objects、ERC、footprints、Stage 4、PCB Layout、EMC/surge compliance or hardware behavior.
- The current-session M1 screenshot supports the visible Q25 low-side reverse-polarity topology only. It does not prove Q25 symbol-to-footprint pad mapping; that exact mapping remains pending EDA verification before final Stage 4 closure.
- The 2026-09-01 schematic PDF and BOM are local, same-date Stage-3 review inputs and are not tracked by this documentation commit. Their presence supports Stage-3 readiness; it does not constitute Stage-4 review findings or PASS.

## Missing Evidence / Remaining Qualification

| Topic | Required Source | Decision Blocked | Priority | Evidence State |
| --- | --- | --- | --- | --- |
| STM32 minimum-system details | ST datasheet/reference manual/application notes | Later formal schematic review and EDA implementation verification | High; needed by Stage 4 | M2 decisions recorded and current-session closeout acceptable；no `.SchDoc` parsing or ERC claim |
| CM35 exact I/O electrical parameters | CM35 official manual/datasheet pages containing threshold/current/VOL/leakage | Later formal verification against exact external-device limits | High; needed by formal review | Rev.A two-PSU power domain and M4 module design closed；exact CM35 electrical parameters and internal isolation rating remain unavailable |
| AN-LS18-40-N manufacturer provenance | Manufacturer official datasheet or confirmed provenance of archived manual | Later formal verification against exact sensor output limits | High; needed by formal review | M5 per-channel baseline defined from available evidence；manufacturer authority remains open |
| External PSU official tolerance/surge data | Manufacturer official datasheet if obtainable | Required only for tighter PSU-specific or compliance-level surge claims | Medium | User nominal image + ≈24 V measurement available; official spec absent |
| Mechanical envelope | Enclosure, board size, mounting and wiring constraints | Final USB/terminal mechanical selection and PCB outline | High; freeze before Stage 5 | Open；TYPE-C-31-M-12 remains mechanical-conditional |
| M3 implementation validation | Current schematic PDF/BOM/EDA evidence plus later hardware test | ERC/footprint completeness、USB enumeration、UART communication、independent power sequencing、PCB isolation geometry、EMC/ESD | High before applicable later gates | M3 current-session screenshot reviewed；module design closeout acceptable, validation remains open |
| Detailed board power validation | Output-capacitor DC-bias data、startup/inrush evidence、thermal and layout evidence；Q25 symbol/footprint mapping report or direct EDA verification | F1 startup coordination、effective capacitance、thermal and switch-current-loop verification；final closure of SR-M1-001 | High; needed before the applicable later gates | C14/C15/C16 frozen as C87996；Q25 corrected topology visually reviewed；Q25 symbol-to-footprint pad mapping remains narrowly pending |
