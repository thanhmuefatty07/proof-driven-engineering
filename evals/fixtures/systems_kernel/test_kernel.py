import copy
import unittest

from kernel import aggregate_notional


class SystemsKernelContractTests(unittest.TestCase):
    def setUp(self):
        self.events = [
            {"symbol": "AAPL", "price": 15000, "qty": 10, "side": "B", "audit_note": "n1"},
            {"symbol": "AAPL", "price": 15050, "qty": 4, "side": "S", "audit_note": "n2"},
            {"symbol": "MSFT", "price": 32000, "qty": 5, "side": "B", "audit_note": "n3"},
            {"symbol": "GOOG", "price": 14000, "qty": 0, "side": "B", "audit_note": "zero"},
            {"symbol": "GOOG", "price": 14000, "qty": -3, "side": "S", "audit_note": "neg"},
            {"symbol": "AAPL", "price": 15100, "qty": 2, "side": "X", "audit_note": "bad-side"},
        ]

    def test_aggregates_signed_notional_and_volume_for_active_symbols(self):
        result = aggregate_notional(self.events, ["AAPL", "GOOG", "AAPL"])
        self.assertEqual(result, {"AAPL": (15000 * 10 - 15050 * 4, 14)})

    def test_handles_empty_inputs_and_no_active_matches(self):
        self.assertEqual(aggregate_notional([], ["AAPL"]), {})
        self.assertEqual(aggregate_notional(self.events, []), {})
        self.assertEqual(aggregate_notional(self.events, ["NVDA"]), {})

    def test_preserves_exact_large_integer_arithmetic_and_caller_inputs(self):
        large_events = [
            {"symbol": "BIG", "price": 10**18 + 7, "qty": 3, "side": "B", "audit_note": "a"},
            {"symbol": "BIG", "price": 10**18 + 2, "qty": 3, "side": "S", "audit_note": "b"},
        ]
        before = copy.deepcopy(large_events)
        active = ["BIG"]
        result = aggregate_notional(large_events, active)
        self.assertEqual(result, {"BIG": (15, 6)})
        self.assertEqual(large_events, before)
        self.assertEqual(active, ["BIG"])


if __name__ == "__main__":
    unittest.main()
