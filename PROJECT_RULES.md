# PROJECT_RULES

1. Current Project facts come only from this repository（当前 Project facts 只来自本仓库）。
2. The Framework version is the Release + Commit recorded in `FRAMEWORK.md`（Framework version 以该绑定为准）。
3. 不自动采用或读取 Framework `main`。
4. Framework binding change 必须由用户明确要求：prerelease dogfooding 使用 Pinned Framework Evaluation，backward-compatible adoption 使用 Compatible Framework Sync，只有 breaking Runtime / Structural Contract adoption 使用 Framework Contract Migration；所有路径执行适用 validation。
5. 关键硬件参数必须回到官方 datasheet、reference manual 或 application note 核对。
6. `.SchDoc` and `.PcbDoc` are the authoritative EDA implementation sources。
7. AI/Codex 不得伪造 EDA、ERC、DRC、Manufacturing、Bring-up 或 Test 结果。
8. Maintain the current Project stage only in the root `README.md`（当前 Project stage 只在根 README 维护）。
9. 其他 Project 不能作为当前 Project 的 fact source。
10. Read only the Stage Skill and evidence required for the current task（只读取当前任务所需 Stage Skill 与 Evidence）。
