---
name: ao-sdlc-branch-workflow
description: 使用开发与审核两个分支命名空间，保留增量开发历史并生成单提交审核分支。用于开始开发任务、准备 PR/CR/MR、审核返工或同步目标分支；遵循项目指定前缀，未指定时使用 dev/ 与 review/。
---

# 开发与审核分支

先读取目标项目的开发规则，确认目标分支、远端、命名空间及当前工作区。采用项目指定的开发与审核前缀；未指定的分别默认为 `dev/`、`review/`，两个分支共用同一任务名。目标分支从任务与项目约定确定，不假定为 `main`。若项目明确采用其他分支流程，遵循该流程。

## 两个分支的职责

| 分支 | 职责 |
| --- | --- |
| 开发分支，如 `dev/<任务名>` | 从最新目标分支创建，承载实现、验证与审核修正；可以按需要多次 commit，保留开发过程中的版本。 |
| 审核分支，如 `review/<任务名>` | 准备送审时从当时最新的目标分支创建，将开发成果 squash 为一个 commit，由此发起并持续更新同一个 PR/CR/MR。 |

单提交要求作用于审核分支。不要为了整理审核历史压缩开发分支，也不要从 dev 的 head 直接创建 review 后保留全部开发 commits。

## 首次送审

1. 在开发分支完成实现、提交和必要验证。切换或改写分支前处理好已有未提交修改；同名分支存在时先检查是否属于当前任务，避免覆盖其他工作。
2. 获取最新目标分支，将开发分支 rebase 到该基线，保留本任务的增量 commits。冲突在 dev 上解决并完成 rebase，按影响重新验证。Rebase 会改变 commit ID，但不要求将开发步骤 squash 成一个。
3. 从该基线创建审核分支，用 `git merge --squash <开发分支>` 暂存完整成果，再按项目提交格式创建一个 commit。不要通过 merge dev 的方式把开发历史带入审核分支。
4. 核对下文的送审条件，再推送审核分支并创建审核请求。开发分支是否推送由备份、协作需要及已有授权决定；审核请求使用 review 分支。

例如，项目以 `origin/main` 为目标且使用默认前缀时，以下命令用于已有开发提交、工作区干净且审核分支尚不存在的首次送审：

```sh
git fetch origin
git switch dev/example-task
git rebase origin/main
# 如有冲突，先解决并完成 rebase；验证通过后继续。
git switch -c review/example-task origin/main
git merge --squash dev/example-task
git commit
```

每步成功后再继续；提交消息采用目标项目格式。任何同步产生的新修改都须先回到开发分支验证，不能只在 review 上修正后就宣布完成。

## 审核返工与更新

回到原 dev 分支继续开发，用新的 commits 记录修正，再把完整成果更新到原 review 分支。若有人直接修改了 review，先核对差异，把有效改动移回 dev 并验证；不要用旧 dev 快照覆盖这些改动，也不要把 review 的 squash commit 整体合回 dev。

- **目标基线未变**：把已验证的 dev 完整文件树同步到 review 的暂存区与工作区，然后 `git commit --amend`，保留一个审核 commit。同步必须包含删除与重命名。不要假定再次 `merge --squash dev` 会自动识别已送审内容；两条分支没有共享开发 commits，重复 squash 可能冲突。
- **目标分支前进，或不便 amend**：先在 dev 上同步最新目标并验证，再从该基线创建临时候选分支，重新 squash dev 并提交。核对完整 diff、文件树及相对旧 review 的变化后，用候选提交更新原 review 分支，保持原审核请求。改写前保留旧 review 的可恢复引用；候选分支不能通过额外 commit 或 merge 接到旧 review 后面。
- **远端审核分支已有更新**：先读取并检查他人提交，处理后再更新。对已推送分支的改写使用 `git push --force-with-lease`，以检查过的远端 head 为预期值；lease 失败时重新检查，不能改用 `--force` 绕过。

同步目标分支采用 rebase，避免引入 merge commit。若共享 dev 分支需要 rebase，也先检查协作者更新；不强推目标分支。

## 每次送审的条件

记录本次同步后的目标基线与已验证 dev head，检查：

```sh
git merge-base --is-ancestor <目标基线> <审核分支>
git rev-list --count <目标基线>..<审核分支>
git rev-list --merges <目标基线>..<审核分支>
git diff --exit-code <开发分支> <审核分支>
```

这些命令中的参数须替换为实际引用。结果应依次为成功、`1`、无 merge commit、无文件树差异；同时阅读相对目标基线的完整 diff，确认仅包含本任务。只有 commit 数为 `1` 不足以证明内容正确或已跟上目标分支。没有实际差异时无需创建空审核提交。

如果检查后 dev 又有提交，或目标分支前进，重新同步并检查受影响条件。推送后确认审核请求仍指向正确目标，等待 CI 针对最新 review head 通过；不要将 dev 的测试结果误称为审核分支的 CI 结果。

按项目合并策略和既有授权结束审核。合并后可清理 review；dev 按开发记录的保留需要归档或清理，先确认没有尚未送审的修改。review 的 squash 合并不代表 dev 的每个 commit 已按祖先关系合入目标，不能仅据此强制删除 dev。

## 边界示例

- 项目指定 `work/` 与 `cr/`：使用 `work/example-task` 和 `cr/example-task`；只指定开发前缀时，审核前缀仍可默认 `review/`。
- Dev 有三个实现提交，审核要求修改：在 dev 增加第四个提交，更新后的 review 仍比目标基线多一个 commit，文件树对应第四次开发的完整结果。
- 目标分支增加了与任务无关的文件：先同步 dev，再生成 review；不能用落后 dev 的整棵文件树覆盖新基线，导致该文件被删除。

本 skill 负责分支和提交的组织；提交表达使用 [communication](../../communication/ao-sdlc-communication/SKILL.md)，验证深度使用 [testing](../../testing/ao-sdlc-testing/SKILL.md)。它不增加推送、发布评论或合并权限，也不把 Ao Agents 的提交格式和合并责任推广到其他项目。
