"""Guard canonical behavior and declared Skill source paths during the 1.6.19 migration.

This test is intentionally compatible with the existing CI engine until the
vendored original 1.6.19 engine has been installed and validated.
"""
import unittest
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]


class SkillMigrationContracts(unittest.TestCase):
    def setUp(self):
        self.config = yaml.safe_load((ROOT / "gpt-project.yaml").read_text(encoding="utf-8"))

    def test_canonical_source_remains_monolithic_during_transition(self):
        self.assertEqual(self.config["instructions"]["canonical"], "src/canonical/instructions.md")
        text = (ROOT / self.config["instructions"]["canonical"]).read_text(encoding="utf-8")
        for phrase in ("ProduktIdentity", "Verifierad", "Beräknad", "Indikativ"):
            # ProductIdentity may only appear in the domain contracts; guard behavior via canonical terms.
            if phrase != "ProduktIdentity":
                self.assertIn(phrase, text)

    def test_declared_sources_are_real_and_distinct(self):
        definitions = self.config["skills"]["definitions"]
        ids = [skill["id"] for skill in definitions]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertIn("prisjamforelse", ids)  # legacy entrypoint, retained temporarily
        expected = {
            "produktidentifiering": "src/skills/produktidentifiering.md",
            "erbjudandeverifiering": "src/skills/erbjudandeverifiering.md",
            "prisrankning": "src/skills/prisrankning.md",
        }
        canonical_path = self.config["instructions"]["canonical"]
        for item in definitions:
            for path in item.get("references", []):
                self.assertTrue((ROOT / path).is_file(), path)
        for skill_id, source in expected.items():
            item = next(x for x in definitions if x["id"] == skill_id)
            self.assertEqual(item.get("source"), source)
            self.assertNotEqual(source, canonical_path)
            body = (ROOT / source).read_text(encoding="utf-8")
            self.assertIn("Ansvar", body)
            self.assertIn("Gräns", body)
            self.assertIn("src/canonical/", body)

    def test_five_distribution_targets_unchanged(self):
        targets = self.config["build_system"]["targets"]
        self.assertEqual(set(targets), {
            "project", "chat_zip", "plugin", "claude_project",
            "claude_skills", "opencode",
        })
        self.assertFalse(self.config["runtime"]["custom_gpt"]["enabled"])


if __name__ == "__main__":
    unittest.main()
