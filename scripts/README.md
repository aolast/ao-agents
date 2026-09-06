# Scripts

存放用户直接执行的安装、同步、检查与维护脚本。选择最容易维护且适合运行环境的语言；不强制所有脚本使用 Rust。

每个脚本说明调用方法、依赖、修改目标与恢复方式。写入安装位置的脚本遵守 [架构中的安装约定](../docs/architecture.md)，并在临时目录验证冲突和重复执行。

工作流专属脚本留在工作流旁边，hook 专属启动包装留在 hook 旁边。

当前入口：

- `check-skill-names.py`：检查暂存区中的 skill 命名，由 Git hook 和 CI 共用。
- `install-git-hooks.py`：预览并显式启用本仓库 Git hooks，保留已有配置。
- `git-hooks/pre-commit`：提交前调用命名检查。
- `tests/`：检查器及 Git hook 的必要测试。

设置步骤、命名规则及 CI 约定见 [DEVELOPING.md](../DEVELOPING.md)。
