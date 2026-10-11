# Prisletaren

Prisjämförande svensk GPT för fysiska varor. Först identifieras exakt produktvariant; därefter hämtas aktuella erbjudanden med webbsökning och totalpriser jämförs med explicit verifierad frakt.

## Vad finns i v0.2?
- Canonical assistentinstruktion och plattformsneutrala kontrakt i `src/canonical/`.
- `prisletaren/ranking.py`: deterministiskt stöd för validering, separation av osäkra erbjudanden och sortering. **Ingen automatisk webbinhämtning ingår i denna modul**.
- Tester utan extern åtkomst (`python -m unittest discover -s tests -v`).
- ChatGPT Chat-instruktion som kan användas manuellt med webbverktyg när sådana finns.
- CI och GitHub Release-paketering. `dist/` skapas endast vid byggning och versionshanteras inte.

## Användning
Använd `src/runtime/chatgpt-chat.md` som instruktion i en chatt med fungerande webbsökning. Ange t.ex. `Hitta lägsta totalpris för Bosch [exakt modell] i Sverige`. Assistenten ska begära kompletteringar om modellen är tvetydig.

## Kompatibilitet
Se `docs/runtime-parity.md`. Prisletaren kan **inte** garantera aktuella priser när webbsökning/öppning av produktsidor saknas. Inga låtsade webbsökningar eller priser.

## Versionshantering
Rekommenderad GitHub-repository: `prisletaren`. Pusha källkoden, skapa en tagg som `v0.1.0` för att bygga distributions-ZIP. Projekt-ZIP byggs separat av `tools/build.py`.

## Livetest v0.2
Se `docs/live-smoke-test-2026-10-11.md`. Produktmatchning och indexpriser kan kontrolleras, men 5–10 verifierade butikserbjudanden inklusive frakt har **inte** kunnat bekräftas i dessa stickprov.

## OpenAI Plugin v0.3.0

`dist/prisletaren-plugin-0.3.0.zip` innehåller `prisletaren/plugin.json` och `prisletaren/skills/prisjamforelse/`. Skills-only, inga MCP-servrar eller hemligheter. Webbåtkomst kräver hoststöd. Installera och utför end-to-end-test innan releaseklassning. `python tools/build.py --version 0.3.0` bygger alla paket och kör tester.

## v0.4.0 Frakt
Tre nivåer: verifierad frakt, beräknad frakt från tillämpliga dokumenterade butiksvillkor, och okänd frakt. Beräknade totalpriser sorteras separat från verifierade. Kodmodulen söker inte webben själv.

## v0.5.0 Aggregatortotal och köpbarhet
Indikativa aggregatorpriser visas separat utan att markeras verifierade. Handlarens avpublicering har företräde; beställningsvaror hålls åtskilda. Reproducerbara offline-fixtures finns i `tests/fixtures/`. Kör `python -m unittest discover -s tests -v` och `python tools/build.py --version 0.5.0`. Kod hämtar fortfarande inga livepriser. Ingen hostacceptans har körts.

## GitHub-klar förbättring av v0.5.0 (2026-10-11)

`tools/build.py` skapar deterministiska ZIP-filer och validerar canonical-paritet, filintegritet och versionsöverensstämmelse. De tidigare 46 testerna och fyra nya byggtester passerar (50 totalt). CI kör tester och paketbygge; releaseworkflow hämtar versionsnummer från taggen.

**Publiceringsstatus:** Ej publicerat. GitHub-konnektorn kan nå befintliga repon men saknar funktion för att skapa `erland/prisletaren`; repo gav 404 vid kontroll. När repo har skapats, pusha hela projekt-ZIP-innehållet (inte `dist/`) och kontrollera GitHub Actions innan release-taggen `v0.5.0` skapas.

**Avvikelse mot GPT Byggaren:** Byggsystemet är än så länge projektspecifikt och använder inte GPT Byggarens fullständiga deklarativa canonical distributionsmotor (`build_system.runtime_targets`). Detta måste åtgärdas före full releaseklassning.
