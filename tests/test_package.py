import json
import re
import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills/proof-driven-engineering"


class PackageTests(unittest.TestCase):
    def test_manifest_can_be_loaded_by_a_skill_consumer(self):
        text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        _, frontmatter, body = text.split("---", 2)
        metadata = yaml.safe_load(frontmatter)
        self.assertEqual(metadata["name"], SKILL.name)
        self.assertIsInstance(metadata["description"], str)
        self.assertTrue(0 < len(metadata["description"]) <= 1024)
        self.assertTrue(body.strip())

    def test_ui_metadata_enables_automatic_discovery(self):
        metadata = yaml.safe_load((SKILL / "agents/openai.yaml").read_text(encoding="utf-8"))
        self.assertIs(metadata["policy"]["allow_implicit_invocation"], True)
        interface = metadata["interface"]
        self.assertTrue(25 <= len(interface["short_description"]) <= 64)
        self.assertIn("$" + SKILL.name, interface["default_prompt"])

    def test_local_references_resolve_within_the_distribution(self):
        for source in ROOT.rglob("*.md"):
            if ".git" in source.parts or ".local" in source.parts:
                continue
            for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", source.read_text(encoding="utf-8")):
                if "://" in target or target.startswith("#"):
                    continue
                with self.subTest(source=source.relative_to(ROOT), target=target):
                    path = (source.parent / target.split("#", 1)[0]).resolve()
                    self.assertTrue(path.is_relative_to(ROOT))
                    self.assertTrue(path.exists())

    def test_behavioral_evals_have_observable_acceptance(self):
        cases = json.loads((ROOT / "evals/cases.json").read_text(encoding="utf-8"))
        ids = [case["id"] for case in cases]
        self.assertEqual(len(ids), len(set(ids)))
        for case in cases:
            with self.subTest(case=case["id"]):
                self.assertTrue(case["prompt"].strip())
                self.assertTrue(case["must_pass"])
                self.assertTrue(case["must_not"])

    def test_fixture_and_oracle_paths_resolve_within_evaluation_suite(self):
        root = ROOT / "evals"
        cases = json.loads((root / "cases.json").read_text(encoding="utf-8"))
        for case in cases:
            for key in ("fixture", "oracle"):
                if key not in case:
                    continue
                with self.subTest(case=case["id"], key=key):
                    path = (root / case[key]).resolve()
                    self.assertTrue(path.is_relative_to(root))
                    self.assertTrue(path.is_file() if key == "oracle" else path.is_dir())


if __name__ == "__main__":
    unittest.main()
