# Skills 目录

本目录统一索引可复用 skills。零散 skill 直接放在此目录；`software-development/` 按开发活动分组，各分类下放具体 skill 文件夹。

`communication/` 按表达职责组织，包含通用表达原则与具体产物的写作方法。Commit message 和设计文档的写作方法归入该分类；形成设计与作出方案取舍归入 `design/`，具体实现方法归入 `implementation/`。

<!-- BEGIN GENERATED SKILL CATALOG -->

| Skill | 说明 |
| --- | --- |
| [ao-create-agent-skill](ao-create-agent-skill/SKILL.md) | 为 Ao 创建或维护 agent skill 时应用个人补充要求，规范命名、语言和 skill 引用边界。 |
| [ao-vocabulary](ao-vocabulary/SKILL.md) | 按 Ao 的个人用语习惯处理中英互译、术语选择和中英文表达。用于翻译、润色、撰写含中英术语的内容，以及维护固定译法、保留英文和避免使用的说法。 |
| [ao-sdlc-communication](software-development/communication/ao-sdlc-communication/SKILL.md) | 软件开发中的共用表达原则。用于 commit message、review request、设计说明、评审意见和进度沟通，区分 code change、评审请求、分支称呼及平台术语，明确变更前后的版本参照、事实与证据。 |
| [ao-sdlc-how-to-write-commit-message](software-development/communication/ao-sdlc-how-to-write-commit-message/SKILL.md) | 撰写或审查 commit message。用于依据实际 code change 表达变更目的、具体影响、关键理由和验证限制，并遵循目标仓库的提交格式；不负责执行提交、拆分变更或管理 Git 分支。 |
| [ao-sdlc-design](software-development/design/ao-sdlc-design/SKILL.md) | 制定或审查软件变更设计。用于澄清预期行为、scope、模块与接口边界、技术债处理时机、方案取舍及交付拆分；按风险和未知项调整设计深度。 |
| [ao-sdlc-implementation](software-development/implementation/ao-sdlc-implementation/SKILL.md) | 按需求和设计完成增量代码变更，并提供可复用的实现质量标准。用于功能实现、已定位问题的修复及代码质量判断，覆盖职责、依赖、错误处理、资源生命周期和可维护性。 |
| [ao-sdlc-workplace-and-git-branch](software-development/implementation/ao-sdlc-workplace-and-git-branch/SKILL.md) | 用于创建或使用任务工作区、开始仓库修改、运行会写入文件的验证、操作 Git 分支及准备 PR/CR/MR。作为 coding agent 的开发习惯，定义工作区目录及默认位置，在其内部使用 clone 或 worktree 隔离仓库，在任务期间保留开发历史、生成单提交审核分支，并在合入目标分支后清理任务分支。 |
| [ao-sdlc-investigation](software-development/investigation/ao-sdlc-investigation/SKILL.md) | 调查软件问题的现象、发生条件和原因，并选择与实际环境匹配的专项方法。用于根因未知的 bug、运行时异常、数据库或 CI 环境问题、性能瓶颈定位；以证据区分假设，不预设必须改代码。 |
| [ao-sdlc-performance-optimization](software-development/performance-optimization/ao-sdlc-performance-optimization/SKILL.md) | 组织软件性能优化。用于改善延迟、吞吐、内存、资源占用或运行成本；定义代表性工作负载和指标，定位瓶颈，并在可比较条件下验证收益、正确性与代价。 |
| [ao-sdlc-refactoring](software-development/refactoring/ao-sdlc-refactoring/SKILL.md) | 组织保持外部行为的软件结构调整。用于消除重复规则、降低耦合、简化控制流或有明确结构目标的技术债清理；定义行为保持边界并组合设计、实现、测试与审查方法。 |
| [ao-sdlc-review](software-development/review/ao-sdlc-review/SKILL.md) | 组织软件设计或代码变更的独立审查、自审与修正复核。用于确认审查范围、调用共享工程标准、核实问题与反证，交付可执行且有依据的评审结论。 |
| [ao-sdlc-testing](software-development/testing/ao-sdlc-testing/SKILL.md) | 为软件变更设计和执行必要测试与验证。用于制定验收证据、补充回归测试、审查测试质量或判断验证是否充分；关注行为、关键失败路径、可靠性和维护成本。 |
| [ao-sdlc-work-log](software-development/work-log/ao-sdlc-work-log/SKILL.md) | 在软件开发任务中维护轻量工作记录并据此恢复。用于中途暂停、Agent 或人类交接、长期调查获得关键结论以及继续已有任务，降低重复调查成本而不过度记录过程。 |

<!-- END GENERATED SKILL CATALOG -->

目录由各 skill 的 frontmatter 自动生成。命名、组织与分发规则见 [DEVELOPING.md](../../DEVELOPING.md#skill-命名与检查)。
