# 软件开发 skills

这里维护软件开发生命周期（software development lifecycle, SDLC）中的可复用工作方法。面向 Agent 编写，人类也可读取和使用；正文中文为主，保留必要英文术语。

## 分组与职责

| 分类目录 | Skill | 维护的内容 |
| --- | --- | --- |
| 根目录（总入口） | [ao-sdlc-overview](ao-sdlc-overview/SKILL.md) | 能力目录、选择条件与常见组合 |
| `design/` | [ao-sdlc-design](design/ao-sdlc-design/SKILL.md) | 目标、scope、行为契约、方案与交付拆分 |
| `implementation/` | [ao-sdlc-implementation](implementation/ao-sdlc-implementation/SKILL.md) | 增量实现方法与代码质量标准 |
| `implementation/` | [ao-sdlc-workplace-and-git-branch](implementation/ao-sdlc-workplace-and-git-branch/SKILL.md) | 工作区隔离、保留开发历史与单提交审核的开发习惯 |
| `review/` | [ao-sdlc-review](review/ao-sdlc-review/SKILL.md) | 审查范围、问题核实、结论与复核方法 |
| `testing/` | [ao-sdlc-testing](testing/ao-sdlc-testing/SKILL.md) | 验证策略、测试质量与证据边界 |
| `work-log/` | [ao-sdlc-work-log](work-log/ao-sdlc-work-log/SKILL.md) | 轻量 checkpoint 与工作恢复 |
| `investigation/` | [ao-sdlc-investigation](investigation/ao-sdlc-investigation/SKILL.md) | 证据驱动的排查及环境专项方法的入口 |
| `refactoring/` | [ao-sdlc-refactoring](refactoring/ao-sdlc-refactoring/SKILL.md) | 保持行为的结构调整方法 |
| `performance-optimization/` | [ao-sdlc-performance-optimization](performance-optimization/ao-sdlc-performance-optimization/SKILL.md) | 指标、瓶颈、优化收益与代价 |
| `communication/` | [ao-sdlc-communication](communication/ao-sdlc-communication/SKILL.md) | 工程表达、版本参照与读者需要的信息 |

分类目录按开发活动组织，每个目录下放独立的 skill 文件夹；同一活动可容纳通用方法和更具体的工作方法。overview 是跨活动的总入口，保留在领域根目录；跨活动的工程沟通单列 communication。目录表达职责，不构成强制的调用层级。review 会引用设计、实现和测试标准；设计时就可以规划测试；各活动可以相互组合。规则只在所属 skill 维护，调用者负责选择与衔接。

## 任务与方法

任务 prompt 描述“这一次做什么、在哪里做、有哪些限制”；skill 描述稳定、可复用的判断方法。refactoring 等活动即使主要通过组合其他 skills 完成，也有独立的方法价值。

| 任务 | 典型使用方式 |
| --- | --- |
| 实现需求 | design 确定必要方案，implementation 实现，testing 验证，review 自审 |
| 已定位的局部 bug | implementation + testing；仅在方案有分歧时补 design |
| 原因未知的问题 | investigation 找证据，再按结论决定是否修改 |
| 独立审查 | review 引用相关标准，不自动执行作者的修改任务 |
| 重构或技术债清理 | design 判断成本和 scope，再按目标选 refactoring 或其他活动 |
| 性能问题 | performance-optimization 明确指标，investigation 定位，随后实现与验证 |
| 中途接手 | work-log 核对当前状态，再选择下一项活动 |

communication 与 work-log 按实际表达和连续性需要使用，不是每个任务都要单独生成文档。活动深度以风险、未知项和恢复成本决定。

## 目录、依赖与项目规则

- 领域目录为 `agents/skills/software-development/`，实际 skill 使用 `ao-sdlc-` 前缀，包含与目录同名的 `name` 字段。
- 除总入口外，skill 使用 `<活动目录>/<skill 名称>/SKILL.md` 布局，例如 `implementation/ao-sdlc-implementation/SKILL.md`。分类目录不需要 `ao-` 前缀，也不直接放 `SKILL.md` 或自动产生指令继承；具体 skill 文件夹保留完整名称。
- investigation 的运行时、数据库、CI 等环境专项子 skills 按实际需求增加。初版只定义通用调查方法与选择原则，不预建空目录或假定某个环境可访问。
- 引用其他 skill 时先按名称在可用目录中定位，再读取对应内容；在本源码树可直接读取文中的相对链接。只加载当前需要的内容，已加载且仍适用的标准不必重复读取。
- 引用缺失时明确哪些方法未加载，继续不依赖它的工作；只有缺失信息确实阻塞当前判断时才请求补充。不能声称已经调用了不可用的 skill。
- 分发时应保留活动分类与 skill 目录的相对布局，或让宿主按名称找到全部被引用 skills。仅复制 overview 无法分发整套能力；源码嵌套不保证工具自动发现。初版不提供安装器，尚未验证具体宿主的安装发现行为。
- 通用 skill 读取目标项目的 `AGENTS.md`、开发文档及代码事实；不将 Ao Agents 自己的单 commit、提交格式或工具权限规则套用到其他项目。调用 skill 不增加外部操作权限，也不推翻会话中已有授权。

项目稳定事实由项目文档维护，暂不设置 repository-context skill。Scope 方法归 design；笼统的“优化”应先明确改善目标，再选择对应活动。

## 初版状态与后续讨论

11 个 `SKILL.md` 均已编写，包含选择描述、方法、产出与边界示例；尚需结合 Ao 的真实工作进一步迭代。验证情况以关联 PR 的记录为准，不把格式检查当成长期使用效果证明。

沟通 skill 已参考用户指定的两篇文章，来源与取舍就近记录在其文件中。后续重点是规则是否改变了正确决策，以及是否误伤简单任务；避免靠不断增加硬性步骤修补个别案例。

设计讨论：[Issue #3](https://github.com/aolast/ao-agents/issues/3)。修改本目录遵循根目录 [DEVELOPING.md](../../../DEVELOPING.md)。
