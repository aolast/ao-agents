#!/usr/bin/env python3
"""Opt in to this repository's hooks without replacing existing hooks."""

import argparse
import subprocess
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true", help="apply the displayed local setting")
    args = parser.parse_args()
    root = Path(subprocess.check_output(
        ["git", "rev-parse", "--show-toplevel"], text=True
    ).strip())
    target = "scripts/git-hooks"
    current = subprocess.run(
        ["git", "config", "--get", "core.hooksPath"], cwd=root, text=True, capture_output=True
    )
    if current.returncode not in (0, 1):
        raise SystemExit(current.stderr)
    if current.returncode == 0:
        if current.stdout.strip() == target:
            print("Repository hooks already enabled.")
            return
        raise SystemExit("Existing core.hooksPath detected; integrate manually before installing.")
    hooks_path = Path(subprocess.check_output(
        ["git", "rev-parse", "--git-path", "hooks"], cwd=root, text=True
    ).strip())
    if not hooks_path.is_absolute():
        hooks_path = root / hooks_path
    if hooks_path.exists() and any(p.name != "README" and not p.name.endswith(".sample")
                                   for p in hooks_path.iterdir()):
        raise SystemExit("Existing Git hooks detected; integrate manually before installing.")
    if not (root / target / "pre-commit").is_file():
        raise SystemExit("Missing repository pre-commit hook.")
    print(f"Set repository-local core.hooksPath = {target}")
    if args.apply:
        subprocess.run(["git", "config", "--local", "core.hooksPath", target], cwd=root, check=True)
        print("Enabled. Restore with: git config --local --unset core.hooksPath")
    else:
        print("Preview only. Add --apply to install.")


if __name__ == "__main__":
    main()
