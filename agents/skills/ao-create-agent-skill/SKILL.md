---
name: ao-create-agent-skill
description: 为 Ao 创建或维护 agent skill 时应用个人补充要求，规范命名、语言和 skill 引用边界。
---

# Ao 的 Skill 补充要求

仅记录 Ao 的个人要求，作为通用 skill 创建能力的补充。

1. Ao 的个人 skill 名称使用 `ao-` 前缀。
2. 说明和指令以中文为主，保留必要的英文术语、标识符和原文。
3. 普通 skill 专注自身职责，不引用、调用或要求读取其他 skills。

   1. 只有以组合多个 skills 完成明确工作流为职责的 orchestrator skill 可以引用其他 skills；引用只写完整的 skill 名称，不使用路径或 Markdown 链接。
