"""All peer distributions must preserve their shared canonical behavior."""
import json
import unittest
import zipfile
from pathlib import Path
from tools.build import ROOT

VERSION = "0.5.0"
EXPECTED = {
    "chat": ("assistant/instructions.md", "chatgpt_chat"),
    "plugin": ("skills/prisjamforelse/SKILL.md", "openai_plugin"),
    "custom-gpt": ("builder/instructions.md", "chatgpt_custom"),
    "claude-project": ("project/instructions.md", "claude_project"),
    "claude-skills": ("skills/prisjamforelse/SKILL.md", "claude_skills"),
    "opencode": ("AGENTS.md", "opencode"),
}

class PeerRuntimeTests(unittest.TestCase):
    def test_declared_runtime_targets(self):
        import yaml
        cfg = yaml.safe_load((ROOT/"gpt-project.yaml").read_text())
        self.assertEqual(set(cfg["build_system"]["targets"]), {"project","chat_zip","plugin","custom_gpt","claude_project","claude_skills","opencode"})
        self.assertTrue(all(cfg["runtime"][key]["enabled"] for key in ("chat_zip","plugin","custom_gpt","claude","claude_skills","opencode")))

    @unittest.skipUnless((ROOT/"build"/"opencode"/"AGENTS.md").exists(), "Run after canonical distributions build")
    def test_runtime_coverage_and_canonical_behavior(self):
        canonical = (ROOT/"src/canonical/instructions.md").read_text()
        for runtime, (entry, runtime_id) in EXPECTED.items():
            with self.subTest(runtime=runtime):
                archive = ROOT/"dist"/f"prisletaren-{runtime}-{VERSION}.zip"
                self.assertTrue(archive.is_file())
                with zipfile.ZipFile(archive) as z:
                    self.assertIsNone(z.testzip())
                    self.assertEqual(len(z.namelist()),len(set(z.namelist())))
                    self.assertIn(canonical.strip(), z.read(entry).decode("utf-8"))
                    self.assertIn("MANIFEST.json",z.namelist())
                    manifest=json.loads(z.read("MANIFEST.json"))
                    self.assertEqual(manifest["runtime_id"], "prisletaren-" + ({"chat":"chat","plugin":"plugin","custom-gpt":"custom-gpt","claude-project":"claude","claude-skills":"claude-skills","opencode":"opencode"}[runtime]))
                    self.assertFalse(any(x.endswith("mcp.json") for x in z.namelist()))

    @unittest.skipUnless((ROOT/"dist"/f"prisletaren-opencode-{VERSION}.zip").exists(), "Run after canonical build")
    def test_required_runtime_layouts(self):
        expected = {
            "custom-gpt":["builder/instructions.md","builder/capabilities.md","COMPATIBILITY.md"],
            "claude-project":["project/instructions.md","project/runtime-contract.json"],
            "claude-skills":["skills/prisjamforelse/SKILL.md","runtime-contract.json"],
            "opencode":["AGENTS.md","opencode.json","runtime-contract.json",".opencode/skills/prisjamforelse/SKILL.md"],
        }
        for runtime,names in expected.items():
            with self.subTest(runtime=runtime), zipfile.ZipFile(ROOT/"dist"/f"prisletaren-{runtime}-{VERSION}.zip") as z:
                self.assertTrue(set(names).issubset(z.namelist()))
