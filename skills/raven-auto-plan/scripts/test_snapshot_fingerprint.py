import json
import unittest
from snapshot_fingerprint import fingerprint


class FingerprintTests(unittest.TestCase):
    def setUp(self):
        self.value = {'requirements': 'Żądanie: dostęp tylko właściciela', 'plan': 'Sprawdź uprawnienia',
                      'phases': [{'id': 'T1', 'contract': 'Auth'}, {'id': 'T2', 'contract': 'Zapis'}]}

    def test_format_and_key_order_do_not_change_contract(self):
        reordered = dict(reversed(list(self.value.items())))
        self.assertEqual(fingerprint(json.dumps(self.value)), fingerprint(json.dumps(reordered, indent=2, ensure_ascii=False)))

    def test_requirements_phase_order_and_contract_changes_invalidate(self):
        original = fingerprint(json.dumps(self.value))
        for variant in [dict(self.value, requirements='Publiczny dostęp'),
                        dict(self.value, phases=list(reversed(self.value['phases']))),
                        dict(self.value, plan='Pomiń uprawnienia')]:
            self.assertNotEqual(original, fingerprint(json.dumps(variant)))

    def test_ambiguous_or_stateful_payload_is_rejected(self):
        for raw in ['{"requirements":"a","requirements":"b","plan":"x","phases":[]}',
                    json.dumps(dict(self.value, progress='done')),
                    '{"requirements":"a","plan":"x","phases":[{"number":NaN}]}',
                    '{"requirements":"a","plan":"x","phases":{}}']:
            with self.assertRaises(ValueError):
                fingerprint(raw)


if __name__ == '__main__':
    unittest.main()
