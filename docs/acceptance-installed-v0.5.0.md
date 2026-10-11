# Acceptansprotokoll – Prisletaren v0.5.0 (2026-10-11)

## Testmiljö
Installerad Prisletaren-skill i ChatGPT, med dess canonical instruktioner och tillgänglig sökning. Detta är **inte** ett test av separat MCP-verktygsanrop eller faktisk utcheckning. Liveprisuppgifterna nedan är observationer vid test, **inte fixtures eller priser att återanvända som aktuella**.

## Fall A: Samsung Galaxy Buds3 Pro vit
- Identitet: MPN `SM-R630NZWAEUB`, EAN `8806095646732`.
- Tio handlarkandidater identifierades, men ingen totalsumma blev faktiskt kassaverifierad.
- Buyn: 1 512 kr + 99 kr frakt = 1 611 kr **beräknad**, men beställningsvara och därför ingen vinnare bland lagerförda produkter.
- MaxGaming: 1 795 kr som indexerat inklusive-frakt-belopp; butikens frakt behöver kontrolleras i kassan. **Indikativ total**.
- Alina: 2 989 kr med angiven fri frakt, leverantörslager snarare än eget lager.
- Proshop: avvikande EAN `8806095646756`; får inte sammanföras okritiskt med målvariant.
- Slutsats: produktidentifiering och separation av lagertillstånd fungerar, men inga fem verifierade köpbara totaler.

## Fall B: Logitech MX Master 3S grafit
- Identitet: MPN `910-006559`, EAN `5099206103726`.
- Alina: 1 149 kr, frakt okänd – inget verifierat totalpris.
- Databyrån genom SweClockers: 1 249 + 99 = 1 348 kr; **indikativ** aggregatorsumma.
- CS Megastore: en produktsida angav 1 620 kr med fri frakt; annan indexerad sida angav 2 066 kr för samma MPN. Olika källålder och motstridiga observationer gör den inte dagsverifierad.
- Inet, Dustin och MaxGaming visade utgången/slutsåld; exkluderade.
- Bluetooth Edition `910-007501`, Mac, Business och annan färg är andra varianter.
- Slutsats: identifiering och avvisning av fel variant fungerar; färskhet och pris-konflikter behöver tydlig spärr.

## Acceptansmatris
| Regel | Fall A | Fall B | Status |
|---|---|---|---|
| MPN, EAN, färg och variant | EAN-konflikt flaggad | Editionsvarianter uteslutna | Godkänt beteende |
| Direktlänk och källnivå | Blandade källor märkta | Blandade källor märkta | Godkänt beteende |
| Lager kontra beställningsvara | Separeras | Utgångna exkluderas | Godkänt beteende |
| Verifierad kontra beräknad/indikativ total | Ingen kassaverifiering | Ingen kassaverifiering | Begränsad |
| Verifierad färskhet | Indexuppgifter inte fullständigt dagsfärska | Motstridiga gamla indexuppgifter | Kräver regressionsskydd |
| 5–10 verifierade köpbara erbjudanden | Inte uppnått | Inte uppnått | Ej godkänt |
| Faktisk plugin-installation | Skill tillgänglig | Skill tillgänglig | Bekräftat |
| Egen MCP / kassautcheckning | Ej körd | Ej körd | Ej verifierat |

## Beslut
Godkänn instruktionsbeteendet som **begränsad pilot**; tilldela inte status 'releaseklar för garanterad prisjämförelse'. Kräv utökade regressionskontroller för källtid, motstridiga priser och indikativa totalsummor före releasebeslut. Framtida livepriser måste hämtas om och verifieras på nytt.
