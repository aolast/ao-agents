---
name: ao-sdlc-overview
description: 软件开发 skills 的总入口。用于开始跨多个开发活动的任务、选择 SDLC 方法或恢复不清楚下一步的工作；根据任务路由到设计、实现、测试、审查、沟通、工作记录及专项活动。
---

# SDLC 使用指引

先读取目标项目的 `AGENTS.md`、开发入口及与任务有关的记录。确认用户目标、当前代码状态和已有授权；按需要查阅真实实现，文档过期时不要把它当作已验证事实。

## 选择方法

| 当前需要 | 读取的 skill |
| --- | --- |
| 明确行为、scope、方案或交付拆分 | [ao-sdlc-design](../design/ao-sdlc-design/SKILL.md) |
| 按已知方案完成修改或检查实现质量 | [ao-sdlc-implementation](../implementation/ao-sdlc-implementation/SKILL.md) |
| 选择测试、验证行为、判断证据是否充分 | [ao-sdlc-testing](../testing/ao-sdlc-testing/SKILL.md) |
| 审查设计或代码、复核问题和修正 | [ao-sdlc-review](../review/ao-sdlc-review/SKILL.md) |
| 撰写设计说明、commit、PR/CR、评论或进度 | [ao-sdlc-communication](../communication/ao-sdlc-communication/SKILL.md) |
| 暂停、交接、长任务 checkpoint 或恢复工作 | [ao-sdlc-work-log](../work-log/ao-sdlc-work-log/SKILL.md) |
| 建立开发分支、生成单提交审核分支或处理审核返工 | [ao-sdlc-branch-workflow](../implementation/ao-sdlc-branch-workflow/SKILL.md) |
| 原因未知，需要复现、收集证据或调查环境 | [ao-sdlc-investigation](../investigation/ao-sdlc-investigation/SKILL.md) |
| 保持外部行为，改善内部结构 | [ao-sdlc-refactoring](../refactoring/ao-sdlc-refactoring/SKILL.md) |
| 改善延迟、吞吐、资源占用或成本 | [ao-sdlc-performance-optimization](../performance-optimization/ao-sdlc-performance-optimization/SKILL.md) |

按名称定位当前需要的 skill；本源码树可用相对链接读取。缺失引用时说明限制，继续可做的部分，不假装已加载。被引用 skill 应用其当前职责，不再反向启动整套流程；已读取的规则可以复用。

## 组合与完成

- 需求实现通常从 design 开始，经 implementation 和 testing 后使用 review 自审。已充分明确的小修复直接进入实现和验证。
- 排查先使用 investigation。结论可以是配置问题或证据不足，不预设一定要改代码。
- 技术债清理先用 design 判断具体负担和处理范围，再按目标进入重构、性能或普通实现。
- 发现新约束时返回相关方法；复核已通过且未受影响的部分无需完整重做。
- 遵循任务本身的交付要求。审查任务交付结论，实施任务交付变更和证据，不因加载此目录自动执行部署、安装或合并。

对外说明实际结果、重要证据和剩余问题。只有确实需要交接或避免显著返工时才维护 work log。

## 边界示例

- “给现有校验补一个已明确的边界条件”：选择 implementation 和 testing，不要求另写架构设计书。
- “帮我判断这个 PR 是否可以接受”：选择 review 及相关标准，先完成审查，不自动改写作者的代码。
