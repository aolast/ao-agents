# Developing Ao Agents

本文件是人类与 Agents 共同遵守的开发、维护流程的唯一维护入口。开始工作前阅读 `README.md` 和相关目录说明；涉及边界调整时阅读 `docs/architecture.md`。

## 工作流程

1. 从最新 `main` 创建短期任务分支，理解需求，检查已有内容，确定受影响组件与唯一维护源。
2. 完成范围内最小且完整的变更，遵循已有结构，不预建执行器、通用配置语言或构建框架。
3. 同步更新受影响的使用说明，按下表完成与风险相称的验证。
4. 检查完整差异，将任务分支整理为单个 commit 后创建 PR；CI 通过后由 Ao 在 PR 中决定合并。禁止直接 push 到 `main`，包括管理员。

## 主干开发与 PR 提交历史

本仓库采用主干开发（trunk-based development），`main` 是唯一长期开发主干。变更使用短期任务分支，保持范围小、及时集成；不建立长期 `develop` 分支或按环境维护开发分支。

所有合入 `main` 的 PR 必须恰好包含 **一个 commit**，在 PR 合并前就满足此要求。不能依赖合并时 squash 来容忍 PR 内保留多个 commits。

- 创建 PR 前整理提交；PR 更新优先 amend 当前 commit，或在整理本任务分支后 squash / rebase 为一个 commit。
- 同步主干使用 rebase，避免将 `main` merge 到任务分支产生额外 merge commit。
- 重写已经推送的任务分支后使用 `git push --force-with-lease`，先确认没有覆盖他人提交；禁止对 `main` 强推。
- 合并使用 squash merge 或 rebase merge，使主干保持线性历史。每次更新后等待 CI 对最新提交通过，再由 Ao 合并；确认任务成果合入目标分支 `main` 后，任务执行者及时清理本地和远端任务分支，包括 dev、review、临时候选分支及备份引用。清理前核实没有未交付修改或其他工作区占用，不为已完成任务长期保留或归档开发分支。

一个 commit 可以包含一到多个紧密相关的 code changes，但仍须围绕单一目的。检查器和单测的分离不要求分成多个 commits。

GitHub 仓库启用 **Automatically delete head branches**，在 PR 合并后自动删除远端审核分支；对应 dev、本地分支和临时引用仍由任务执行者核实并清理。[GitHub 自动删除分支说明](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/managing-the-automatic-deletion-of-branches)（核实于 2026-09-07）。

## Commit message

提交消息遵循 Conventional Commits，统一使用无 scope 的格式：`<type>[!]: <description>`，通常为 `type: description`。type 使用英文；description 以中文为主，保留必要英文术语，清楚说明变更目的。

- 常用 type：`feat` 新功能、`fix` 修复、`docs` 文档、`refactor` 重构、`test` 测试、`ci` CI 配置、`build` 构建与依赖、`chore` 日常维护。
- Skill 是本仓库的核心功能，`SKILL.md` 中的触发条件、指令和示例都是功能实现的一部分。新增或增强 skill 使用 `feat`，修正 skill 的行为或指令错误使用 `fix`，保持行为不变的内部整理使用 `refactor`；不能仅因源文件是 Markdown 就归为 `docs`。
- `docs` 用于 README、使用说明、开发约定等说明文档。功能变更及配套说明在同一提交中时，按功能变更选择 type。
- 不使用括号中的 scope，不维护 scope 标签系统；需要说明影响范围时，直接写入 description。
- 不兼容变更使用 `!` 或 `BREAKING CHANGE:` footer，并说明影响和迁移方式。
- 示例：`feat: 增加代码审查 skill`、`fix: 修正审查 skill 的触发条件`、`docs: 更新本地开发设置说明`、`ci: 检查 PR 仅包含一个 commit`。

PR 标题沿用最终 commit 的标题；squash merge 时核对最终提交消息，保持同一格式。当前通过开发流程与评审遵守此约定，暂不额外引入 commitlint 或 CI job。

## 架构与实现约定

- 共享规则与能力只维护一份；编排 skills 调用基础 skills，不复制其标准。
- Plugins 负责包装；分发时包含或显式安装依赖，不假定仓库相对路径在运行环境可用。
- 配置保留软件原生格式，落地前核实工具版本、官方规范与加载方式。
- Agent 使用的 hooks 统一使用 Rust 开发，以便构建和分发独立二进制；出现具体需求后再创建 crate。Git hooks 属于仓库维护脚本，可使用 shell / Python。
- 编辑源文件不等于安装到本机。安装脚本应预览目标、检测冲突、可重复运行并保留恢复方法，详见 `docs/architecture.md`。

## 新增与修改

先确定组件的使用场景和维护源，再选择目录。组件说明至少写清用途、使用入口、适用工具或版本、依赖和当前状态。纯笔记无需套用程序组件的全部要求。

从真实需求提取共享内容；只使用一次的逻辑留在原组件附近。不要因为可以抽象就增加注册中心、继承系统或构建框架。

## 验证

| 变更 | 最小有用验证 |
| --- | --- |
| 文档、指令、模板 | 阅读完整上下文，检查链接、冲突规则与未替换占位符 |
| Skill、prompt | 用代表性任务检查触发、输出及重要失败情况；记录模型与日期 |
| 软件配置 | 原生格式解析，通过目标工具的检查或实际加载验证 |
| 安装、同步脚本 | 在临时目标验证预览、重复执行、冲突与恢复 |
| Rust hook | 验证事件输入、输出约定、异常输入、超时和失败语义 |

未运行的检查明确标注，不将语法通过写成行为验证成功。外部软件的配置行为应保留官方来源和核实日期。

## 知识沉淀

经验笔记区分观察、解释与建议。记录适用环境、日期、关键示例与限制；避免把一次结果直接提升为普遍规则。稳定结论可以转为指令或 skill，原笔记保留背景并指向维护源。

有长期影响且存在实际取舍的决定，记录在 `docs/decisions/NNNN-topic.md`：背景、决定、理由、影响。日常修改无需另写决策文档。

## 命名与文档

- Skill 名称使用下文规定的 `ao-` 前缀，其余路径使用 lowercase kebab-case；标准文件名及 Python 测试模块的 `test_*.py` 命名除外。
- 说明文档优先使用中文，代码标识符和文件名使用英文；指令语言按使用对象选择。
- `README.md` 是人类入口，`AGENTS.md` 是 Agent 入口；共同流程只在本文件维护。`CLAUDE.md` 保持指向 `AGENTS.md` 的相对符号链接。

## Git 与本机状态

提交可复现的源文件、示例、必要的依赖锁文件。不要提交凭据、会话、执行日志、构建产物与本机状态。`.gitignore` 只是辅助，提交前仍要查看差异。

每次 change 围绕一个可理解的目的。PR / CR / MR 是 review 活动，可以包含一到多个 code changes；不要用“写一个 PR”代指实现代码。

本项目使用 private GitHub repo；创建时设置为 private，后续维护保持私有。私有仓库同样不保存凭据、会话、私密日志或机器状态。

远程仓库为 `https://github.com/aolast/ao-agents.git`。在已配置 GitHub 身份认证的环境中使用 `git clone https://github.com/aolast/ao-agents.git` 获取仓库，然后按本文件流程维护。

## Skill 命名与检查

所有本仓库维护的 skill 统一命名为 `ao-<lowercase-kebab-case>`，例如 `ao-code-review`。目录名与 `SKILL.md` YAML frontmatter 的 `name` 必须完全相同，总长度不超过 64 字符。`ao-` 是固定命名空间，后缀必须非空，使用小写字母、数字及分隔词的单个连字符。

零散 skill 直接放在 `agents/skills/<skill 名称>/`，有实际分组需要时再增加分类目录。软件开发放在 `agents/skills/software-development/`，其 skills 统一以 `ao-sdlc-` 开头；使用 `<活动目录>/<skill 名称>/SKILL.md`。分类目录不需要 skill 前缀，也不直接放 `SKILL.md`；只有实际 skill 目录需要与 `name` 匹配。

`agents/skills/` 内只维护一份 [README 目录](agents/skills/README.md)，目录区块由脚本读取各 skill 的 frontmatter `name` 与 `description` 生成，不手工维护目录行，也不为领域、活动或单个 skill 另建 README。标记区块外的分类说明仍在 README 中维护。具体方法和边界在对应 `SKILL.md` 维护，共同维护规则放在本文件。

根据各 skill 的名称和描述选择当前需要的能力，不设置通用的 overview 路由层。需要分发编排能力时，确保目标环境能按名称找到被引用的 skills；源码嵌套不保证工具自动发现，安装方式与加载行为需按目标宿主验证。

检查器扫描 Git 暂存区中所有 `SKILL.md`，包括领域子目录及 plugins 内的 skills。它检查本次将提交的内容，避免工作区里尚未暂存的修复掩盖错误；删除的文件不再检查。目前不提交第三方原版 skills，外部依赖通过安装管理。`SKILL.md` 使用普通文件；插件分发时从维护源打包。

该命名满足 [Agent Skills 标准](https://agentskills.io/specification) 的名称字符与长度约束。检查器只验证命名及必要的 frontmatter 结构，其他字段与宿主加载行为仍按组件需求验证。安装时遇到同名 skill 应报告冲突，不自动覆盖。

Skill 的 `description`、执行步骤和检查标准以中文为主，保留 code change、scope、API 等必要英文术语。名称、路径、YAML 字段名、代码、命令与原始报错保持英文或原文；不维护逐段中英文重复副本。

## 本地开发设置

维护脚本使用 Python 3.12+ 和 Git，Git hook 支持 macOS / Linux。首次 clone 后执行：

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements-dev.txt
python scripts/install-git-hooks.py
python scripts/install-git-hooks.py --apply
```

安装器默认预览，只修改当前仓库的 `core.hooksPath`；发现已有 hooks 或不同路径则停止，保留已有设置。重复执行不重复安装。撤销本次设置使用 `git config --local --unset core.hooksPath`。Git clone 不会自动启用自定义 hooks，每份 checkout 需要设置一次。

提交前 `pre-commit` 先检查 skill 命名，再从暂存区生成 README 目录并自动暂存该文件。生成仅覆盖目录标记区块，保留说明文字；若目录需要更新且 README 还有未暂存修改，hook 停止，先暂存或另行保存这些修改再提交。需要生成目录时，使用 `git add` 后的普通 `git commit` 或 `git commit -a`；带路径参数的提交使用临时暂存区，hook 会在写入前停止，避免提交后主暂存区仍保留旧目录。

手动生成同样会更新并暂存 README：

```sh
python scripts/generate-skill-catalog.py
```

手动验证与 CI 使用以下命令；目录检查不会修改文件或暂存区：

```sh
python -m unittest discover -s scripts/tests -v
python scripts/check-skill-names.py
python scripts/generate-skill-catalog.py --check
```

先 `git add` 待检查文件。命名检查读取整个暂存区并递归覆盖领域目录及 plugins；目录生成只读取 `agents/skills/` 下已暂存的 skills，按路径排序，删除的 skill 不再出现。CI 检查已提交目录与 frontmatter 是否一致；单测覆盖生成结果、暂存区边界与 hook 行为。Git hook 可被跳过，服务端必需的 CI 检查才是合并关卡。

## CI 与 main 保护

`.github/workflows/ci.yml` 在面向 `main` 的 PR 及合并后的 `main` push 上运行。只保留两个必要 job：`skill-names` 运行脚本单测、仓库实际命名检查及目录一致性检查；`pr-single-commit` 检查 PR 事件中的 commit 数必须为 1。后者在 `main` push 上无需检查 PR 数量。不加路径过滤，保证每个 PR 都产生必需状态；不添加无实际部署对象的 CD、覆盖率门槛或多平台矩阵。

Agent Rust hooks 出现实际实现时，再增加对应 crate 的必要测试和所需平台的构建分发流程。GitHub workflow 中第三方 actions 固定到 commit SHA，升级通过 PR。

`main` 的目标保护策略保存在 `.github/main-protection.json`：必须经 PR，必须通过 GitHub Actions 的 `skill-names` 和 `pr-single-commit` 检查并跟上最新 `main`；保持线性历史；应用于管理员，禁止 force push、删除和绕过 PR。个人仓库不强制另一位 reviewer 的 approval，Ao 通过 PR 完成最终审查和合并。

**配置文件不会自动开启远程保护。** 当前连接没有仓库保护写入接口。需要在有仓库管理权限且已登录的 GitHub CLI 环境中，checkout 包含最新保护配置的分支，待对应 PR 的 CI 运行后执行：

```sh
gh api --method PUT repos/aolast/ao-agents/branches/main/protection \
  --input .github/main-protection.json
gh api repos/aolast/ao-agents/branches/main/protection
```

该命令应用完整策略；已有保护时先检查差异，避免覆盖其他规则。读取返回值核实策略实际生效，再合并本 PR。若此前未开启 GitHub Actions，在仓库 Settings → Actions → General 中启用。服务器配置变更需要写入权限，不能用修改本文件代替。

私有仓库的分支保护需要支持该功能的 GitHub 方案（个人账号通常为 Pro）；若返回方案限制，保留仓库私有并处理方案限制。[GitHub 分支保护与 API 说明](https://docs.github.com/en/rest/branches/branch-protection#update-branch-protection)（核实于 2026-09-06）。
