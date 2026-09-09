# Scripts

存放用户直接执行的安装、同步、检查与维护脚本。选择最容易维护且适合运行环境的语言；不强制所有脚本使用 Rust。

每个脚本说明调用方法、依赖、修改目标与恢复方式。写入安装位置的脚本遵守 [架构中的安装约定](../docs/architecture.md)，并在临时目录验证冲突和重复执行。

工作流专属脚本留在工作流旁边，hook 专属启动包装留在 hook 旁边。

当前入口：

- `check-skill-names.py`：检查暂存区中的 skill 命名，由 Git hook 和 CI 共用。
- `generate-skill-catalog.py`：从暂存区 frontmatter 生成并暂存 `agents/skills/README.md` 的目录区块；`--check` 只检查暂存区内容，供 CI 使用。
- `install-git-hooks.py`：预览并显式启用本仓库 Git hooks，保留已有配置。
- `git-hooks/pre-commit`：提交前检查命名，再自动生成并暂存 skill 目录。
- `tests/`：检查器及 Git hook 的必要测试。

生成器使用与命名检查器相同的 Python / PyYAML 环境，只更新 README 的生成标记之间的目录。撤销生成结果时按 Git 差异选择性恢复 README；修改 frontmatter 后重新生成即可更新目录。

设置步骤、命名规则及 CI 约定见 [DEVELOPING.md](../DEVELOPING.md)。
