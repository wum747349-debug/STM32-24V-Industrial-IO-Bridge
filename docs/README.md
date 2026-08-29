# Stage Documents（阶段文档）

本目录保存 Stage-enabled 与 Conditional Project 文档。Bootstrap 不预建这些文件；只有真实活动触发时才创建。

| Path | Responsibility | Enable When |
| --- | --- | --- |
| `component_selection_plan.md` | Critical component candidates and decisions | Stage 2 begins |
| `module_design/*.md` | Module connections, calculations, evidence, risks, layout requirements | A module enters Stage 3 detail design |
| `schematic_review.md` | Actual schematic review evidence, issues, status, conclusion | Stage 4 begins |
| `pcb_design_rules.md` | Project rule values, Scope, Priority, configuration status, waiver definitions | Before Stage 5 Layout Preflight |
| `pcb_review.md` | Layout Preflight, routing issues, user DRC summary, waivers, manufacturing release | Layout Preflight is recorded; maintained through Stages 6–7 |
| `bringup_log.md` | Assembly, first power-on, measurements, debug history | Stage 8 assembly or bring-up activity begins |
| `test_report.md` | Test conditions, results, limits, acceptance conclusion | Stage 8 formal testing begins |
| `revision_history.md` | Hardware revisions, reasons, impact, required revalidation | First hardware revision or material change |
| `user/` | User-facing setup, wiring, interface, and safety guidance | The project requires user documentation |

当前 Project Stage 只在仓库根 `README.md` 维护。文件存在不证明对应 Stage 已通过。
