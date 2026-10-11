# Runtimeparitet – fem jämbördiga distributioner

Alla aktiva runtimepaket genereras från `src/canonical/instructions.md` via GPT Byggarens canonical byggare. Samtliga behåller identifiering av exakt produkt, källornas färskhet, osäker frakt, motstridiga priser och förbud mot fabricerade erbjudanden.

| Runtime | Paketering | Webbkrav och begränsning |
|---|---|---|
| ChatGPT Chat | Chat ZIP och runtimekontrakt | Webbsökning behövs för aktuella priser |
| OpenAI Plugin | Skills-first och pluginmanifest | Webbtillgång beror på ChatGPT-värdmiljön; ingen egen MCP |
| Claude Project | Projektinstruktion och kontrakt | Aktuella webbkällor är kontoberoende |
| Claude Skills | En separat prisjämförelseskill med kontrakt | Automatisk skillanvändning och webb beror på värdmiljön |
| OpenCode | AGENTS.md, skill och runtimekontrakt | Extern webbåtkomst kräver faktiskt konfigurerade verktyg |

Runtimekontrakten får aldrig lova fungerande livepriser i en miljö som saknar webbverktyg. En zipfil är ingen hostinstallationsverifiering. Ingen runtime får upphöja gammal sökindexdata eller indikator från aggregator till kassaverifierad totalsumma.

Kontroller i CI: enhetstester, sex runtime-builds, GPT Byggarens validator, canonical innehållsparitet, arkivlayout och befintliga Chat/Plugin-test.
