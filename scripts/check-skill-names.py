#!/usr/bin/env python3
"""Validate skill names from the Git index, shared by pre-commit and CI."""

import re
import subprocess
import sys
from pathlib import Path, PurePosixPath

import yaml


NAME_PATTERN = re.compile(r"ao__[a-z0-9]+(?:-[a-z0-9]+)*\Z")


def validate_skill(path, content):
    """Check the directory and exactly one string-valued frontmatter name."""
    errors = []
    directory = PurePosixPath(path).parent.name
    if not NAME_PATTERN.fullmatch(directory) or len(directory) > 64:
        errors.append("directory must be ao__<lowercase-kebab-case>, at most 64 characters")
    lines = content.splitlines()
    if not lines or lines[0] != "---":
        return errors + ["SKILL.md must start with YAML frontmatter"]
    try:
        end = lines.index("---", 1)
    except ValueError:
        return errors + ["frontmatter is missing its closing ---"]
    try:
        node = yaml.compose("\n".join(lines[1:end]), Loader=yaml.SafeLoader)
    except yaml.YAMLError as exc:
        return errors + [f"invalid YAML: {exc}"]
    if not isinstance(node, yaml.MappingNode):
        return errors + ["frontmatter must be a mapping"]
    names = [value for key, value in node.value
             if isinstance(key, yaml.ScalarNode) and key.value == "name"]
    if len(names) != 1:
        return errors + ["frontmatter must contain exactly one name"]
    name = names[0]
    if not isinstance(name, yaml.ScalarNode) or name.tag != "tag:yaml.org,2002:str":
        return errors + ["name must be a string"]
    if not NAME_PATTERN.fullmatch(name.value) or len(name.value) > 64:
        errors.append("name must be ao__<lowercase-kebab-case>, at most 64 characters")
    if name.value != directory:
        errors.append("name must match its parent directory")
    return errors


def check_index(root):
    """Read indexed blobs, so an unstaged fix cannot conceal a bad commit."""
    listing = subprocess.check_output(
        ["git", "ls-files", "--stage", "-z"], cwd=root
    )
    errors = []
    count = 0
    for record in listing.split(b"\0"):
        if not record:
            continue
        metadata, raw_path = record.split(b"\t", 1)
        path = raw_path.decode("utf-8")
        if PurePosixPath(path).name != "SKILL.md":
            continue
        count += 1
        mode, sha, stage = metadata.decode("ascii").split()
        if stage != "0" or mode not in ("100644", "100755"):
            errors.append(f"{path}: SKILL.md must be a resolved regular file in the index")
            continue
        data = subprocess.check_output(["git", "cat-file", "blob", sha], cwd=root)
        try:
            content = data.decode("utf-8")
        except UnicodeDecodeError:
            errors.append(f"{path}: SKILL.md must be UTF-8")
            continue
        errors.extend(f"{path}: {error}" for error in validate_skill(path, content))
    return count, errors


def main():
    try:
        root = Path(subprocess.check_output(
            ["git", "rev-parse", "--show-toplevel"], text=True
        ).strip())
        count, errors = check_index(root)
    except (OSError, UnicodeError, subprocess.CalledProcessError) as exc:
        print(f"Cannot check skill names: {exc}", file=sys.stderr)
        return 1
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print(f"Skill names OK ({count} indexed skills checked).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
