# Critical Component Selection Plan

本文件是 Stage 2 — Critical Component Selection 的进入入口与后续 selection decision 主记录。本次 Gate 1.5 closeout 仅启用该 Stage-required 文件，不开始候选研究、器件 qualification、MPN 选择或 BOM 决策。

## Stage 2 Entry State

- Selection activity：Not started
- Candidate components：None recorded
- Selected components：None
- EDA implementation：Not started

## Confirmed Inputs

- 主控需求：STM32F103C8T6 直接集成到 PCB；最小系统实现尚未设计。
- 通信架构：board-mounted USB-UART 与 STM32 UART 之间采用 galvanic isolation；具体 USB-UART 与 digital isolator 未选择。
- Sensor acquisition：4 个 AN-LS18-40-N 的 NO + NC 均采集，共 8 路 digital inputs；具体 Sensor Input Frontend 未选择。
- CM35 scope：CM35 提供 IN1–IN18 / OUT1–OUT8；本板使用 IN11–IN18 / OUT1–OUT8，IN1–IN10 不属于本板控制范围。
- 制造目标：JLCPCB / LCSC 与 SMT / PCBA preferred；实际库存与装配可行性尚未核对。

## Selection Work Not Yet Started

后续 Stage 2 才按 `requirements.md` 的 OPEN-003～OPEN-010 与 `references.md` 的 evidence 状态，评估 USB connector、USB-UART、digital isolator、24 V protection、24 V → 3.3 V power、Sensor / CM35 interface、terminal 与相关关键器件。候选、淘汰理由、qualification basis 与最终 decision 必须在真实研究发生后写入本文件；本次不预填任何候选或具体 MPN。

## Evidence Boundary

- 关键参数必须依据 manufacturer official datasheet、reference manual 或 application note。
- Legacy schematic / BOM 只作为 Legacy Design Reference / Existing Functional Evidence，不自动成为本 Project 的器件决定。
- Supplier 页面只用于采购与装配可用性，不替代官方技术资料。
- 本文件当前不证明原理图、PCB、ERC、DRC、Manufacturing 或 Test 已完成。
