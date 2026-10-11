# GPT Byggaren canonical builder (upstream snapshot)

Vendored from installed GPT Byggaren `distribution-and-parity` skill resources on 2026-10-11.

- `build_distributions.py` and `validate_distributions.py` are the upstream canonical scripts.
- `lib/project_model.py` and `lib/__init__.py` provide required imports.
- Python dependency: `PyYAML` (see root `requirements-build.txt`).

**Integration status:** Dependency stage only. The scripts require a full GPT Byggaren `gpt-project.yaml`, platform-specific templates and contracts. Prisletaren still uses `tools/build.py` for the two active, tested distributions. The upstream scripts MUST NOT replace it until the full project schema and runtime resources are provided and the generated archives pass parity validation. This is intentionally not release-ready.
