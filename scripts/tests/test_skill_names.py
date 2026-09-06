import importlib.util
import os
from pathlib import Path
import subprocess
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "check-skill-names.py"
spec = importlib.util.spec_from_file_location("check_skill_names", SCRIPT)
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)


def skill(name):
    return f"---\nname: {name}\ndescription: Test fixture\n---\nBody\n"


class SkillNamesTest(unittest.TestCase):
    def test_valid_names_and_quoted_yaml(self):
        for name in ("ao-review", "ao-code-review", "ao-tool2", "ao-" + "x" * 61):
            with self.subTest(name=name):
                self.assertEqual([], checker.validate_skill(
                    f"agents/skills/{name}/SKILL.md", skill(f'"{name}" # comment')))

    def test_rejects_invalid_prefix_and_suffix(self):
        for name in ("review", "ao_review", "ao__review", "ao--review", "ao-", "ao-Review",
                     "ao-code--review", "ao-code_review", "ao-" + "x" * 62):
            with self.subTest(name=name):
                self.assertTrue(checker.validate_skill(f"agents/skills/{name}/SKILL.md", skill(name)))

    def test_name_must_match_directory(self):
        self.assertIn("name must match its parent directory", checker.validate_skill(
            "agents/skills/ao-review/SKILL.md", skill("ao-author")))

    def test_frontmatter_errors_fail_closed(self):
        for content in ("# no header", "---\nname: ao-review", "---\nname: [\n---",
                        "---\ndescription: missing name\n---", "---\nname: 123\n---",
                        "---\nname: ao-review\nname: ao-review\n---"):
            with self.subTest(content=content):
                self.assertTrue(checker.validate_skill("agents/skills/ao-review/SKILL.md", content))

    def test_index_includes_plugins_and_ignores_unstaged_fix(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subprocess.run(["git", "init", "-q", directory], check=True)
            path = root / "agents/plugins/example/skills/ao-review/SKILL.md"
            path.parent.mkdir(parents=True)
            path.write_text(skill("review"))
            subprocess.run(["git", "add", "."], cwd=root, check=True)
            path.write_text(skill("ao-review"))
            count, errors = checker.check_index(root)
            self.assertEqual(1, count)
            self.assertTrue(errors)
            subprocess.run(["git", "add", "."], cwd=root, check=True)
            self.assertEqual((1, []), checker.check_index(root))
            subprocess.run(["git", "rm", "-q", "-f", str(path)], cwd=root, check=True)
            self.assertEqual((0, []), checker.check_index(root))

    def test_pre_commit_blocks_invalid_staged_skill(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subprocess.run(["git", "init", "-q", directory], check=True)
            (root / "scripts").mkdir()
            (root / "scripts/check-skill-names.py").write_bytes(SCRIPT.read_bytes())
            path = root / "agents/skills/ao-review/SKILL.md"
            path.parent.mkdir(parents=True)
            path.write_text(skill("review"))
            subprocess.run(["git", "add", "."], cwd=root, check=True)
            hook = SCRIPT.parent / "git-hooks/pre-commit"
            result = subprocess.run(["sh", str(hook)], cwd=root, capture_output=True)
            self.assertNotEqual(0, result.returncode)
            self.assertIn(b"name must", result.stderr)
            path.write_text(skill("ao-review"))
            subprocess.run(["git", "add", "."], cwd=root, check=True)
            result = subprocess.run(["sh", str(hook)], cwd=root, capture_output=True)
            self.assertEqual(0, result.returncode, result.stderr)

    def test_symlink_skill_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subprocess.run(["git", "init", "-q", directory], check=True)
            path = root / "agents/skills/ao-review/SKILL.md"
            path.parent.mkdir(parents=True)
            os.symlink("missing.md", path)
            subprocess.run(["git", "add", "."], cwd=root, check=True)
            self.assertTrue(checker.check_index(root)[1])


if __name__ == "__main__":
    unittest.main()
