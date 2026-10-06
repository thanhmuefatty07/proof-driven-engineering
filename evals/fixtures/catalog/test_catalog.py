import unittest

from catalog import resolve


class CatalogContractTests(unittest.TestCase):
    def setUp(self):
        self.records = [
            {"id": "a", "value": 10},
            {"id": "b", "value": 20},
            {"id": "a", "value": 30},
        ]

    def test_order_duplicates_and_first_matching_record_are_preserved(self):
        result = resolve(self.records, ["b", "a", "a", "missing"])
        self.assertEqual([row["value"] for row in result], [20, 10, 10])
        self.assertIs(result[1], self.records[0])
        self.assertIs(result[2], self.records[0])

    def test_missing_ids_and_empty_inputs_are_omitted(self):
        self.assertEqual(resolve(self.records, ["missing"]), [])
        self.assertEqual(resolve([], ["a"]), [])
        self.assertEqual(resolve(self.records, []), [])

    def test_inputs_remain_unchanged_and_aliasing_is_preserved(self):
        result = resolve(self.records, ["b"])
        self.assertEqual(self.records, [
            {"id": "a", "value": 10},
            {"id": "b", "value": 20},
            {"id": "a", "value": 30},
        ])
        result[0]["value"] = 21
        self.assertEqual(self.records[1]["value"], 21)


if __name__ == "__main__":
    unittest.main()
