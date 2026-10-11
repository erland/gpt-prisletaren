import json
import os
import unittest
import zipfile
from pathlib import Path
from tools.build import ROOT

VERSION = os.environ.get("GITHUB_REF_NAME", "").removeprefix("v") if os.environ.get("GITHUB_REF_TYPE") == "tag" else json.loads((ROOT/"docs/project-status.json").read_text())["version"]

@unittest.skipUnless((ROOT/'dist'/f'prisletaren-chat-{VERSION}.zip').exists(), 'Run after canonical build')
class CanonicalOutputTests(unittest.TestCase):
    def test_chat_and_plugin_archives_created(self):
        for name in (f"prisletaren-chat-{VERSION}.zip",f"prisletaren-plugin-{VERSION}.zip"):
            archive=ROOT/"dist"/name
            with self.subTest(name=name):
                self.assertTrue(archive.is_file())
                with zipfile.ZipFile(archive) as z:
                    self.assertIsNone(z.testzip())
                    self.assertEqual(len(z.namelist()),len(set(z.namelist())))
    def test_chat_canonical(self):
        with zipfile.ZipFile(ROOT/"dist"/f"prisletaren-chat-{VERSION}.zip") as z:
            self.assertEqual(z.read("assistant/instructions.md"),(ROOT/"src/canonical/instructions.md").read_bytes())
    def test_plugin_canonical(self):
        with zipfile.ZipFile(ROOT/"dist"/f"prisletaren-plugin-{VERSION}.zip") as z:
            self.assertIn((ROOT/"src/canonical/instructions.md").read_bytes(),z.read("skills/prisjamforelse/SKILL.md"))
            self.assertFalse(any(p.endswith("mcp.json") for p in z.namelist()))
            self.assertIn("plugin.json",z.namelist())
            manifest=json.loads(z.read("plugin.json"))
            self.assertEqual(manifest["extensions"]["com.openai"]["interface"]["displayName"],"Prisletaren")
            self.assertEqual(manifest["extensions"]["com.openai"]["interface"]["shortDescription"],"Jämför priser med frakt")
