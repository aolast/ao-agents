# Skills

按领域维护可复用的 Agent skills，允许分类子目录。实际 skill 目录包含 `SKILL.md`，以 `ao-` 开头，目录名与 frontmatter 的 `name` 一致；分类目录不受 skill 前缀约束。

| 领域 | 入口 |
| --- | --- |
| 软件开发 | [software-development](software-development/README.md)，11 个 `ao-sdlc-` skills |

领域 README 维护职责、边界和组织方式；运行时入口 skill 负责按任务选择方法。共享标准只维护一份，组合调用不构成固定的层级或强制流水线。

新增领域或环境专项内容时按实际需求建立目录；源码嵌套不代表宿主自动递归发现。分发时包含所引用的 skills，验证安装布局和依赖解析。

命名、语言与维护流程遵循 [DEVELOPING.md](../../DEVELOPING.md#skill-命名与检查)。当前内容为仓库中的初版源码，尚未安装到特定 Agent 软件。
