# Releaseförberedelse: Prisletaren v0.5.0

Status: **förberedd, inte publicerad**. Skapa ingen tagg förrän alla blockerande punkter är klara.

## Bekräftat
- PR #3 är mergad (mergecommit `ed42b3c2b50773fe3e61f880b6bc9f149dde6a23`).
- PR-CI #51 blev grön på commit `86951d0`: enhetstester, gammal byggkontroll, canonical Chat/Plugin-build, upstream-validator och paketkontraktstester.
- Canonical runtimekontraktet aktiverar `chat_zip` och `plugin`. Ingen ny runtime aktiveras implicit.
- Releaseworkflowet använder canonical upstream-byggaren med versionsnummer från taggen.

## Releaseblockerare
1. Releaseworkflowets nya kontrollsteg måste först verifieras i PR-CI eller en ofarlig lokal workflow-simulering. Git-tagg får inte användas som enda provkörning.
2. Plugin-installation och end-to-end-test i ChatGPT saknar ännu dokumenterad acceptans.
3. Aktuella totalpriser, frakt och lagerstatus har inte verifierats konsekvent för 5–10 köpbara svenska butiker. Detta ska anges som begränsning för pilotrelease.
4. Ingen taggstyrd GitHub Release-körning har provats; detta kan endast kontrolleras efter beslut om publicering.

## Leveranser vid framtida v0.5.0
- `prisletaren-project.zip`
- `prisletaren-chat-0.5.0.zip`
- `prisletaren-plugin-0.5.0.zip`
- `SHA256SUMS.txt`
- `DELIVERY-MANIFEST.json`

## Föreslagen releasebeskrivning
Prisletaren v0.5.0 är en pilot för att identifiera en exakt produktmodell och jämföra svenska priser med tydlig separation mellan verifierad frakt, beräknad frakt, indikativa aggregatorpriser och okända belopp. Lagerbrist och beställningsvaror redovisas separat. ChatGPT Chat och OpenAI Plugin byggs från samma canonical instruktioner. Livepriser beror på sökkällornas tillgänglighet och kan inte garanteras. Prisletaren utför inga inköp och har ingen egen automatiserad prisinsamling.

## Förslag på ordning
1. Merga releasehärdningsändringen endast efter grön CI.
2. Genomför installerat hostacceptanstest, notera resultat och eventuella blockerare.
3. Besluta explicit om pilotrelease trots kända begränsningar.
4. Först då: skapa `v0.5.0` och granska faktiska GitHub Release-artefakter.
