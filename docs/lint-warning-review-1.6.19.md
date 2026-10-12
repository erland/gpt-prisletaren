# Granskning av kvarvarande lintvarningar (GPT Byggaren v1.6.19)

## Beslut

De två `GP210`-varningarna gäller historiska *exakta spegelfiler*, inte två konkurrerande canonical källor. De behålls i denna migration för att inte ändra kompatibilitetsvägarna i det befintliga projektet.

| Spegel | Canonical källa | Beslut |
| --- | --- | --- |
| `src/runtime/chatgpt-chat.md` | `src/canonical/instructions.md` | Behåll för historisk Chat-användning |
| `src/plugin/prisletaren/skills/prisjamforelse/references/contracts.md` | `src/canonical/contracts.md` | Behåll för äldre Plugin-paketering |

Canonical auktoritet ligger kvar i `src/canonical/`. Nya distributioner genereras genom `gpt-project.yaml` och den modulära projektionen. Spegelfilerna är inte nya redigeringsytor.

## Skydd

`tests/test_legacy_mirrors.py` kräver byteidentiska speglar och accepterar **endast** de två uttryckligen granskade `GP210`-varningarna. Nya lintfel och nya/ändrade varningar orsakar testfel i CI. `PYTHONDONTWRITEBYTECODE=1` används i hela CI-jobbet för att linter inte ska rapportera temporära Python-cacher som källfiler.

## Avveckling, separat beslut

Ta inte bort speglarna innan äldre konsumenter och installationsanvisningar uppdaterats och distributions- och hosttester är gröna. Om de tas bort ska tillhörande regressionstester ersättas med tester för de nya källvägarna.

## Releasegräns

Godkänd källkod-CI betyder inte att en installerad Plugin eller Chat ZIP har verifierats med aktuella butikserbjudanden och verkliga fraktvillkor. Ingen release-tagg eller merge görs enbart utifrån denna granskning.
