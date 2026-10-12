# Migrering till GPT Byggaren v1.6.19

Status: **påbörjad, ej färdigställd eller releaseklar** (2026-10-12).

## Inventering (main)

- `gpt-project.yaml` är en deklarativ profil med fem aktiva runtime-mål: Chat ZIP, ChatGPT Plugin, Claude Project, Claude Skills och OpenCode. Projektartefakten byggs också.
- `src/canonical/instructions.md` är beteendekällan. `src/canonical/contracts.md` definierar produktidentitet, erbjudanden, frakt och evidensnivåer.
- `tools/upstream_gpt_byggaren/` innehåller en tidigare incheckad distributionsbyggare, använd i både CI och releaseworkflow.
- `tools/build.py` är en äldre projektspecifik regression-/fallback-byggare.
- `tests/test_all_runtimes.py` verifierar ZIP-layout och att canonical instruktion finns i runtimepaketen, men inte full end-to-end-paritet i installerade värdmiljöer.
- `docs/project-status.json` anger 0.5.0 och uttryckligen kvarstående hosttester och releasekontroller.

## Bevarande krav

1. **Ändra inte prisbeteendet.** Exakt MPN/EAN/variant måste identifieras före rankning.
2. **Behåll fem distributioner**, utan Custom GPT eller MCP-beroende för plugin.
3. Verifierat, beräknat, indikativt, beställningsvara och okänt måste förbli åtskilda.
4. Handlarens tillgänglighet har företräde framför inaktuella aggregatorsaldon.
5. Ingen uppgift om lägsta dagspris utan faktisk tillgång till och kontroll av aktuella källor.
6. En gemensam canonical källa ska kompileras till varje runtime; dela gärna upp ansvar i skills, men duplicera inte domänreglerna i fem handunderhållna varianter.

## Arbetet som återstår innan migrationen får klassas som klar

- [ ] Jämför **hela** den incheckade upstream-byggaren, dess `lib/`-moduler och schemafiler mot originalmotorn i GPT Byggaren **1.6.19**.
- [ ] Uppgradera motorn atomärt från den verifierade originaldistributionen. Blanda inte script från olika motorversioner.
- [ ] Uppdatera projektprofil/skillkompilering enligt 1.6.19, med oförändrade canonical prisregler.
- [ ] Säkerställ att genererade skills delar en kanonisk kärna men använder runtimeanpassade entrypoints där det behövs.
- [ ] Kör projekttester, motorlint, profilvalidering, byggning av projekt + fem distributioner och kontroll av SHA-256/manifest.
- [ ] Verifiera arkivinnehåll, ingen oavsiktlig MCP-konfiguration och komplett canonical-funktion i varje runtime.
- [ ] Kör hostacceptans för plugin samt verifieringsfall med okänd frakt, motstridiga priser, fel variant, slutsålt och beställningsvara.
- [ ] Uppdatera projektstatus och versionsnummer **först efter godkänd verifiering**.

## Migreringsbeslut

Migration av säkra kontrakts- och byggdelar kan göras automatiskt. Ändringar som riskerar att tappa canonical affärsregler eller som inte kan testas i värdmiljön ska lämnas för granskning. Release/tagg ska inte skapas enbart för att källfiler ändrats.

Detta dokument är en verifierbar migrationsbaslinje, **inte ett påstående om att motorn har uppgraderats**.
