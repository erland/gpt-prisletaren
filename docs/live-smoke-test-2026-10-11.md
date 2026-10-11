# Live-smoketest – 2026-10-11 (svensk marknad)

Testmetod: webbsökningar, jämförelsesidor och åtkomliga handlarsidor; inga simulerade priser. Resultat är observationer, inte en prislista att återanvända. Indexeringens tid är inte samma som butikens senaste kontrolltid.

## Fall A: Logitech MX Master 3S (grafit), MPN 910-006559, EAN 5099206103726
- Produktidentitet verifierad mot Elgigantens produktsida och Inet.
- Prisjakt listar generiska MX Master 3S för från 895 kr, men även Bluetooth Edition, for Mac, for Business och tillbehör finns som separata sökträffar. Risk för variantblandning.
- Inet produktsida anger **Utgått/Slutsåld**: får inte ligga i köpbar rankning trots produktmatchning.
- CS Megastore anger 1 620 kr inklusive frakt på produktsidan (visat i sökresultat), men denna stickprovsnotering ska inte märkas "verifierad just nu" utan nytt sidbesök, tillgänglighets- och tidskontroll.

## Fall B: Samsung Galaxy Buds3 Pro, vit, SM-R630NZWAEUB, EAN 8806095646732
- SweClockers Priser listar 1 795 kr inkl. frakt hos MaxGaming och 1 875 kr hos CDON (marknadsplats). Aggregerade belopp är **indikativa**, inte självständigt bekräftade på säljarens produktsida eller i kassan.
- Clas Ohlson listar 2 989 kr men kräver varianten vald och hämtar lagersaldo dynamiskt. Kategori/färg och lager måste kontrolleras.
- Silver SM-R630NZAAEUB / EAN 8806095646800 är en annan variant och får ej blandas.

## Slutsats och åtgärder
Tre observerade risker: variantblandning, cachade/indikativa aggregatpriser samt otillgängligt lager eller fraktvillkor. v0.2 har därför striktare MPN-matchning, klassning av aggregatorer och tredjepartssäljare som osäkra, krav på verifieringsflaggor för pris/frakt/avgifter samt tidsstämpel med tidszon och max 24 timmar. **Inga 5–10 aktuella totalpriser har verifierats på butikernas sidor**. Kan därför inte påstå att lägsta pris i Sverige har fastställts.

## Källor
- https://www.prisjakt.nu/produkt.php?p=6496148
- https://www.prisjakt.nu/produkt.php?p=16048945
- https://www.elgiganten.se/product/datorer-kontor/datortillbehor/mus-tangentbord/datormus/logitech-mx-master-3s-tradlos-mus-grafit/463133
- https://www.inet.se/produkt/6602036/logitech-mx-master-3s-graphite
- https://www.csmegastore.se/i/8337611/logitech-mx-master-3s-mus-laser-7-knapper-tr%C3%A5dl%C3%B8s-bluetooth-2-4-ghz-logitech-bolt-mottaker-grafitt
- https://priser.sweclockers.com/produkt/179649/samsung-galaxy-buds3-pro-vit
- https://www.clasohlson.com/se/Samsung-Galaxy-Buds3-Pro-tradlosa-in-ear-horlurar-AI/p/39-4741-1
- https://buyn.se/products/samsung-galaxy-buds3-pro-true-wireless-aktiv-brusreducering-silver
