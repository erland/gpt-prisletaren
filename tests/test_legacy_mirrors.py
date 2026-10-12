"""Protect historical source mirrors until their consumers have been retired."""
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

class LegacyMirrorTests(unittest.TestCase):
    def test_chat_legacy_mirror_preserves_canonical(self):
        self.assertEqual(
            (ROOT / "src/runtime/chatgpt-chat.md").read_bytes(),
            (ROOT / "src/canonical/instructions.md").read_bytes(),
        )

    def test_plugin_legacy_contract_mirror_preserves_canonical(self):
        self.assertEqual(
            (ROOT / "src/plugin/prisletaren/skills/prisjamforelse/references/contracts.md").read_bytes(),
            (ROOT / "src/canonical/contracts.md").read_bytes(),
        )

    def test_lint_has_only_reviewed_duplicate_warnings(self):
        import sys
        sys.path.insert(0, str(ROOT / "tools/upstream_gpt_byggaren"))
        from lint_gpt_project import lint
        report = lint(ROOT)
        self.assertEqual(report["summary"]["errors"], 0, report["findings"])
        warnings = {(f["code"], f["message"]) for f in report["findings"] if f["severity"] == "warning"}
        expected = {
            ("GP210", "Identical Markdown files detected: src/plugin/prisletaren/skills/prisjamforelse/references/contracts.md, src/canonical/contracts.md"),
            ("GP210", "Identical Markdown files detected: src/runtime/chatgpt-chat.md, src/canonical/instructions.md"),
        }
        self.assertEqual(warnings, expected)

if __name__ == "__main__":
    unittest.main()
