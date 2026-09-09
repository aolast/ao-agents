import importlib.util
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

import yaml


SCRIPTS = Path(__file__).resolve().parents[1]
SCRIPT = SCRIPTS / "generate-skill-catalog.py"
spec = importlib.util.spec_from_file_location("generate_skill_catalog", SCRIPT)
catalog = importlib.util.module_from_spec(spec)
spec.loader.exec_module(catalog)

README = ("# Intro\n\nManual introduction.\n\n" + catalog.START
          + "\n\nold catalog\n\n" + catalog.END + "\n\nManual footer.\n")


class SkillCatalogTest(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        self.git("init", "-q")
        self.git("config", "user.name", "Test")
        self.git("config", "user.email", "test@example.invalid")
        self.git("config", "commit.gpgSign", "false")
        self.git("config", "core.hooksPath", ".git/no-hooks")
        self.readme = self.root / catalog.README
        self.readme.parent.mkdir(parents=True)
        self.readme.write_text(README)
        for relative in ("check-skill-names.py", "generate-skill-catalog.py",
                         "git-hooks/pre-commit"):
            target = self.root / "scripts" / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(SCRIPTS / relative, target)
        self.git("add", ".")

    def git(self, *args):
        return subprocess.check_output(["git", *args], cwd=self.root)

    def index_readme(self):
        return self.git("show", ":" + catalog.README).decode()

    def skill(self, name, description="First description", category="", stage=True):
        path = self.readme.parent / category / name / "SKILL.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("---\n" + yaml.safe_dump(
            {"name": name, "description": description}, allow_unicode=True
        ) + "---\nBody\n")
        if stage:
            self.git("add", str(path))
        return path

    def test_uses_staged_frontmatter_and_formats_nested_entries(self):
        path = self.skill("ao-second", "多行 | <literal>\n第二行", "category space")
        self.skill("ao-first")
        self.skill("ao-untracked", stage=False)
        path.write_text(path.read_text().replace("第二行", "unstaged description"))
        indexed_skill = self.git("show", ":agents/skills/category space/ao-second/SKILL.md")
        self.assertTrue(catalog.update_catalog(self.root))
        result = self.index_readme()
        self.assertIn("[ao-second](category%20space/ao-second/SKILL.md)", result)
        self.assertIn("多行 &#124; &lt;literal&gt; 第二行", result)
        self.assertLess(result.index("[ao-first]"), result.index("[ao-second]"))
        self.assertNotIn("ao-untracked", result)
        self.assertNotIn("unstaged description", result)
        self.assertEqual(indexed_skill, self.git(
            "show", ":agents/skills/category space/ao-second/SKILL.md"))
        self.assertIn("unstaged description", path.read_text())

    def test_preserves_manual_text_and_is_idempotent(self):
        self.skill("ao-first")
        self.assertTrue(catalog.update_catalog(self.root))
        result = self.index_readme()
        self.assertTrue(result.startswith("# Intro\n\nManual introduction.\n\n"))
        self.assertTrue(result.endswith("\n\nManual footer.\n"))
        self.assertEqual(result, self.readme.read_text())
        self.assertFalse(catalog.update_catalog(self.root))
        self.assertEqual(result, self.index_readme())

    def test_staged_add_rename_and_delete(self):
        path = self.skill("ao-old")
        catalog.update_catalog(self.root)
        renamed = path.parent.with_name("ao-new")
        self.git("mv", str(path.parent), str(renamed))
        self.skill("ao-new")
        catalog.update_catalog(self.root)
        self.assertIn("[ao-new](ao-new/SKILL.md)", self.index_readme())
        self.assertNotIn("ao-old", self.index_readme())
        self.git("rm", "-q", "-f", str(renamed / "SKILL.md"))
        catalog.update_catalog(self.root)
        self.assertNotIn("[ao-new]", self.index_readme())

    def test_check_reads_index_even_when_worktree_catalog_is_fixed(self):
        self.skill("ao-first")
        catalog.update_catalog(self.root)
        self.skill("ao-first", "Second description")
        self.readme.write_text(self.readme.read_text().replace(
            "First description", "Second description"))
        old_index = self.index_readme()
        worktree = self.readme.read_bytes()
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "--check"], cwd=self.root, capture_output=True
        )
        self.assertNotEqual(0, result.returncode)
        self.assertIn(b"catalog is stale", result.stderr)
        self.assertEqual(old_index, self.index_readme())
        self.assertEqual(worktree, self.readme.read_bytes())
        self.git("add", catalog.README)
        self.assertFalse(catalog.update_catalog(self.root, check=True))

    def test_refuses_unstaged_readme_changes_without_mutating_either_copy(self):
        self.skill("ao-first")
        self.readme.write_text(README + "Unstaged manual note.\n")
        old_index = self.index_readme()
        worktree = self.readme.read_bytes()
        with self.assertRaisesRegex(ValueError, "unstaged changes"):
            catalog.update_catalog(self.root)
        self.assertEqual(old_index, self.index_readme())
        self.assertEqual(worktree, self.readme.read_bytes())
        # A current indexed catalog needs no write and can coexist with manual edits.
        self.git("add", catalog.README)
        catalog.update_catalog(self.root)
        self.readme.write_text(self.readme.read_text() + "Another unstaged note.\n")
        worktree = self.readme.read_bytes()
        self.assertFalse(catalog.update_catalog(self.root))
        self.assertEqual(worktree, self.readme.read_bytes())

    def test_invalid_description_fails_before_any_write(self):
        path = self.skill("ao-first")
        original = self.index_readme()
        invalid = ("", "description: ''", "description: 42", "description: [item]",
                   "description: one\ndescription: two", "description: [")
        for description in invalid:
            with self.subTest(description=description):
                path.write_text(f"---\nname: ao-first\n{description}\n---\nBody\n")
                self.git("add", str(path))
                with self.assertRaises(ValueError):
                    catalog.update_catalog(self.root)
                self.assertEqual(original, self.index_readme())
                self.assertEqual(README, self.readme.read_text())

    def test_requires_unambiguous_catalog_markers(self):
        for content in ("no markers", catalog.END + "\n" + catalog.START,
                        README + catalog.START + "\n", README + catalog.END + "\n"):
            with self.subTest(content=content):
                with self.assertRaisesRegex(ValueError, "catalog markers"):
                    catalog.replace_catalog(content, "table")

    def test_rejects_indexed_symlinks_and_worktree_readme_symlinks(self):
        path = self.readme.parent / "ao-link" / "SKILL.md"
        path.parent.mkdir()
        path.symlink_to("missing.md")
        self.git("add", str(path))
        with self.assertRaisesRegex(ValueError, "resolved regular file"):
            catalog.update_catalog(self.root)
        self.git("rm", "-q", "-f", str(path))
        target = self.root / "other.md"
        target.write_text(README)
        self.readme.unlink()
        self.readme.symlink_to(target)
        with self.assertRaisesRegex(ValueError, "symlink"):
            catalog.update_catalog(self.root)
        self.assertEqual(README, target.read_text())
        self.assertEqual(README, self.index_readme())

    def test_hook_commits_catalog_without_staging_unrelated_or_unstaged_content(self):
        path = self.skill("ao-first")
        path.write_text(path.read_text().replace("First description", "Unstaged description"))
        note = self.root / "note.txt"
        note.write_text("Untracked note\n")
        self.git("config", "core.hooksPath", "scripts/git-hooks")
        self.git("commit", "-qm", "Add skill")
        committed = self.git("show", "HEAD:" + catalog.README).decode()
        self.assertIn("First description", committed)
        self.assertNotIn("Unstaged description", committed)
        self.assertEqual(committed, self.index_readme())
        self.assertEqual(committed, self.readme.read_text())
        self.assertIn("Unstaged description", path.read_text())
        self.assertNotIn(b"note.txt", self.git("ls-tree", "-r", "--name-only", "HEAD"))
        self.assertFalse(catalog.update_catalog(self.root, check=True))

    def test_path_limited_commit_stops_before_mutating_catalog(self):
        path = self.skill("ao-first")
        note = self.root / "note.txt"
        note.write_text("Base\n")
        self.git("add", str(note))
        catalog.update_catalog(self.root)
        self.git("commit", "-qm", "Base")
        head = self.git("rev-parse", "HEAD")
        original = self.index_readme()
        note.write_text("Keep staged\n")
        self.git("add", str(note))
        self.skill("ao-first", "Selected description", stage=False)
        self.git("config", "core.hooksPath", "scripts/git-hooks")
        result = subprocess.run(
            ["git", "commit", "-qm", "Selected skill", "--only", str(path)],
            cwd=self.root, capture_output=True
        )
        self.assertNotEqual(0, result.returncode)
        self.assertIn(b"without path arguments", result.stderr)
        self.assertEqual(head, self.git("rev-parse", "HEAD"))
        self.assertEqual(b"Keep staged\n", self.git("show", ":note.txt"))
        self.assertEqual(original, self.index_readme())
        self.assertEqual(original, self.readme.read_text())

    def test_hook_supports_commit_all(self):
        self.skill("ao-first")
        catalog.update_catalog(self.root)
        self.git("commit", "-qm", "Base")
        self.skill("ao-first", "Commit all description", stage=False)
        self.git("config", "core.hooksPath", "scripts/git-hooks")
        self.git("commit", "-qam", "Update all")
        committed = self.git("show", "HEAD:" + catalog.README).decode()
        self.assertIn("Commit all description", committed)
        self.assertEqual(committed, self.index_readme())
        self.assertEqual(committed, self.readme.read_text())


if __name__ == "__main__":
    unittest.main()
