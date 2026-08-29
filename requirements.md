# Requirements Baseline

本文件保存 Stage 1 第一版需求边界。已确认内容来自用户提供的项目事实；未知事实保持 `TBD` / `待确认`，不构成器件选型、原理图实现或验证结论。

## Project Goal

设计 STM32F103C8T6 直接板载的 24 V 工业 I/O 中继与接口板，实现 C# 上位机经 USB / 板载 USB-UART 与 STM32 通信、STM32 与 CM35 之间 8 路控制及 8 路状态回读，并为 4 个 AN-LS18-40-N 光电开关提供独立现场接口和 24 V 供电。设计应改善现场接线、保护、调试和 PCBA 适配性，同时保留已经实际设备验证的 CM35 系统级功能行为作为 Legacy Functional Baseline。

## Out of Scope

- 本阶段不选择具体 USB-UART、digital isolator、DC/DC、TVS、反接保护、保险/PTC、Sensor Input Frontend 或端子 MPN。
- 不进行 Stage 2 Component Selection、Stage 3 Schematic Design 或任何后续 Stage 工作。
- 不创建或修改 `.SchDoc`、`.PcbDoc`，不执行 EDA drawing、PCB design、firmware implementation 或 manufacturing output。
- 不声称 ERC、DRC、Repour、PCBA、Bring-up 或实测已完成。
- 不把上一代 schematic / BOM 作为本项目当前 EDA authority，也不把旧器件未经重新 qualification 直接冻结为新设计。

## Functional Boundary

- 系统链路：C# 上位机 ↔ USB ↔ 板载 USB-UART ↔ STM32 ↔ CM35。
- CM35 实际提供 IN1–IN18 与 OUT1–OUT8；本 Project 只控制 IN11–IN18，并回读 OUT1–OUT8。IN1–IN10 不属于本板控制范围。
- CM35 控制：保留 8 路 STM32 → CM35 IN11–IN18 控制通道。
- CM35 回读：保留 8 路 CM35 OUT1–OUT8 → STM32 状态通道，包括当前保留通道。
- 传感器：连接 4 个相同 AN-LS18-40-N，每个传感器具有独立 `+24V / 0V / NO / NC` 现场端子；NO 与 NC 均采集，共 8 路 MCU sensor digital inputs。
- 板载功能：STM32F103C8T6 最小系统、板载 USB-UART、24 V 输入与保护、低压供电、SWD / 调试与必要测试入口。
- 固件负责把 Active-Low 物理 GPIO 语义转换为正逻辑协议语义；本项目本阶段只记录接口契约，不实现固件。

## Module Boundary

| Module | Stage 1 Responsibility |
| --- | --- |
| M1 — 24V Input / Protection / Low-voltage Power | 接收机器 24 V，形成受保护 24 V bus，并向机器侧低压逻辑供电；具体架构待后续阶段确定。 |
| M2 — STM32F103C8T6 Minimum System | 集成 MCU 本体及后续所需的供电、VDDA、reset、boot、clock、SWD、调试与安全启动边界。 |
| M3 — USB-UART Communication | 实现 PC USB 到 STM32 UART，并在 USB-UART 与 machine-side STM32 UART 之间设置 galvanic isolation；具体器件待后续阶段确定。 |
| M4 — CM35 Industrial I/O Interface | 8 路 STM32 → IN11–IN18 控制与 8 路 OUT1–OUT8 → STM32 回读。 |
| M5 — Photoelectric Sensor Interface | 为 4 个 AN-LS18-40-N 供电，并接收每个传感器的 NO + NC，共 8 路输入；具体输入前端待后续阶段确定。 |
| M6 — Connectors / SWD / Indicators / Test Points | 提供便于现场接线、编程、调试和安全首次上电的物理入口；指示功能范围待确认。 |

## Power Requirements

- 外部机器电源为 24 V DC。
- 24 V 输入必须经过保护后形成 protected 24V bus；该 bus 至少服务 CM35 interface、4 个光电开关与板上低压电源。
- 板上必须产生 STM32 与机器侧逻辑所需低压电源；24 V → 3.3 V 的具体架构和器件待 Stage 2/3。
- 必须考虑反接、surge / transient、外部工业长线与输入保护；具体 TVS、fuse/PTC、reverse-polarity 与 DC/DC 方案待定。
- USB 供电不得意外反向供电 machine-side power system。
- 首次上电必须支持安全的限流测试流程；实际限流值与步骤待后续设计和 Bring-up 计划确定。
- 4 个传感器由板上 protected 24V bus 供电；总功耗、电流预算与热设计待取得官方资料并在后续阶段核算。

## Interface Requirements

### PC / USB / UART

- 采用 board-mounted USB-UART，尽量复用现有串口帧与 C# 上位机 communication model。
- USB-UART 与 STM32 UART 之间必须采用 galvanically isolated UART interface；PC USB ground 与 machine-side 24 V `0V` 不直接共地。
- USB connector 类型、USB-UART IC、digital isolator、USART/GPIO 分配及具体隔离实现均待后续阶段确定。

### STM32 → CM35（IN11–IN18）

- 保留 8 路硬件通道；上一代经实际设备验证的系统行为是对 CM35 输入信号线下拉至 24 V `0V` 时输入有效。
- Protocol / Application contract：`DataIn = 1` 表示 Active，`DataIn = 0` 表示 Inactive。
- Physical controller-output GPIO contract：`LOW = Active`，`HIGH = Inactive`；极性转换属于 STM32 firmware。
- 上一代 2N7002 下拉实现作为 Legacy Design Reference；用户已在 Stage 2 明确授权复用该转换思路，新原理图仍必须根据当期器件与官方资料重新 qualification。

### CM35 → STM32（OUT1–OUT8）

- 保留 8 路硬件通道；Stage 2 对归档上一代原理图的检查显示，legacy readback 同样采用 2N7002 MOSFET conversion networks，而不是 optocoupler。上一版文字中的 optocoupler 描述已按实际 schematic evidence 纠正。
- 上一代系统行为仍为 CM35 Active → STM32 GPIO LOW，Inactive → GPIO HIGH；新设计的 exact resistor values、输入保护与阈值必须在 Stage 3 结合 CM35 当期电气资料重新 qualification。
- Protocol / Application contract：`DataOut = 1` 表示当前状态 Active，`DataOut = 0` 表示 Inactive。
- firmware 必须执行 Active-Low → positive protocol semantic inversion。

### CM35 Handshake Protocol — Version B

| CM35 Input | Meaning / Encoding |
| --- | --- |
| IN11 | Start Request：OFF=无效，ON=启动请求有效 |
| IN12 | Scan Mode：OFF=正式扫描，ON=参考扫描 |
| IN13 / IN14 | Reference Count Encoding：`00=3`、`01=5`、`10=8`、`11=12`；仅参考扫描使用 |
| IN15 | Scan Length：OFF=8 mm，ON=15 mm |
| IN16 | Scan Speed：OFF=20 mm/min，ON=30 mm/min |
| IN17 | Reserved / Spare；保留硬件通道 |
| IN18 | Reserved / Spare；保留硬件通道 |

- IN11 只表示 Start Request；IN12 只选择 Formal / Reference Scan；IN16 只选择速度。
- Formal scan 不使用 IN13 / IN14；启动前必须先设置 length 与 speed。
- Reference scan 启动前必须先设置 length、speed 与 reference-count encoding。

| CM35 Output | Meaning |
| --- | --- |
| OUT1 | BUSY — 运动执行中 |
| OUT2 | SYNC — 采集同步脉冲 |
| OUT3 | DONE — 扫描段结束脉冲 |
| OUT4 | FAULT — 故障 / 保护信号 |
| OUT5–OUT8 | Reserved；必须保留硬件通道 |

### Photoelectric Sensors

- 4 个用户已购 AN-LS18-40-N：M18 laser diffuse-reflective、NPN、4-wire NO + NC、DC 10–30 V、检测距离 30–400 mm。
- 用户提供的接线定义：Brown=`+24V`、Blue=`0V`、Black=`NO`、White=`NC`；后续连接前仍需以可追溯的正式资料核对。
- 每个传感器使用独立 `+24V / 0V / NO / NC` 端子。
- 现场长线输入必须考虑 ESD / transient / noise、input current limiting / protection，并可考虑 RC / hardware filtering；无需高速数字输入。
- 具体采用 transistor、Schmitt buffer、comparator 或 optocoupler 留待 Stage 2/3。
- 每个传感器的 NO + NC 均采集：4 个传感器共 8 路 MCU sensor digital inputs。

## Safety Boundary

- MCU reset、boot、firmware not ready 及任何上电瞬态期间，全部 CM35 control 必须保持 OFF / inactive，不得触发 CM35 输入误动作。
- 外部 24 V、CM35 与 Sensor 长线接口必须考虑反接、ESD、surge/transient、噪声和故障传播。
- USB-UART 与 STM32 UART 之间的 galvanic isolation 是已确认架构要求，用于隔离 PC USB ground 与 machine-side 24 V `0V`；具体器件、额定值与实现仍需后续 qualification。
- USB 侧不得意外 back-power 机器侧；不同电源域之间的掉电、插拔与 fault state 必须在后续设计中验证。
- 首次上电使用可限流电源并分阶段验证；具体安全 procedure 后续建立，当前未执行实物上电。
- 本 Stage 1 不声称满足任何未定义的法规、functional safety 或 isolation rating；如项目需要，须由用户另行确认适用标准。

## Manufacturing Baseline

- JLCPCB / LCSC preferred；PCB assembly 以 JLCPCB SMT / PCBA 为优先目标。
- MCU 与主要器件尽量直接 SMT，减少人工焊接；connector 的 SMT / THT 取决于后续装配和机械 qualification。
- 器件应尽量具备嘉立创可采购/可贴装性，但具体库存、料号与替代方案属于 Stage 2。
- CM35 IN11–IN18、OUT1–OUT8 使用便于现场接线的 terminal block；4 个 Sensor 各使用独立 4-wire terminal；24 V 输入使用独立 terminal。
- 当前倾向约 5.0 / 5.08 mm pitch，可评估 pluggable screw terminal；具体 pitch、系列与 MPN 尚未冻结。
- PCB layer count、板厚、铜厚、尺寸、安装孔、enclosure 与 mounting constraints 均待确认。

## Acceptance Criteria

| ID | Requirement | Verification Method | Expected Result |
| --- | --- | --- | --- |
| REQ-001 | Repository 使用固定 Framework v1.1.1 snapshot 并保持 Standalone Project 结构 | Project Validator + 人工核对 | binding、Required files、导航与状态一致，无 Template residue |
| REQ-002 | 具有 8 路 STM32 → CM35 IN11–IN18 硬件通道 | 后续原理图审查与硬件测试 | 8 路均存在，含 IN17/IN18 reserved channels |
| REQ-003 | 具有 8 路 CM35 OUT1–OUT8 → STM32 硬件通道 | 后续原理图审查与硬件测试 | 8 路均存在，含 OUT5–OUT8 reserved channels |
| REQ-004 | 保持 Version B handshake mapping 与时序前置规则 | Firmware/interface review + integration test | IN/OUT mapping、scan prerequisites 与协议语义一致 |
| REQ-005 | 保持协议正逻辑与物理 Active-Low 的跨层契约 | Schematic / firmware / PC software interface review | DataIn/DataOut 的 `1=Active`，GPIO Active-Low inversion 明确且一致 |
| REQ-006 | reset、boot、firmware not ready 时 CM35 controls 为 inactive | 后续原理图分析、上电与 fault-injection test | 不发生 CM35 输入误动作 |
| REQ-007 | 4 个传感器各有独立 `+24V/0V/NO/NC` 现场端子，并采集全部 NO + NC | 原理图/PCB审查与接线检查 | 四组接口完整、标识清晰，共 8 路 MCU sensor digital inputs |
| REQ-008 | 传感器长线输入具备与工业环境相适应的保护/限流/抗噪声设计 | 后续设计审查与测试 | 设计依据可追溯；测试条件与结果后续定义 |
| REQ-009 | 板载 USB-UART 经 galvanically isolated UART interface 连接 STM32 | 后续原理图审查、隔离边界检查与通信测试 | 无需外置 USB-to-serial module；PC USB ground 与 machine-side 24 V `0V` 不直接共地；现有通信模型可评估复用 |
| REQ-010 | USB 不得 back-power machine-side power system | Power-state review + 插拔/掉电测试 | 所有相关供电状态下无非预期反向供电 |
| REQ-011 | 24 V 输入保护并建立 protected 24V bus 与逻辑低压电源 | 后续设计审查与上电测试 | 保护与供电架构有官方依据，满足已确认负载与 fault boundary |
| REQ-012 | CM35、Sensor 和 Power terminals 适合现场接线 | Mechanical/PCB review + 装配检查 | pitch/系列经确认，接线与维护可达性满足用户约束 |
| REQ-013 | 面向 JLCPCB / LCSC 与 SMT / PCBA | BOM/DFM/装配审查 | 关键器件和装配路线可采购、可制造；例外有明确记录 |
| REQ-014 | 首次上电可安全限流测试 | Bring-up plan review + 用户执行 | 有分阶段限流步骤、预期与停止条件；当前尚未执行 |

## Open Questions

| ID | Question | Impact | Decision Needed By | Owner / Source | Qualification / Confirmation Plan | State |
| --- | --- | --- | --- | --- | --- | --- |
| OPEN-001 | USB-UART 是否进行 galvanic isolation？ | 决定 ground loop、噪声、故障传播、电源域和 BOM | Resolved in Stage 1 | 用户确认 | 采用 board-mounted USB-UART + galvanically isolated UART interface；Stage 2 Primary 为 CH340C + ISO7721DR，Stage 3 继续核对 power-state/back-power behavior | Closed |
| OPEN-002 | 每个传感器读取 NO only 还是 NO + NC？ | 决定 MCU 输入数量、前端通道数、端口资源与诊断能力 | Resolved in Stage 1 | 用户确认 | 每个传感器 NO + NC 均采集，4 × 2 = 8 路 MCU sensor digital inputs；具体 frontend 留待 Stage 2/3 | Closed |
| OPEN-003 | USB connector 具体类型？ | 影响机械可靠性、装配、外壳和线缆 | Before Stage 2 selection | 用户 / Mechanical | Stage 2 conditional candidate 为 TYPE-C-31-M-12；待 enclosure / 板边机械约束确认后才能关闭 | Open |
| OPEN-004 | CM35 / Sensor / Power terminal 最终 pitch 和系列？ | 影响板尺寸、现场接线、装配方式与成本 | Select in Stage 2; freeze before Stage 5 | 用户 / Mechanical / JLCPCB capability | 比较约 5.0/5.08 mm 候选、pluggable 需求与 PCBA 可行性 | Open |
| OPEN-005 | 24 V input protection architecture？ | 影响反接、surge/transient 能力、压降、热与安全 | Resolved in Stage 2 | 用户 measurement + Stage 2 qualification | 采用 input overcurrent element + STPS2H100A series reverse-polarity protection + SMBJ30A-TR TVS + protected 24V bus；exact fuse/PTC rating、surge waveform/source impedance 与 thermal margin 留待 Stage 3 计算 | Closed |
| OPEN-006 | 24 V → 3.3 V power architecture？ | 影响效率、热、噪声、布局、成本与可采购性 | Resolved in Stage 2 | Stage 2 qualification | Primary 采用 LMR36510FADDAR 65 V / 1 A class synchronous buck；exact inductor/FB/capacitors/load budget/thermal 留待 Stage 3 | Closed |
| OPEN-007 | exact GPIO / USART pin allocation？ | 影响通道数量、boot/debug、安全状态与 PCB routing | Stage 3 | Stage 3 design | 按已确认的 8 路 sensor inputs 与隔离 UART 架构进行资源分配、启动状态和冲突检查 | Open |
| OPEN-008 | exact isolation / sensor-interface components？ | 影响输入阈值、保护、速度、功耗、隔离与通道密度 | Select in Stage 2; qualify in Stage 3 | Stage 2/3 qualification | Stage 2 Primary 已确定 ISO7721DR 与 Nexperia 2N7002,215；CM35/Sensor exact resistor、filter、ESD/transient/current-limiting network 仍需官方外设电气资料与 Stage 3 qualification | Open |
| OPEN-009 | enclosure / PCB size / mounting constraints？ | 影响 connector 布局、板框、安装孔、散热和可维护性 | Collect before Stage 2; freeze before Stage 5 | 用户 / Mechanical | 收集可用空间、安装方式、禁布区、固定点及接线方向并确认 | Open |
| OPEN-010 | 是否需要 indicator LEDs / additional diagnostic interface？ | 影响 GPIO、电源预算、面板可见性和调试效率 | Before Stage 2 selection | 用户 / Serviceability | 定义必须显示的 power/communication/I/O/fault 状态和可见性需求 | Open |
