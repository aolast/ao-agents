#!/usr/bin/env python3
"""Generate and stage the skills README catalog from indexed frontmatter."""

import argparse
import html
from pathlib import Path, PurePosixPath
import subprocess
import sys
from urllib.parse import quote

import yaml


README = "agents/skills/README.md"
START = "<!-- BEGIN GENERATED SKILL CATALOG -->"
END = "<!-- END GENERATED SKILL CATALOG -->"


def indexed_sources(root):
    """Only read blobs that will be committed, including staged adds and deletions."""
    listing = subprocess.check_output(
        ["git", "ls-files", "--stage", "-z", "--", "agents/skills/"], cwd=root
    )
    sources = {}
    for record in listing.split(b"\0"):
        if not record:
            continue
        metadata, raw_path = record.split(b"\t", 1)
        path = raw_path.decode("utf-8")
        if path != README and PurePosixPath(path).name != "SKILL.md":
            continue
        mode, sha, stage = metadata.decode("ascii").split()
        if stage != "0" or mode not in ("100644", "100755"):
            raise ValueError(f"{path}: must be a resolved regular file in the index")
        data = subprocess.check_output(["git", "cat-file", "blob", sha], cwd=root)
        try:
            sources[path] = data.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError(f"{path}: must be UTF-8") from exc
    if README not in sources:
        raise ValueError(f"{README}: must exist in the index")
    return sources


def frontmatter_fields(path, content):
    """Extract one nonempty string for each displayed field."""
    lines = content.splitlines()
    if not lines or lines[0] != "---":
        raise ValueError(f"{path}: must start with YAML frontmatter")
    try:
        end = lines.index("---", 1)
    except ValueError as exc:
        raise ValueError(f"{path}: frontmatter is missing its closing ---") from exc
    try:
        node = yaml.compose("\n".join(lines[1:end]), Loader=yaml.SafeLoader)
    except yaml.YAMLError as exc:
        raise ValueError(f"{path}: invalid YAML: {exc}") from exc
    if not isinstance(node, yaml.MappingNode):
        raise ValueError(f"{path}: frontmatter must be a mapping")
    fields = {}
    for field in ("name", "description"):
        values = [value for key, value in node.value
                  if isinstance(key, yaml.ScalarNode) and key.value == field]
        if len(values) != 1:
            raise ValueError(f"{path}: frontmatter must contain exactly one {field}")
        value = values[0]
        if (not isinstance(value, yaml.ScalarNode)
                or value.tag != "tag:yaml.org,2002:str" or not value.value.strip()):
            raise ValueError(f"{path}: {field} must be a nonempty string")
        fields[field] = value.value
    return fields


def cell(value):
    # Keep multiline descriptions and literal pipes/HTML within a single table cell.
    return html.escape(" ".join(value.split()), quote=False).replace("|", "&#124;")


def render_catalog(sources):
    rows = ["| Skill | 说明 |", "| --- | --- |"]
    for path in sorted(sources):
        if path == README:
            continue
        fields = frontmatter_fields(path, sources[path])
        target = PurePosixPath(path).relative_to("agents/skills").as_posix()
        rows.append(f"| [{cell(fields['name'])}]({quote(target, safe='/')})"
                    f" | {cell(fields['description'])} |")
    return "\n".join(rows)


def replace_catalog(readme, table):
    lines = readme.splitlines(keepends=True)
    starts = [i for i, line in enumerate(lines) if line.rstrip("\r\n") == START]
    ends = [i for i, line in enumerate(lines) if line.rstrip("\r\n") == END]
    if len(starts) != 1 or len(ends) != 1 or starts[0] >= ends[0]:
        raise ValueError(f"{README}: requires one ordered pair of catalog markers")
    before = "".join(lines[:starts[0] + 1]).rstrip("\r\n")
    after = "".join(lines[ends[0]:])
    return f"{before}\n\n{table}\n\n{after}"


def update_catalog(root, check=False):
    sources = indexed_sources(root)
    original = sources[README]
    expected = replace_catalog(original, render_catalog(sources))
    if expected == original:
        return False
    if check:
        raise ValueError("Skill catalog is stale; run python scripts/generate-skill-catalog.py.")
    # Path-limited commits use a temporary index whose generated entries are not
    # copied back to the real index by Git. Do not leave a staged reverse change.
    git_dir = Path(subprocess.check_output(
        ["git", "rev-parse", "--absolute-git-dir"], cwd=root, text=True
    ).strip())
    index = Path(subprocess.check_output(
        ["git", "rev-parse", "--git-path", "index"], cwd=root, text=True
    ).strip())
    if not index.is_absolute():
        index = root / index
    if index.resolve() not in ((git_dir / "index").resolve(),
                               (git_dir / "index.lock").resolve()):
        raise ValueError("catalog updates require the regular index; "
                         "stage files, then run git commit without path arguments")
    target = root / README
    for path in (root / "agents", root / "agents/skills", target):
        if path.is_symlink():
            raise ValueError(f"{README}: refusing to write through a symlink")
    if not target.is_file() or target.read_bytes() != original.encode("utf-8"):
        raise ValueError(f"{README}: has unstaged changes; stage or save them before generating")
    result = subprocess.run(["git", "diff", "--quiet", "--", README], cwd=root)
    if result.returncode == 1:
        raise ValueError(f"{README}: has unstaged changes; stage or save them before generating")
    if result.returncode:
        raise subprocess.CalledProcessError(result.returncode, result.args)
    target.write_text(expected, encoding="utf-8")
    subprocess.run(["git", "add", "--", README], cwd=root, check=True)
    return True


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true",
                        help="check indexed catalog without changing files or the index")
    args = parser.parse_args()
    try:
        root = Path(subprocess.check_output(
            ["git", "rev-parse", "--show-toplevel"], text=True
        ).strip())
        changed = update_catalog(root, check=args.check)
    except (ValueError, OSError, UnicodeError, subprocess.CalledProcessError) as exc:
        print(f"Cannot generate skill catalog: {exc}", file=sys.stderr)
        return 1
    print("Updated and staged skill catalog." if changed else "Skill catalog is up to date.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
