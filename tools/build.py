"""Deterministic, contract-checked build for active Prisletaren distributions.

This remains a project-specific builder, not GPT Byggaren's full canonical builder.
"""
from pathlib import Path
import argparse
import json
import re
import subprocess
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[1]
EXCLUDE = {'.git', 'dist', '__pycache__', '.pytest_cache', '.venv', 'build', '.mypy_cache'}
ZIP_DATE = (2020, 1, 1, 0, 0, 0)

def files():
    return sorted((p for p in ROOT.rglob('*') if p.is_file() and not p.is_symlink() and not any(part in EXCLUDE for part in p.relative_to(ROOT).parts) and p.suffix != '.pyc'), key=lambda p: p.relative_to(ROOT).as_posix())

def zip_write(target, mapping):
    with zipfile.ZipFile(target, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for arc, src in sorted(mapping, key=lambda pair: pair[0]):
            name = str(arc).replace('\\', '/')
            info = zipfile.ZipInfo(name, ZIP_DATE)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            z.writestr(info, src.read_bytes())

def plugin_mapping():
    base = ROOT / 'src/plugin'
    return [(p.relative_to(base).as_posix(), p) for p in sorted(base.rglob('*')) if p.is_file() and not p.is_symlink() and p.name != 'mcp.json']

def validate_sources(version):
    canonical = (ROOT/'src/canonical/instructions.md').read_bytes()
    contracts = (ROOT/'src/canonical/contracts.md').read_bytes()
    assert canonical == (ROOT/'src/runtime/chatgpt-chat.md').read_bytes(), 'Chat canonical drift'
    skill = (ROOT/'src/plugin/prisletaren/skills/prisjamforelse/SKILL.md').read_bytes()
    assert canonical in skill, 'Plugin canonical drift'
    assert contracts == (ROOT/'src/plugin/prisletaren/skills/prisjamforelse/references/contracts.md').read_bytes(), 'Contract drift'
    assert not list((ROOT/'src/plugin').rglob('mcp.json')), 'Unexpected MCP configuration'
    manifest = json.loads((ROOT/'src/plugin/prisletaren/plugin.json').read_text())
    assert manifest['version'] == version, 'Release tag and plugin manifest version differ'
    assert manifest['name'] == 'prisletaren'
    assert len(manifest['extensions']['com.openai']['interface']['shortDescription']) <= 30
    status = json.loads((ROOT/'docs/project-status.json').read_text())
    assert status['version'] == version, 'Release tag and project status version differ'

def validate_archives(paths):
    for path in paths:
        with zipfile.ZipFile(path) as z:
            assert z.testzip() is None, f'Bad archive: {path}'
            names = z.namelist()
            assert len(names) == len(set(names)), f'Duplicate ZIP entry: {path}'
            assert all(not n.startswith('/') and '..' not in Path(n).parts for n in names)
            assert not any('/dist/' in '/'+n or '__pycache__' in n for n in names)
    with zipfile.ZipFile(paths[1]) as z:
        assert z.read('INSTRUCTIONS.md') == (ROOT/'src/canonical/instructions.md').read_bytes()
    with zipfile.ZipFile(paths[2]) as z:
        assert 'prisletaren/plugin.json' in z.namelist()
        assert 'prisletaren/skills/prisjamforelse/SKILL.md' in z.namelist()
        assert all(not n.endswith('mcp.json') for n in z.namelist())

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--version', required=True, help='Semver release tag, e.g. v0.5.0')
    ap.add_argument('--skip-tests', action='store_true', help='Only use in CI after tests have already passed')
    args = ap.parse_args()
    version = args.version.removeprefix('v')
    if not re.fullmatch(r'\d+\.\d+\.\d+', version):
        ap.error('Version must be semver, e.g. v0.5.0')
    validate_sources(version)
    if not args.skip_tests:
        result = subprocess.run([sys.executable, '-m', 'unittest', 'discover', '-s', 'tests', '-v'], cwd=ROOT)
        if result.returncode: raise SystemExit(result.returncode)
    out = ROOT / 'dist'; out.mkdir(exist_ok=True)
    project, chat, plugin = [out / f'prisletaren-{name}-{version}.zip' for name in ('project','chat','plugin')]
    zip_write(project, [(p.relative_to(ROOT).as_posix(), p) for p in files()])
    zip_write(chat, [('INSTRUCTIONS.md', ROOT/'src/runtime/chatgpt-chat.md'), ('START-HERE.md', ROOT/'src/runtime/START-HERE.md')])
    zip_write(plugin, plugin_mapping())
    validate_archives((project, chat, plugin))
    for p in (project,chat,plugin): print(p)

if __name__ == '__main__': main()
