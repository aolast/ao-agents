# Skills 目录

本目录统一索引可复用 skills。零散 skill 直接放在此目录；`software-development/` 按开发活动分组，各分类下放具体 skill 文件夹。

Testing 按项目、阶段及验证对象确定证据与完成条件。

`communication/` 按表达职责组织，包含通用表达原则与具体产物的写作方法。Commit message、review request 和设计文档的写作方法归入该分类；形成设计与作出方案取舍归入 `design/`，具体实现方法归入 `implementation/`。

Commit message 与 review request 的写作统一由 `ao-sdlc-write-change-descriptions` 提供，按用户请求选择一种或两种产物；模板、checklist 和完整配对示例均在其 `SKILL.md` 内维护。

`review/` 保留两个独立入口：`ao-sdlc-code-review` 负责代码评审及实现后自审，`ao-sdlc-system-design-review` 负责系统设计专项评审。两者不互相调用；按待审对象选择，代码中的高层解决思路在代码评审中结合目标判断，系统职责、跨组件契约、数据归属及运行方式的专项评审使用系统设计入口。

`ao-sdlc-code-review` 按背景、动机与解决思路，修改范围，代码实现，测试四章组织；实现层依次检查功能正确性、代码质量与可读性、性能，测试代码应用同一套质量标准。可显式调用 `$ao-sdlc-code-review` 并提供待审 code changes，也可指定评审维度。内容由 frontmatter、简介、分层 checklist/question list 和结果模板组成；结果采用通过／未通过与 P1/P2/P3 分级，结合基线说明问题归属，必要复现和关键假设写在对应问题内。

两个 review skills 均为宿主无关、自包含的文本指令。源码目录存在不代表已安装或生效。

SDLC 中，design 负责形成契约与关键取舍，implementation 在这些约束内细化代码，并将有证据的设计冲突反馈到相关决定；low-level design 按决策影响划界，不固定归属某个阶段。Review 负责独立评审或实现后自审；implementation 保留编写指导，详细评审方法与 checklist 由 review skills 维护。

编排 skills 为 `ao-sdlc-implementation`、`ao-sdlc-workplace-and-git-branch`、`ao-sdlc-refactoring` 和 `ao-sdlc-performance-optimization`，按实际步骤以完整名称引用所需能力；分发时需确保依赖可发现。其余 SDLC skills 聚焦自身职责，不依赖其他 skills；skill 内部 references 仍通过相对链接读取。

`ao-write-task-item` 用于定义与拆解任务，可显式调用 `$ao-write-task-item` 并提供目标、已有任务或新发现；适用于支持文本 skills 的宿主，不依赖其他 skills 或外部任务系统。当前为仓库维护源，尚未安装到本机加载目录。

<!-- BEGIN GENERATED SKILL CATALOG -->

| Skill | 说明 |
| --- | --- |
| [ao-create-agent-skill](ao-create-agent-skill/SKILL.md) | 为 Ao 创建或维护 agent skill 时应用个人补充要求，规范命名、语言和 skill 引用边界。 |
| [ao-vocabulary](ao-vocabulary/SKILL.md) | 按 Ao 的个人用语习惯处理中英互译、术语选择和中英文表达。用于翻译、润色、撰写含中英术语的内容，以及维护固定译法、保留英文和避免使用的说法。 |
| [ao-write-task-item](ao-write-task-item/SKILL.md) | 在定义，拆解任务时使用。 |
| [ao-writing-review](ao-writing-review/SKILL.md) | 审核和润色文档、说明、指令及日常书面表达，依据 checklist 和案例识别写作 anti-pattern，重点检查缺乏语境支撑的防御性补充、无依据的对比及信息位置不当。用于请求 writing review、检查表达问题或按已知问题润色文本时。 |
| [ao-sdlc-communication](software-development/communication/ao-sdlc-communication/SKILL.md) | 软件开发中的共用表达原则。用于 commit message、review request、设计说明、评审意见和进度沟通，区分 code change、评审请求、分支称呼及平台术语，明确变更前后的版本参照、事实与证据。 |
| [ao-sdlc-write-change-descriptions](software-development/communication/ao-sdlc-write-change-descriptions/SKILL.md) | 撰写、审查或更新 commit message 与 review request（PR/CR/MR）的标题和正文，按提交或完整送审目标组织事实、动机、取舍和验证说明；内含两套模板、配对示例及各自的 checklist，不负责提交、送审操作或代码审查。 |
| [ao-sdlc-design](software-development/design/ao-sdlc-design/SKILL.md) | 制定和细化软件变更方案。用于澄清预期行为、scope、模块与接口边界、技术债处理时机、方案取舍及交付拆分；按风险和未知项调整设计深度，不作为独立设计评审入口。 |
| [ao-sdlc-implementation](software-development/implementation/ao-sdlc-implementation/SKILL.md) | 组织从需求和设计到增量代码变更的实现工作流。用于功能实现与已定位问题的修复，按需组合工作区准备、方案澄清、验证和实现后自审；不作为独立代码评审入口。 |
| [ao-sdlc-workplace-and-git-branch](software-development/implementation/ao-sdlc-workplace-and-git-branch/SKILL.md) | 用于创建或使用任务工作区、开始仓库修改、运行会写入文件的验证、操作 Git 分支及准备 PR/CR/MR。作为 coding agent 的开发习惯，定义工作区目录及默认位置，在其内部使用 clone 或 worktree 隔离仓库，在任务期间保留开发历史、生成单提交审核分支，并在合入目标分支后清理任务分支。 |
| [ao-sdlc-investigation](software-development/investigation/ao-sdlc-investigation/SKILL.md) | 调查软件问题的现象、发生条件和原因，并选择与实际环境匹配的专项方法。用于根因未知的 bug、运行时异常、数据库或 CI 环境问题、性能瓶颈定位；以证据区分假设，不预设必须改代码。 |
| [ao-sdlc-performance-optimization](software-development/performance-optimization/ao-sdlc-performance-optimization/SKILL.md) | 编排软件性能优化中的调查、方案选择、实现与验证。用于改善延迟、吞吐、内存、资源占用或运行成本；定义代表性工作负载和指标，定位瓶颈，并在可比较条件下验证收益、正确性与代价。 |
| [ao-sdlc-refactoring](software-development/refactoring/ao-sdlc-refactoring/SKILL.md) | 组织保持外部行为的软件结构调整。用于消除重复规则、降低耦合、简化控制流或有明确结构目标的技术债清理；定义行为保持边界并组合设计、实现、测试与审查方法。 |
| [ao-sdlc-code-review](software-development/review/ao-sdlc-code-review/SKILL.md) | 使用分层 checklist 评审 code changes 及其背景与解决思路，并按结果模板交付结论。覆盖背景、动机与解决思路、修改范围、代码实现和测试；实现层细分功能正确性、代码质量与可读性、性能。用于完整 review、自审、指定层级评审及修正复核。 |
| [ao-sdlc-system-design-review](software-development/review/ao-sdlc-system-design-review/SKILL.md) | 评审系统设计中的职责边界、接口契约、数据流、失败语义和演进方案。用于设计稿评审，或 code change 改变服务边界、数据归属、跨组件契约及运行方式时；聚焦方案能否满足需求与约束。 |
| [ao-sdlc-testing](software-development/testing/ao-sdlc-testing/SKILL.md) | 为软件变更规划和执行测试与验证。按项目要求、开发阶段及 function、class、module 或 feature 的验证目标确定范围、证据和停止条件，判断当前结论是否成立及还缺什么。 |
| [ao-sdlc-work-log](software-development/work-log/ao-sdlc-work-log/SKILL.md) | 在软件开发任务中维护轻量工作记录并据此恢复。用于中途暂停、Agent 或人类交接、长期调查获得关键结论以及继续已有任务，降低重复调查成本而不过度记录过程。 |

<!-- END GENERATED SKILL CATALOG -->

目录由各 skill 的 frontmatter 自动生成。命名、组织与分发规则见 [DEVELOPING.md](../../DEVELOPING.md#skill-命名与检查)。
