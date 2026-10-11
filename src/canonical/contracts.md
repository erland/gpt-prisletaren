# Plattformsneutrala kontrakt

## Capabilities
`identify_product(query) -> identity | alternatives | clarification`
`discover_offers(identity, market="SE") -> offer_candidates`
`verify_offer(candidate, identity) -> verified | uncertain | rejected`
`rank_offers(offers) -> ranked, uncertain, excluded`
`present_results(ranked, uncertain, metadata) -> comparison`

## ProductIdentity
`brand`, `model`, `mpn` (valfritt), `gtin` (valfritt), `attributes` (variantattribut), `quantity` (standard 1), `condition` (new).

## Offer
`merchant`, `url`, `mpn?`, `brand`, `model`, `gtin?`, `attributes`, `condition`, `currency`, `vat_included`, `delivers_to_sweden`, `product_price`, `shipping_price` (null om okänd), `mandatory_fees` (null om okända), `stock_status` (in_stock, preorder, out_of_stock, unknown), `checked_at` (ISO 8601), `source_url`, `membership_required`, `personal_coupon_required`, `seller_type`, `source_type`, `direct_merchant_page`, `price_source_verified`, `shipping_source_verified`, `fees_source_verified`, `import_fees_unknown`, `reference_time` (testbar klocka).

## Invariants
- `total_price` fastställs bara om pris, frakt och obligatoriska avgifter är verifierade.
- Avvikande GTIN eller variant => avvisas; om identitet inte kan bekräftas => osäker.
- Inga priser utan aktuella källor; aldrig förväxla prisjämförelsens länksida med faktisk produktsida.
- Validera allmän tillgång, skick, valuta, moms, leveransland, tillgänglighet och tidsstämpel.
- Ingen påhittad fraktfrihet, butik, källa eller produktidentitet.

## Fraktstatus v0.4.0
`shipping_status`: `verified | calculated | unknown`. `shipping_rule`: `{type: free_over_threshold | flat_rate | tiered, source_type: merchant, source_url: https://..., applies_to_product: true, applies_to_destination: true, requires_checkout: false, exclusions_unknown: false, requires_membership: false, threshold?: SEK, amount?: SEK, tiers?: [{min_order, amount}]}`. En beräknad total sorteras separat och får aldrig anges som verifierad kassatotal. Fraktregel utan källadress eller entydig tillämplighet ger okänd frakt.

## v0.5 – erbjudandeproveniens och köpbarhet
`source_type=aggregator`, `aggregator_total_price` och `source_url` ger endast gruppen `indicative` om beloppen är konsistenta; det ger aldrig verifierad köpbarhet. `merchant_availability`: `in_stock | unavailable | discontinued | out_of_stock | preorder | unknown`. Butikens `unavailable` vinner över aggregatorns `in_stock`. `stock_status`: även `order_item | backorder | preorder`; dessa går till `order_items`, ej huvudrankningen. Rangordning: separata grupper `verified`, `calculated`, `indicative`, `order_items`, `uncertain`, `rejected`; summera inte gruppers ranking till en garanterad svensk prisordning.
