# Produktidentifiering

**Ansvar:** avgöra vilken exakt fysisk produkt och variant användaren avser innan offerter får jämföras.

**Utlösare:** en prisfråga med produktnamn, modell, MPN/EAN eller osäkra variantattribut.

**Arbetsflöde:** normalisera märke, modell, MPN/EAN, färg, storlek, kapacitet och antal; granska avvikelser mellan källor; be om en riktad komplettering när material variantosäkerhet återstår. Returnera entydig ProductIdentity eller en klar fråga, aldrig en gissning.

**Gräns:** gör inte prisrankning och behandla inte en liknande produkt som identisk.

**Kontrakt:** `identify_product(query)` i `src/canonical/contracts.md`. Canonical instruktion i `src/canonical/instructions.md` har företräde.
