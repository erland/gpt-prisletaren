import json
import unittest
from pathlib import Path
from decimal import Decimal
from prisletaren.ranking import classify_offer, compare_offers

FIXTURE = json.loads((Path(__file__).parent/'fixtures/acceptance-v05.json').read_text())

class AcceptanceV05(unittest.TestCase):
    def test_fixture_cases(self):
        for case in FIXTURE['cases']:
            with self.subTest(case=case['name']):
                offer={**FIXTURE['base'], **case['changes']}
                kind, _, total=classify_offer(FIXTURE['identity'], offer)
                self.assertEqual(kind,case['category'])
                self.assertEqual(total, Decimal(case['total']) if case['total'] is not None else None)
    def test_preliminary_not_verified_winner(self):
        rows=[]
        for i, spec in enumerate(FIXTURE['cases'][:2]):
            rows.append({**FIXTURE['base'],**spec['changes'],'merchant':f'Merchant {i}','url':f'https://example.com/{i}'})
        groups=compare_offers(FIXTURE['identity'], rows)
        self.assertEqual(len(groups['verified']),1)
        self.assertEqual(len(groups['indicative']),1)
        self.assertLess(groups['indicative'][0]['total'],groups['verified'][0]['total'])
    def test_fixture_is_explicitly_synthetic(self):
        self.assertIn('Syntetiska',FIXTURE['note'])
