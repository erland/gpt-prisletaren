# Prisletaren – utvecklingsplan

Status: Idéanalys och preliminär arkitektur, 2026-10-11.

## Syfte
Hjälpa privatpersoner i Sverige hitta det lägsta aktuella priset för en exakt identifierad fysisk produkt, med separata priser före och efter frakt, upp till 5–10 verifierade erbjudanden och direktlänkar till produktsidor.

## Funktionella krav
1. Ta emot produktnamn, modellbeteckning, EAN/GTIN eller produktsideslänk.
2. Normalisera produktidentitet: märke, modell, variant, färg, storlek, kapacitet, förpackningsmängd och GTIN när tillgängligt.
3. Fråga efter minsta nödvändiga komplettering om produktidentiteten är tvetydig; visa möjliga kandidater när det underlättar.
4. Sök dagsaktuella erbjudanden från relevanta sökresultat, prisjämförelsesidor och butikers egna produktsidor.
5. Verifiera produktmatchning, tillgänglighet, SEK, svensk moms, leverans till Sverige och fraktinformation.
6. Beräkna totalpris = pris inklusive moms + lägsta allmänt tillgängliga fraktalternativ + övriga obligatoriska avgifter.
7. Visa separat varupris, frakt, obligatoriska avgifter, totalpris, lagerstatus, källa/kontrolltid och direktlänk.
8. Sortera på verifierat totalpris; hantera okänd frakt utanför den säkert rangordnade listan.
9. Returnera högst 10 och helst minst 5 när tillräckligt många verifierade alternativ finns. Fabricera aldrig erbjudanden.
10. Beskriv begränsningar, osäkerhet, eventuella postnummerberoenden och att slutpris alltid kontrolleras i butikskassan.

## Avgränsning v1
- Privatperson i Sverige, nya fysiska produkter, en enhet, standardleverans.
- SEK, pris med moms; utländska erbjudanden endast om leverans till Sverige och relevanta skatter/avgifter kan fastställas eller tydligt redovisas som okända.
- Inga inköp, kassainteraktioner, lagerreservationer, automatiska prisbevakningar eller historik i v1.
- Exkludera medlemspriser, individuella kuponger, begagnat och refurbished från huvudrankningen; visa eventuellt separat.
- Om frakt kräver postnummer: begär postnummer endast vid behov eller ange tydligt osäkerhet.

## Målarkitektur
### Capability-kontrakt
- `identify_product(input) -> ProductIdentity | CandidateList | Clarification`
- `discover_offers(identity, market=SE) -> OfferCandidate[]`
- `verify_offer(candidate, identity) -> VerifiedOffer | Rejection | UncertainOffer`
- `rank_offers(verified_offers) -> RankedOffer[]`
- `present_results(identity, ranking, limitations) -> SwedishComparison`

### Datakontrakt (centrala fält)
- ProductIdentity: brand, model, gtin?, variant_attributes, quantity, condition=new.
- Offer: merchant, merchant_product_url, product_price_sek, shipping_sek?, mandatory_fees_sek?, total_sek?, stock_status, checked_at, source_url, identity_confidence, price_confidence, shipping_status=verified|unknown|conditional.
- Shipping = unknown får aldrig tolkas som 0.
- Verified total = produktpris + verifierad frakt + verifierade obligatoriska avgifter.

### Workspace/state
- `guided` modellrobusthet i första versionen; tillfälligt samtalstillstånd räcker eftersom prisjämförelse är ett engångsflöde.
- Persistenta projektfiler och Git-status används för utvecklingsprocessen, inte för slutkonsumentens prisfråga.

### Verktyg och runtime
- Webbsökning och öppning av aktuella sidor är kärnkrav. Vissa källor kan vara otillgängliga eller sakna kontrollerbara fraktvillkor.
- Prissajter (t.ex. Prisjakt, PriceRunner) används som upptäcktskällor, helst följt av verifiering hos handlare.
- Ingen egen scrapingbackend eller betalt API som grundkrav. Utvärdera behov efter verkliga testfall.
- Bedöm ChatGPT Chat, OpenAI Plugin, Claude Projects/Skills, OpenCode separat och aktivera bara fungerande runtime med nödvändiga webbfunktioner.

## Testfall
1. Entydigt modellnummer: tio butiker med olika frakt.
2. Tvetydigt produktnamn: fråga färg/lagring/årsmodell.
3. Samma märke, olika GTIN: fel variant avvisas.
4. Lockpris med fraktavgift: totalpris styr sortering.
5. Okänd frakt: ingen påhittad totalsumma.
6. Slutsåld eller utgången produkt: inte lägst bland köpbara produkter.
7. Färre än fem verifierade butiker: visa de som hittats.
8. Dubbletter, marknadsplatser, utlandssäljare och medlemspriser särbehandlas.
9. Ingen webbtillgång: gör inte anspråk på aktuellt lägsta pris.
10. Direktlänkar måste nå erbjudandets produktsida, inte en generisk sökning.

## Genomförandeplan och gates
1. **Idé och krav:** besluta namn och mål, fastställa v1 avgränsning. (Preliminär klar)
2. **Arkitektur och kontrakt:** canonical instruktion, modellrobusthet, webbtillgång och datakontrakt. (Förslagen, ej validerade)
3. **Projektstruktur:** README, canonical source, projektstatus, tester och .gitignore. (Ej påbörjat)
4. **Prototyp:** bygg produktidentifiering, prissökning, verifiering och resultatpresentation. (Ej påbörjat)
5. **Verifiering:** testsvit med riktiga sökexempel, deterministisk lint/hygiene, kontroll av resultat och direktlänkar. (Ej påbörjat)
6. **Distributioner:** aktivera endast verifierat kompatibla runtimes, bygg separata paket från canonical source. (Ej påbörjat)
7. **GitHub:** CI för PR/branch, release-byggning med taggstyrd version, inga genererade dist-filer i källrepository. (Ej påbörjat)
8. **Release:** kontrollera parityrapport, teststatus och artefakter och leverera projekt-ZIP samt varje distributions-ZIP separat. (Ej påbörjat)

## Nästa rekommenderade steg
Godkänn eller justera idéanalysen; skapa därefter canonical projektstruktur och den första körbara prototypen. Inga implementationer eller runtime-distributioner är ännu skapade.

## Bakgrundskällor (kontrollerade 2026-10-11)
- https://www.prisjakt.nu/information/sa-har-jamfor-vi-priser-info
- https://www.prisjakt.nu/information/prisjakts-basfunktioner
- https://support.google.com/merchants/answer/7052112?hl=sv
