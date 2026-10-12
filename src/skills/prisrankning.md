# Prisrankning och redovisning

**Ansvar:** rangordna verifierade kandidater och redovisa osäkerhet transparent på svenska.

**Utlösare:** verifierade och/eller osäkra Offer-objekt föreligger.

**Arbetsflöde:** använd varupris + faktisk/tillämpligt härledd frakt + obligatoriska avgifter; separera verified, calculated, indicative, order_items, uncertain och rejected. Visa källor, kontrolltid, lagerstatus och direkta produktlänkar där sådana är observerade. Utse endast lägsta **bland verifierade erbjudanden**, aldrig en osäker total som vinnare.

**Gräns:** skapa inte källor, butikslänkar, pris eller webbobservationer. Använd inte offline-fixtures som aktuella erbjudanden.

**Kontrakt:** `rank_offers` och `present_results` i `src/canonical/contracts.md`. Följ alltid canonical instruktion.
