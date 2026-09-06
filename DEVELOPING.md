# Developing Ao Agents

本文件是人类与 Agents 共同遵守的开发、维护流程的唯一维护入口。开始工作前阅读 `README.md` 和相关目录说明；涉及边界调整时阅读 `docs/architecture.md`。

## 工作流程

1. 从最新 `main` 创建任务分支，理解需求，检查已有内容，确定受影响组件与唯一维护源。
2. 完成范围内最小且完整的变更，遵循已有结构，不预建执行器、通用配置语言或构建框架。
3. 同步更新受影响的使用说明，按下表完成与风险相称的验证。
4. 检查完整差异，提交到任务分支并创建 PR；CI 通过后由 Ao 在 PR 中决定合并。禁止直接 push 到 `main`，包括管理员。

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

- Skill 名称使用下文规定的 `ao__` 前缀，其余路径使用 lowercase kebab-case；标准文件名及 Python 测试模块的 `test_*.py` 命名除外。
- 说明文档优先使用中文，代码标识符和文件名使用英文；指令语言按使用对象选择。
- `README.md` 是人类入口，`AGENTS.md` 是 Agent 入口；共同流程只在本文件维护。`CLAUDE.md` 保持指向 `AGENTS.md` 的相对符号链接。

## Git 与本机状态

提交可复现的源文件、示例、必要的依赖锁文件。不要提交凭据、会话、执行日志、构建产物与本机状态。`.gitignore` 只是辅助，提交前仍要查看差异。

每次 change 围绕一个可理解的目的。PR / CR / MR 是 review 活动，可以包含一到多个 code changes；不要用“写一个 PR”代指实现代码。

本项目使用 private GitHub repo；创建时设置为 private，后续维护保持私有。私有仓库同样不保存凭据、会话、私密日志或机器状态。

远程仓库为 `https://github.com/aolast/ao-agents.git`。在已配置 GitHub 身份认证的环境中使用 `git clone https://github.com/aolast/ao-agents.git` 获取仓库，然后按本文件流程维护。

## Skill 命名与检查

所有本仓库维护的 skill 统一命名为 `ao__<lowercase-kebab-case>`，例如 `ao__code-review`。目录名与 `SKILL.md` YAML frontmatter 的 `name` 必须完全相同，总长度不超过 64 字符。`ao__` 是固定命名空间，后缀必须非空，使用小写字母、数字及分隔词的单个连字符。

检查器扫描 Git 暂存区中所有 `SKILL.md`，包括 plugins 内的 skills。它检查本次将提交的内容，避免工作区里尚未暂存的修复掩盖错误；删除的文件不再检查。目前不提交第三方原版 skills，外部依赖通过安装管理。`SKILL.md` 使用普通文件；插件分发时从维护源打包。

注意：这是本仓库的命名约定。[Agent Skills 标准](https://agentskills.io/specification) 的 `name` 只允许小写字母、数字和连字符，排除了下划线（核实于 2026-09-06）。因此本检查不代表通过标准规范或任意宿主的兼容性验证。接入具体工具时验证 `ao__` 支持情况；若不支持，先讨论明确的命名或分发调整，不默默重命名。

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

提交前 `pre-commit` 调用共享命名检查器。手动验证与 CI 使用相同命令：

```sh
python -m unittest discover -s scripts/tests -v
python scripts/check-skill-names.py
```

先 `git add` 待检查文件。检查器读取整个暂存区；当前没有 skills 时允许通过，由单测中的临时数据验证规则确实能拦截错误。Git hook 可被跳过，服务端必需的 CI 检查才是合并关卡。

## CI 与 main 保护

`.github/workflows/ci.yml` 在面向 `main` 的 PR 及合并后的 `main` push 上运行。初期只有一个稳定命名的 job：`skill-names`，运行命名检查器单测及仓库实际命名检查。不加路径过滤，保证每个 PR 都产生必需状态；不添加无实际部署对象的 CD、覆盖率门槛或多平台矩阵。

Agent Rust hooks 出现实际实现时，再增加对应 crate 的必要测试和所需平台的构建分发流程。GitHub workflow 中第三方 actions 固定到 commit SHA，升级通过 PR。

`main` 的目标保护策略保存在 `.github/main-protection.json`：必须经 PR，必须通过 GitHub Actions 的 `skill-names` 检查并跟上最新 `main`；应用于管理员，禁止 force push、删除和绕过 PR。个人仓库不强制另一位 reviewer 的 approval，Ao 通过 PR 完成最终审查和合并。

**配置文件不会自动开启远程保护。** 当前连接没有仓库保护写入接口。本次初始化需要在有仓库管理权限且已登录的 GitHub CLI 环境中，先 checkout 本变更分支，待本 PR 的 CI 运行后执行：

```sh
gh api --method PUT repos/aolast/ao-agents/branches/main/protection \
  --input .github/main-protection.json
gh api repos/aolast/ao-agents/branches/main/protection
```

该命令应用完整策略；已有保护时先检查差异，避免覆盖其他规则。读取返回值核实策略实际生效，再合并本 PR。若此前未开启 GitHub Actions，在仓库 Settings → Actions → General 中启用。服务器配置变更需要写入权限，不能用修改本文件代替。

私有仓库的分支保护需要支持该功能的 GitHub 方案（个人账号通常为 Pro）；若返回方案限制，保留仓库私有并处理方案限制。[GitHub 分支保护与 API 说明](https://docs.github.com/en/rest/branches/branch-protection#update-branch-protection)（核实于 2026-09-06）。
