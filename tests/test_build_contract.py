import tempfile
import unittest
from pathlib import Path
from zipfile import ZipFile
from tools.build import ROOT, plugin_mapping, validate_sources, validate_archives, zip_write

class BuildContractTests(unittest.TestCase):
    def test_versions_and_canonical_inputs(self):
        validate_sources('0.5.0')
    def test_wrong_release_version_is_rejected(self):
        with self.assertRaises(AssertionError):
            validate_sources('0.5.1')
    def test_archive_determinism_and_structure(self):
        with tempfile.TemporaryDirectory() as d:
            one=Path(d)/'one.zip'; two=Path(d)/'two.zip'
            zip_write(one,plugin_mapping()); zip_write(two,plugin_mapping())
            self.assertEqual(one.read_bytes(),two.read_bytes())
            with ZipFile(one) as z:
                self.assertTrue(z.testzip() is None)
                self.assertTrue(all(not name.endswith('mcp.json') for name in z.namelist()))
    def test_no_dist_in_project(self):
        from tools.build import files
        self.assertFalse(any('/dist/' in '/'+p.relative_to(ROOT).as_posix() for p in files()))
