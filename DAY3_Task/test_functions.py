"""Offline checks for the two ordinary Python helper functions."""
import unittest
from app import price_lookup, availability_check


class BakeryFunctionTests(unittest.TestCase):
    def test_price_lookup_known_item(self):
        self.assertEqual(price_lookup("cupcake", 6), 480)
        self.assertEqual(price_lookup("plum cake"), 500)

    def test_price_lookup_unknown_item(self):
        self.assertIsNone(price_lookup("brownie"))

    def test_price_lookup_invalid_quantity(self):
        with self.assertRaises(ValueError):
            price_lookup("cupcake", 0)

    def test_availability_notice(self):
        self.assertIn("requirement is met", availability_check("tomorrow", 24))
        self.assertIn("24 hours", availability_check("today evening", 5))


if __name__ == "__main__":
    unittest.main()
