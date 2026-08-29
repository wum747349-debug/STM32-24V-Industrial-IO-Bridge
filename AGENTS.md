# AGENTS

本文件只负责 Standalone Project 的启动上下文路由；以下 Validator-sensitive exact phrases 保留 canonical English wording。

1. Read `FRAMEWORK.md` first（先读取 `FRAMEWORK.md`）。
2. 再读取本 Project 的 `PROJECT_RULES.md`。
3. Obtain the bound Framework Release and immutable Commit from `FRAMEWORK.md`（取得绑定的 Release 与 immutable Commit）。
4. 从该 bound Framework snapshot 读取 `docs/AI_Context_Guide.md`。
5. 只加载当前任务需要的 Project Facts、Stage Method 与 Evidence。
6. Do not default to Framework `main`（不得默认读取 Framework `main`）。
7. Do not read another Project by default or use it as this Project's fact source（不得默认读取其他 Project 或把它作为事实源）。

绑定 Framework snapshot 提供 Workflow、Skill、Checklist 与专项 Guide；本 Project repository 提供自己的 facts 与 evidence。
