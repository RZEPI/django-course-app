"""
Sample tests
"""

from django.test import SimpleTestCase

from app import calc


class CalcTests(SimpleTestCase):
    """Test the calc module/"""

    def test_add(self):
        """Test adding numbers together"""
        result = calc.add(5, 6)

        self.assertEqual(result, 11)

    def test_substract(self):
        """Test substract numbers."""
        res = calc.substract(5, 3)

        self.assertEqual(res, 2)
