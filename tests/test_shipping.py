import unittest
from test_ranking import IDENTITY, offer
from prisletaren.ranking import classify_offer, compare_offers, resolve_shipping

RULE={'type':'free_over_threshold','threshold':'900','source_type':'merchant','source_url':'https://example.com/shipping','applies_to_product':True,'applies_to_destination':True}
class ShippingTests(unittest.TestCase):
    def test_free_threshold(self):
        self.assertEqual(classify_offer(IDENTITY,offer(shipping_source_verified=False,shipping_price=None,shipping_rule=RULE))[0],'calculated')
    def test_threshold_not_met(self):
        self.assertEqual(resolve_shipping(offer(product_price='899',shipping_source_verified=False,shipping_price=None,shipping_rule=RULE))[0],'unknown')
    def test_flat_rate(self):
        rule=RULE|{'type':'flat_rate','amount':'59'}
        self.assertEqual(str(classify_offer(IDENTITY,offer(shipping_price=None,shipping_source_verified=False,shipping_rule=rule))[2]),'1059')
    def test_missing_source(self):
        self.assertEqual(resolve_shipping(offer(shipping_price=None,shipping_source_verified=False,shipping_rule=RULE|{'source_url':None}))[0],'unknown')
    def test_product_exclusion(self):
        self.assertEqual(resolve_shipping(offer(shipping_price=None,shipping_source_verified=False,shipping_rule=RULE|{'applies_to_product':False}))[0],'unknown')
    def test_destination_exclusion(self):
        self.assertEqual(resolve_shipping(offer(shipping_price=None,shipping_source_verified=False,shipping_rule=RULE|{'applies_to_destination':False}))[0],'unknown')
    def test_checkout_requirement(self):
        self.assertEqual(resolve_shipping(offer(shipping_price=None,shipping_source_verified=False,shipping_rule=RULE|{'requires_checkout':True}))[0],'unknown')
    def test_tiered(self):
        rule=RULE|{'type':'tiered','tiers':[{'min_order':'0','amount':'99'},{'min_order':'900','amount':'29'}]}
        self.assertEqual(str(classify_offer(IDENTITY,offer(shipping_price=None,shipping_source_verified=False,shipping_rule=rule))[2]),'1029')
    def test_separated_from_verified(self):
        o=offer(merchant='C',url='https://example.com/c',shipping_price=None,shipping_source_verified=False,shipping_rule=RULE)
        result=compare_offers(IDENTITY,[offer(),o]);self.assertEqual(len(result['verified']),1);self.assertEqual(len(result['calculated']),1)
    def test_not_invented_zero(self):
        self.assertEqual(resolve_shipping(offer(shipping_price='0',shipping_source_verified=False))[0],'unknown')
    def test_membership_rule_rejected(self):
        self.assertEqual(resolve_shipping(offer(shipping_price=None,shipping_source_verified=False,shipping_rule=RULE|{'requires_membership':True}))[0],'unknown')
    def test_exclusions_unknown(self):
        self.assertEqual(resolve_shipping(offer(shipping_price=None,shipping_source_verified=False,shipping_rule=RULE|{'exclusions_unknown':True}))[0],'unknown')
if __name__=='__main__':unittest.main()
