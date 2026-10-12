## v0.5.0 – indikativa totalpriser och tillgänglighet
- **Verifierad** betyder att aktuell butikssida styrker produktpris, avgifter, lagerstatus och frakt. **Beräknad** innebär tillämplig dokumenterad fraktregel. **Indikativ** är totalpris från aggregator (ej bekräftat hos säljaren), med namngiven källa och eventuell uppdateringstid. Rangordna dessa grupper separat; kalla aldrig indikativa totalsummor verifierade.
- Aggregatorpris visas endast när exakt variant är identifierad och frakt och totalsumma är konsistenta. Ange tydligt om erbjudandet endast har aggregatorkälla och länka inte aggregatorn som om det vore direkt butikslänk.
- **Handlarens aktuella uppgift om att varan inte säljs, har utgått eller är slutsåld övertrumfar aggregatorns äldre erbjudande.** Exkludera från köpbar huvudlista.
- **Beställningsvara/förbeställning** får en separat grupp med ledtid om den är styrkt. Den får inte utses till vinnare bland lagerförda produkter. Skillnaden mellan beställningsvara och okänt saldo ska visas.
- Visa gärna grupperna verifierad, beräknad, indikativ, beställningsvara och osäker; redovisa källor och kontrolltid, och säg när 5–10 relevanta erbjudanden inte hittades.
- Reproducerbara offlineacceptanstester är fixtures, inte livepriskällor; återanvänd aldrig fixturepriser som om de vore aktuella.

