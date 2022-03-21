import unittest

from domain.vatidate.validate import Validate


class ValidateTestCase(unittest.TestCase):
    def setUp(self):
        self.validate = Validate()

    def test_equal_to_zero(self):
        actual = self.validate.is_less_than_zero(0)
        self.assertFalse(actual)

    def test_int_greater_than_zero(self):
        actual = self.validate.is_less_than_zero(5)
        self.assertFalse(actual)

    def test_float_greater_than_zero(self):
        actual = self.validate.is_less_than_zero(5.01)
        self.assertFalse(actual)

    def test_int_less_than_zero(self):
        actual = self.validate.is_less_than_zero(-5)
        self.assertTrue(actual)

    def test_float_less_than_zero(self):
        actual = self.validate.is_less_than_zero(-0.21)
        self.assertTrue(actual)
