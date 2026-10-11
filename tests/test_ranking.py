import unittest
from prisletaren.ranking import compare_offers, classify_offer

IDENTITY = {'brand': 'Bosch', 'model': 'S100', 'gtin': '123', 'attributes': {'color': 'white'}}
BASE = dict(merchant='Butik A', url='https://example.com/item/a', brand='Bosch', model='S100', gtin='123', attributes={'color': 'white'}, condition='new', currency='SEK', vat_included=True, delivers_to_sweden=True, product_price='1000', shipping_price='99', mandatory_fees='0', stock_status='in_stock', checked_at='2026-10-11T08:00:00+02:00', source_url='https://example.com/item/a', membership_required=False, personal_coupon_required=False, price_source_verified=True, shipping_source_verified=True, fees_source_verified=True, direct_merchant_page=True, source_type='merchant', reference_time='2026-10-11T09:00:00+02:00')

def offer(**changes):
    return BASE | changes

class RankingTests(unittest.TestCase):
    def test_total_includes_shipping_and_fees(self):
        self.assertEqual(str(classify_offer(IDENTITY, offer(mandatory_fees='5'))[2]), '1104')
    def test_unknown_shipping_not_free(self):
        self.assertEqual(classify_offer(IDENTITY, offer(shipping_price=None))[0], 'uncertain')
    def test_cheapest_total_not_cheapest_base(self):
        a = offer(merchant='A', product_price='1000', shipping_price='200')
        b = offer(merchant='B', url='https://example.com/item/b', product_price='1090', shipping_price='0')
        self.assertEqual(compare_offers(IDENTITY, [a,b])['verified'][0]['offer']['merchant'], 'B')
    def test_wrong_gtin_rejected(self):
        self.assertEqual(classify_offer(IDENTITY, offer(gtin='999'))[0], 'rejected')
    def test_wrong_color_rejected(self):
        self.assertEqual(classify_offer(IDENTITY, offer(attributes={'color':'black'}))[0], 'rejected')
    def test_out_of_stock_rejected(self):
        self.assertEqual(classify_offer(IDENTITY, offer(stock_status='out_of_stock'))[0], 'rejected')
    def test_member_price_rejected(self):
        self.assertEqual(classify_offer(IDENTITY, offer(membership_required=True))[0], 'rejected')
    def test_malformed_url_rejected(self):
        self.assertEqual(classify_offer(IDENTITY, offer(url='not-a-url'))[0], 'rejected')
    def test_deduplicated(self):
        self.assertEqual(len(compare_offers(IDENTITY, [offer(),offer()])['verified']), 1)
    def test_no_fabricated_five(self):
        self.assertEqual(len(compare_offers(IDENTITY, [offer()])['verified']), 1)
    def test_negative_money_uncertain(self):
        self.assertEqual(classify_offer(IDENTITY, offer(shipping_price=-1))[0], 'uncertain')
    def test_unsupported_delivery_rejected(self):
        self.assertEqual(classify_offer(IDENTITY, offer(delivers_to_sweden=False))[0], 'rejected')
    def test_no_source_uncertain(self):
        self.assertEqual(classify_offer(IDENTITY, offer(source_url=None))[0], 'uncertain')
    def test_aggregator_not_verified(self):
        self.assertEqual(classify_offer(IDENTITY, offer(source_type='aggregator'))[0], 'uncertain')
    def test_missing_direct_link(self):
        self.assertEqual(classify_offer(IDENTITY, offer(direct_merchant_page=False))[0], 'uncertain')
    def test_unverified_shipping_not_free(self):
        self.assertEqual(classify_offer(IDENTITY, offer(shipping_price='0', shipping_source_verified=False))[0], 'uncertain')
    def test_old_price_uncertain(self):
        self.assertEqual(classify_offer(IDENTITY, offer(checked_at='2026-09-10T08:00:00+02:00'))[0], 'uncertain')
    def test_future_price_uncertain(self):
        self.assertEqual(classify_offer(IDENTITY, offer(checked_at='2026-10-13T08:00:00+02:00'))[0], 'uncertain')
    def test_missing_timezone_uncertain(self):
        self.assertEqual(classify_offer(IDENTITY, offer(checked_at='2026-10-11T08:00:00'))[0], 'uncertain')
    def test_marketplace_separated(self):
        self.assertEqual(classify_offer(IDENTITY, offer(seller_type='marketplace_third_party'))[0], 'uncertain')
    def test_import_fees_uncertain(self):
        self.assertEqual(classify_offer(IDENTITY, offer(import_fees_unknown=True))[0], 'uncertain')
    def test_wrong_mpn_rejected(self):
        identity = IDENTITY | {'mpn':'910-006559'}
        self.assertEqual(classify_offer(identity, offer(mpn='910-006560'))[0], 'rejected')
    def test_missing_mpn_uncertain(self):
        identity = IDENTITY | {'mpn':'910-006559'}
        self.assertEqual(classify_offer(identity, offer())[0], 'uncertain')
    def test_missing_price_verification_uncertain(self):
        self.assertEqual(classify_offer(IDENTITY, offer(price_source_verified=False))[0], 'uncertain')
    def test_unverified_variant_uncertain(self):
        self.assertEqual(classify_offer(IDENTITY, offer(attributes={}))[0], 'uncertain')

if __name__ == '__main__': unittest.main()
