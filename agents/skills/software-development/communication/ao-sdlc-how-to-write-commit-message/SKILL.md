---
name: ao-sdlc-how-to-write-commit-message
description: 撰写或审查 commit message。用于依据实际 code change 表达变更目的、具体影响、关键理由和验证限制，并遵循目标仓库的提交格式；不负责执行提交、拆分变更或管理 Git 分支。
---

# 如何写 Commit Message

基于本次提交的实际 code change 和已有证据写作，采用 [communication](../ao-sdlc-communication/SKILL.md) 的通用表达原则；已读取时直接复用。

## 采用项目格式

Commit 格式、语言、是否使用 Conventional Commits、是否允许 scope 均读取目标仓库规则。没有约定时以清晰、简短的事实表达为准，不把 Ao Agents 的提交格式推广到其他项目。

## 标题与正文

标题让读者分辨这次具体变更，正文补充 code change 难以表达的信息。按变更需要交代：

- 为什么需要变更，以及具体影响。
- 关键实现理由，尤其是仅看 code change 难以理解的选择。
- 验证结果与实际限制，不把预期结果写成已验证事实。

简单拼写修正只需说明纠正了什么；无需额外编造用户影响、替代方案或长篇背景。正文的长度取决于读者理解这次变更需要的信息。

## 信息归属

提交消息解释这次变化及理由；长期维护信息、评审对话与接手状态的归属遵循 communication 的“信息归属与核对”。

完成后对照实际 code change 核对描述，确认基线行为、提交后的结果和已部署的运行事实没有混淆。提交操作、分支和提交组织由 [workplace-and-git-branch](../../implementation/ao-sdlc-workplace-and-git-branch/SKILL.md) 负责；仅写消息时不启动这些流程。
