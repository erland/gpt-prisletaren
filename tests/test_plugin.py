import json
import unittest
from pathlib import Path
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]
class PluginContractTests(unittest.TestCase):
    def test_manifest_is_skills_only(self):
        m=json.loads((ROOT/'src/plugin/prisletaren/plugin.json').read_text())
        self.assertEqual(m['name'],'prisletaren')
        self.assertNotIn('mcpServers',m)
        self.assertNotIn('skills',m)
        self.assertLessEqual(len(m['extensions']['com.openai']['interface']['shortDescription']),30)
    def test_skill_retains_full_canonical_rules(self):
        original=(ROOT/'src/canonical/instructions.md').read_text()
        skill=(ROOT/'src/plugin/prisletaren/skills/prisjamforelse/SKILL.md').read_text()
        self.assertIn(original,skill)
    def test_chat_retains_full_canonical_rules(self):
        self.assertEqual((ROOT/'src/runtime/chatgpt-chat.md').read_bytes(),(ROOT/'src/canonical/instructions.md').read_bytes())
    def test_no_mcp_json_in_plugin_tree(self):
        self.assertFalse(list((ROOT/'src/plugin').rglob('mcp.json')))
    def test_reference_parity(self):
        self.assertEqual((ROOT/'src/canonical/contracts.md').read_bytes(),(ROOT/'src/plugin/prisletaren/skills/prisjamforelse/references/contracts.md').read_bytes())
    def test_generated_plugin_archive(self):
        from tempfile import TemporaryDirectory
        # Test packaging utility without depending on an already released file.
        from tools.build import plugin_mapping, zip_write
        with TemporaryDirectory() as d:
            z=Path(d)/'p.zip'
            zip_write(z,plugin_mapping())
            with ZipFile(z) as f:
                names=f.namelist()
                self.assertIn('prisletaren/plugin.json',names)
                self.assertIn('prisletaren/skills/prisjamforelse/SKILL.md',names)
                self.assertFalse(any(n.endswith('mcp.json') for n in names))
                self.assertEqual(len(names),len(set(names)))
