# GPT Byggarens canonical distributionsmotor – integrerad

## Genomfört
- Upstream `build_distributions.py` och `validate_distributions.py` med `lib/project_model.py` finns i `tools/upstream_gpt_byggaren/`.
- `gpt-project.yaml` deklarerar projekt, canonical instruktion, kunskapsstruktur, skill och runtime-mål för `chat_zip` och `plugin`.
- `src/templates/README.plugin.md` och befintliga Chat-startinstruktioner är kopplade som mallar.
- Båda runtimeformaten byggs i GitHub CI med upstream-byggaren och valideras med upstream-validatorn.
- Separata artefakttester kontrollerar ZIP-struktur, canonical instruktionsinnehåll och frånvaro av `mcp.json`.
- Releaseworkflow använder upstream-byggaren och validatorn vid framtida taggar.

## Bevarande och begränsningar
- `tools/build.py` behålls tills vidare som historisk/fallback-byggare och körs fortfarande i CI, för regressionskontroll. Release bygger med upstream.
- Upstream Chat ZIP har egen runtime-layout (`assistant/instructions.md` och START-HERE.md), och Plugin ZIP har `plugin.json` och Skills. De är inte byte-för-byte identiska med äldre paket men delar canonical kärnbeteende.
- Python-rankningsmodulen söker inte priser själv. Ingen butikskasseverifiering, hostinstallerad pluginacceptans eller full webbsökningsparitet har genomförts.
- Release är **inte publicerad**. Tagga inte förrän release-readiness kontrollerats och plugin-hosttest genomförts.

## Testkommandon
```sh
python -m pip install -r requirements-build.txt
python -m unittest discover -s tests -v
python tools/upstream_gpt_byggaren/build_distributions.py --project-root . --version 0.5.0 --targets chat_zip,plugin
python tools/upstream_gpt_byggaren/validate_distributions.py --project-root .
python -m unittest tests.test_canonical_output -v
```
