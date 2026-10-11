import json
import unittest
import zipfile
from pathlib import Path
from tools.build import ROOT

@unittest.skipUnless((ROOT/'dist'/'prisletaren-chat-0.5.0.zip').exists(), 'Run after canonical build')
class CanonicalOutputTests(unittest.TestCase):
    def test_chat_and_plugin_archives_created(self):
        for name in ("prisletaren-chat-0.5.0.zip","prisletaren-plugin-0.5.0.zip"):
            archive=ROOT/"dist"/name
            with self.subTest(name=name):
                self.assertTrue(archive.is_file())
                with zipfile.ZipFile(archive) as z:
                    self.assertIsNone(z.testzip())
                    self.assertEqual(len(z.namelist()),len(set(z.namelist())))
    def test_chat_canonical(self):
        with zipfile.ZipFile(ROOT/"dist"/"prisletaren-chat-0.5.0.zip") as z:
            self.assertEqual(z.read("assistant/instructions.md"),(ROOT/"src/canonical/instructions.md").read_bytes())
    def test_plugin_canonical(self):
        with zipfile.ZipFile(ROOT/"dist"/"prisletaren-plugin-0.5.0.zip") as z:
            self.assertIn((ROOT/"src/canonical/instructions.md").read_bytes(),z.read("skills/prisjamforelse/SKILL.md"))
            self.assertFalse(any(p.endswith("mcp.json") for p in z.namelist()))
            self.assertIn("plugin.json",z.namelist())
            manifest=json.loads(z.read("plugin.json"))
            self.assertEqual(manifest["extensions"]["com.openai"]["interface"]["displayName"],"Prisletaren")
            self.assertEqual(manifest["extensions"]["com.openai"]["interface"]["shortDescription"],"Jämför priser med frakt")
