"""Rankning av redan insamlade erbjudanden. Hämtar INGA priser från webben."""
from decimal import Decimal, InvalidOperation
from urllib.parse import urlparse
from datetime import datetime, timedelta, timezone


def money(value):
    if value is None or isinstance(value, bool):
        return None
    try:
        d = Decimal(str(value))
    except (InvalidOperation, ValueError):
        return None
    return d if d.is_finite() and d >= 0 else None




def resolve_shipping(offer):
    """Returnera (status, belopp, skäl). Inga fraktpriser antas från sökindex.

    Fraktregler måste vara dokumenterade på en tillämplig handlarkälla.
    """
    explicit = money(offer.get('shipping_price'))
    if offer.get('shipping_source_verified') is True and explicit is not None:
        return 'verified', explicit, 'frakt direkt verifierad'
    rule = offer.get('shipping_rule')
    if not isinstance(rule, dict) or rule.get('source_type') != 'merchant' or not rule.get('source_url'):
        return 'unknown', None, 'saknar verifierbara fraktvillkor'
    if rule.get('applies_to_product') is not True or rule.get('applies_to_destination') is not True:
        return 'unknown', None, 'fraktregelns tillämplighet oklar'
    if rule.get('requires_checkout') or rule.get('exclusions_unknown') or rule.get('requires_membership'):
        return 'unknown', None, 'fraktregel kräver ytterligare villkor'
    price = money(offer.get('product_price'))
    if price is None:
        return 'unknown', None, 'okänt produktpris'
    kind = rule.get('type')
    if kind == 'free_over_threshold':
        threshold = money(rule.get('threshold'))
        if threshold is not None and price >= threshold:
            return 'calculated', Decimal('0'), 'fri frakt enligt tillämplig beloppsgräns'
    elif kind == 'flat_rate':
        amount = money(rule.get('amount'))
        if amount is not None:
            return 'calculated', amount, 'fast frakt enligt tillämpliga villkor'
    elif kind == 'tiered':
        tiers = rule.get('tiers')
        if isinstance(tiers, list):
            matches = [(money(t.get('min_order')), money(t.get('amount'))) for t in tiers if isinstance(t, dict)]
            valid = [(minimum, amount) for minimum, amount in matches if minimum is not None and amount is not None and price >= minimum]
            if valid:
                return 'calculated', max(valid, key=lambda x: x[0])[1], 'frakt enligt beloppsintervall'
    return 'unknown', None, 'fraktregeln gav inget tillämpligt belopp'

def aggregator_total(offer):
    """Indikativt aggregatortotalpris; aldrig en kassaverifiering."""
    if offer.get('source_type') != 'aggregator' or not offer.get('source_url'):
        return None
    product = money(offer.get('product_price'))
    ship = money(offer.get('shipping_price'))
    fees = money(offer.get('mandatory_fees'))
    published = money(offer.get('aggregator_total_price'))
    if product is None or published is None or (ship is None and fees is None):
        return None
    # Bevara aggregatorns totalpris enbart om redovisade delbelopp stämmer.
    if ship is not None and fees is not None and product + ship + fees != published:
        return None
    if published < product:
        return None
    return published


def fulfilment_status(offer):
    """Aktuell butikstillgänglighet väger tyngre än aggregatorns index."""
    if offer.get('merchant_availability') in ('unavailable', 'discontinued', 'out_of_stock'):
        return 'unavailable'
    if offer.get('stock_status') == 'out_of_stock':
        return 'unavailable'
    if offer.get('merchant_availability') == 'preorder' or offer.get('stock_status') in ('preorder', 'backorder', 'order_item'):
        return 'order_item'
    if offer.get('merchant_availability') == 'in_stock' or offer.get('stock_status') == 'in_stock':
        return 'in_stock'
    return 'unknown'


def classify_offer(identity, offer):
    """Returnerar (category, reason, total) med category verified/uncertain/rejected."""
    for key in ("brand", "model"):
        if not offer.get(key) or str(identity.get(key, '')).casefold().strip() != str(offer[key]).casefold().strip():
            return 'rejected', f'fel {key}', None
    if identity.get('mpn') and offer.get('mpn') and str(identity['mpn']).casefold().strip() != str(offer['mpn']).casefold().strip():
        return 'rejected', 'fel tillverkarartikelnummer', None
    if identity.get('gtin') and offer.get('gtin') and str(identity['gtin']) != str(offer['gtin']):
        return 'rejected', 'fel GTIN', None
    for key, value in identity.get('attributes', {}).items():
        if key in offer.get('attributes', {}) and str(offer['attributes'][key]).casefold() != str(value).casefold():
            return 'rejected', f'fel variant: {key}', None
    if offer.get('condition') != 'new' or fulfilment_status(offer) == 'unavailable':
        return 'rejected', 'skick eller lagerstatus', None
    if offer.get('membership_required') or offer.get('personal_coupon_required'):
        return 'rejected', 'villkorsbundet pris', None
    if offer.get('currency') != 'SEK' or offer.get('vat_included') is not True or offer.get('delivers_to_sweden') is not True:
        return 'rejected', 'pris/leveransvillkor', None
    url = offer.get('url', '')
    parsed = urlparse(url)
    if parsed.scheme != 'https' or not parsed.hostname or parsed.username or parsed.password:
        return 'rejected', 'ogiltig direktlänk', None
    # Förbeställning/beställningsvara visas separat och får inte vinna lagerförda erbjudanden.
    if fulfilment_status(offer) == 'order_item':
        ship_kind, ship_cost, _ = resolve_shipping(offer)
        base = money(offer.get('product_price'))
        fees = money(offer.get('mandatory_fees'))
        total = base + ship_cost + fees if base is not None and ship_cost is not None and fees is not None else None
        return 'order_items', 'beställningsvara eller förbeställning; ej lagerförd', total
    if offer.get('conflicting_price_evidence') is True:
        return 'uncertain', 'motstridiga prisuppgifter måste avstämmas hos handlaren', None
    if offer.get('source_type') == 'merchant' and offer.get('observed_at'):
        try:
            observed = datetime.fromisoformat(offer['observed_at'].replace('Z', '+00:00'))
            reference = offer.get('reference_time')
            now = datetime.fromisoformat(reference.replace('Z', '+00:00')) if reference else datetime.now(timezone.utc)
            if observed.tzinfo is None or now - observed > timedelta(hours=24) or observed > now + timedelta(minutes=5):
                return 'uncertain', 'inaktuell eller ogiltig prisobservation', None
        except (ValueError, TypeError, AttributeError):
            return 'uncertain', 'ogiltig prisobservationstid', None
    if offer.get('seller_type') == 'marketplace_third_party':
        return 'uncertain', 'tredjepartssäljare kräver separat bedömning', None
    if offer.get('import_fees_unknown'):
        return 'uncertain', 'importavgifter okända', None
    if offer.get('source_type') == 'aggregator':
        total = aggregator_total(offer)
        if total is not None:
            return 'indicative', 'indikativ aggregatortotal, inte verifierad hos handlare', total
        return 'uncertain', 'aggregatoruppgift utan konsistent totalpris', None
    if offer.get('direct_merchant_page') is False:
        return 'uncertain', 'ej kontrollerad butikssida', None
    if offer.get('stock_status') != 'in_stock':
        return 'uncertain', 'lagerstatus inte bekräftad', None
    if not offer.get('checked_at') or not offer.get('source_url'):
        return 'uncertain', 'saknar kontrolltid/källa', None
    try:
        checked = datetime.fromisoformat(offer['checked_at'].replace('Z', '+00:00'))
        if checked.tzinfo is None:
            raise ValueError('missing timezone')
        reference = offer.get('reference_time')
        now = datetime.fromisoformat(reference.replace('Z', '+00:00')) if reference else datetime.now(timezone.utc)
        if checked > now + timedelta(minutes=5) or now - checked > timedelta(hours=24):
            return 'uncertain', 'gammal eller framtida kontrolltid', None
    except (ValueError, TypeError, AttributeError):
        return 'uncertain', 'ogiltig kontrolltid', None
    if not offer.get('price_source_verified', False):
        return 'uncertain', 'pris ej verifierat på butikssidan', None
    if not offer.get('fees_source_verified', False):
        return 'uncertain', 'obligatoriska avgifter ej verifierade', None
    if identity.get('mpn') and not offer.get('mpn'):
        return 'uncertain', 'artikelnummer ej verifierat', None
    if identity.get('gtin') and not offer.get('gtin'):
        return 'uncertain', 'GTIN ej verifierat', None
    if any(key not in offer.get('attributes', {}) for key in identity.get('attributes', {})):
        return 'uncertain', 'variant ej verifierad', None
    shipping_status, shipping, shipping_reason = resolve_shipping(offer)
    values = [money(offer.get(x)) for x in ('product_price', 'mandatory_fees')]
    if any(v is None for v in values):
        return 'uncertain', 'okänt pris eller obligatorisk avgift', None
    if shipping is None:
        return 'uncertain', 'okänd frakt: ' + shipping_reason, None
    total = sum(values, shipping)
    if shipping_status == 'calculated':
        return 'calculated', shipping_reason, total
    return 'verified', 'kontrollerat totalpris', total


def compare_offers(identity, offers):
    """Sortera verifierade totalpriser; separera osäkra och avvisade; deduplicera butik + URL."""
    groups = {'verified': [], 'calculated': [], 'indicative': [], 'order_items': [], 'uncertain': [], 'rejected': []}
    seen = set()
    for offer in offers:
        key = (str(offer.get('merchant', '')).casefold(), offer.get('url'))
        if key in seen:
            continue
        seen.add(key)
        category, reason, total = classify_offer(identity, offer)
        groups[category].append({'offer': offer, 'reason': reason, 'total': total})
    groups['verified'].sort(key=lambda x: (x['total'], money(x['offer'].get('product_price'))))
    groups['calculated'].sort(key=lambda x: (x['total'], money(x['offer'].get('product_price'))))
    for k in ('indicative', 'order_items'):
        groups[k].sort(key=lambda x: (x['total'] is None, x['total'] if x['total'] is not None else Decimal('Infinity')))
    return groups
