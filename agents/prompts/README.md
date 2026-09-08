# Prompts

统一维护长期指令与直接使用的任务提示词。

| 路径 | 内容 |
| --- | --- |
| [AO-AGENTS.md](AO-AGENTS.md) | Ao 的 user-level `AGENTS.md` 指令源 |
| `managed/` | 支持集中管理机制的软件所需指令源 |
| `user/` | 跨项目的个人指令源 |
| `project/` | 项目级指令模板 |
| `tasks/` | 直接使用的任务提示词 |
| `fragments/` | 有实际复用需求的共享规则片段 |

子目录按需创建，当前维护 Ao 的个人指令源与项目模板。模板使用 `.md.template` 后缀，避免被误认为当前生效的指令。

长期指令写明适用工具、范围与加载方式；任务提示词写明必要输入和期望输出。需要可复用流程及配套资源时使用 `agents/skills/`，避免复制 skill 中已有标准。

共享片段需要明确读取或在分发时展开，Markdown 链接不保证内容自动加载。managed、user、project 表达部署意图，实际路径与优先级按目标工具核实。

根目录 `AGENTS.md` 是本仓库的 Agent 入口，不作为对外分发模板。

`AO-AGENTS.md` 是 Ao 跨项目使用的 user-level `AGENTS.md` 指令源，面向支持用户级 `AGENTS.md` 的 coding agent。它记录个人 Agent 相关资产的维护仓库、`ao-` skill 命名前缀，以及建议默认读取 `ao-vocabulary` 的约定。

全文使用 `<ao-user-level-agents-instructions>` 标签标识来源与边界，开头说明用途和编号条目的写法，具体原则放在 `<principles>` 内。使用时按目标工具的加载方式部署为用户级 `AGENTS.md`；当前仅维护源文件，尚未安装到用户配置位置。
