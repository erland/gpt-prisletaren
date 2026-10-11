"""Fail-closed checks for importing the GPT Byggaren canonical distribution engine."""
import unittest
from pathlib import Path
from tools.build import ROOT, validate_sources

UPSTREAM = ROOT / "tools" / "upstream_gpt_byggaren"


class UpstreamBuilderGateTests(unittest.TestCase):
    def test_upstream_sources_present(self):
        for file in ("build_distributions.py", "validate_distributions.py",
                     "lib/project_model.py", "lib/__init__.py"):
            with self.subTest(file=file):
                self.assertTrue((UPSTREAM / file).is_file())

    def test_upstream_has_full_contract_requirement(self):
        code = (UPSTREAM / "build_distributions.py").read_text()
        self.assertIn('gpt-project.yaml', code)
        self.assertIn('RUNTIME_BUILDERS', code)
        self.assertIn('build_runtime_target', code)

    def test_do_not_claim_full_integration_without_schema(self):
        # The current project must keep its proven local builder until a
        # complete upstream YAML schema + templates have been integrated.
        self.assertFalse((ROOT / "gpt-project.yaml").exists())
        self.assertIn("project-specific builder", (ROOT / "tools" / "build.py").read_text())
        validate_sources("0.5.0")

    def test_dependency_documented(self):
        self.assertIn("PyYAML", (ROOT / "requirements-build.txt").read_text())
