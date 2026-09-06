# Ao Agents

Ao 个人使用 AI Agents 的知识、经验、指令、配置与自动化仓库，以 private GitHub repo 形式维护。

## 阅读入口

- **人类**：从本文件了解用途与目录；开发和维护前阅读 [DEVELOPING.md](DEVELOPING.md)。
- **Agents**：从 [AGENTS.md](AGENTS.md) 进入，同样遵循 `DEVELOPING.md`。`CLAUDE.md` 是指向 `AGENTS.md` 的符号链接。
- **架构与经验**：查看 [docs](docs/README.md)。

## 目录

| 路径 | 职责 |
| --- | --- |
| `agents/prompts/` | 长期指令、任务提示词、managed / user 指令与项目模板 |
| `agents/skills/` | 基础 skills 与顶层编排 skills |
| `agents/plugins/` | 插件包装、清单与分发 |
| `agents/configs/` | 各软件的权限、模型、插件、hooks 等原生配置 |
| `agents/hooks/` | 自制 hooks，实现需要编译时使用 Rust |
| `scripts/` | 本仓库的安装、同步、检查与维护脚本 |
| `workflows/` | 个人 AI 工作流及其专属代码与配置 |
| `docs/` | 架构、知识、经验、实验与设计决策 |

仓库文件是维护源，目标软件的加载位置由组件安装说明确定。目录存在不代表已经安装或生效。

## 当前状态

已建立目录骨架、主干开发流程、项目指令模板、ao- 命名检查、Git hook 与最小 CI（命名和 PR 单 commit 检查）。分支保护配置和启用步骤见 `DEVELOPING.md`。尚未实现可安装插件、具体软件配置、hooks 或工作流。远程仓库：[aolast/ao-agents](https://github.com/aolast/ao-agents)，保持 private。

下一步选择首个实际使用的 Agent 软件，落地个人指令和原生配置，再按需求增加 skills、安装脚本与 hooks。
