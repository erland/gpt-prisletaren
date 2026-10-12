# Erbjudandeverifiering

**Ansvar:** hitta och verifiera aktuella butikserbjudanden för redan identifierad variant.

**Utlösare:** ProductIdentity är klar och kandidaten behöver bekräftas hos handlare.

**Arbetsflöde:** upptäck kandidater via aggregator och bred sökning; öppna handlarens produktsida; kontrollera variant, skick, moms, valuta, leverans till Sverige, saldo, frakt och obligatoriska avgifter. Dokumentera källadress, observerad tid och fraktstatus (verified/calculated/unknown). Separera aggregatoruppgifter från handlarkällor och kassaverifiering. Handlarens slutsålt/utgått övertrumfar aggregator.

**Gräns:** ingen egen ranking eller slutsats om billigast. Okänd frakt kan inte anges som verifierat totalpris.

**Kontrakt:** `discover_offers` och `verify_offer` i `src/canonical/contracts.md`. Följ alltid canonical instruktion.
