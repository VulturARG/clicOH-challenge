import unittest

from domain.vatidate.validate import Validate


class ValidateTestCase(unittest.TestCase):
    def setUp(self):
        self.validate = Validate()

    # validate.is_less_than_zero

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

    # validate.is_string_in_string

    def test_is_string_in_string(self):
        actual = self.validate.is_string_in_string('cd', 'abcdef')
        self.assertTrue(actual)

    def test_is_string_not_in_string(self):
        actual = self.validate.is_string_in_string('yz', 'abcdef')
        self.assertFalse(actual)

    # validate.is_only_letters

    def test_only_letters(self):
        actual = self.validate.is_only_letters('abc')
        self.assertTrue(actual)

    def test_only_letters_empty_string(self):
        actual = self.validate.is_only_letters('')
        self.assertFalse(actual)

    def test_only_letters_with_space(self):
        actual = self.validate.is_only_letters('abc def')
        self.assertFalse(actual)

    def test_only_letters_with_number(self):
        actual = self.validate.is_only_letters('abc123')
        self.assertFalse(actual)

    def test_only_letters_with_special_char(self):
        actual = self.validate.is_only_letters('abc@def')
        self.assertFalse(actual)

    # validate.is_upper_letter_in_string

    def test_is_upper_letter_in_string(self):
        actual = self.validate.is_upper_letter_in_string('abCdef')
        self.assertTrue(actual)

    def test_not_upper_letter_in_string(self):
        actual = self.validate.is_upper_letter_in_string('abcdef')
        self.assertFalse(actual)

    # validate.have_upper_letters_numbers_and_special_characters

    def test_upper_letters_numbers_and_special_characters(self):
        actual = self.validate.have_upper_letters_numbers_and_special_characters('abZc123@def')
        self.assertTrue(actual)

    def test_no_upper_letters_numbers_and_special_characters(self):
        actual = self.validate.have_upper_letters_numbers_and_special_characters('abc123@def')
        self.assertFalse(actual)

    def test_have_letters_numbers_and_special_characters_with_letters_only(self):
        actual = self.validate.have_upper_letters_numbers_and_special_characters('abc')
        self.assertFalse(actual)

    def test_have_letters_numbers_and_special_characters_with_letters_numbers(self):
        actual = self.validate.have_upper_letters_numbers_and_special_characters('abc125')
        self.assertFalse(actual)

    def test_have_letters_numbers_and_special_characters_with_letters_special_chars(self):
        actual = self.validate.have_upper_letters_numbers_and_special_characters('abc_#')
        self.assertFalse(actual)

    def test_have_letters_numbers_and_special_characters_with_space(self):
        actual = self.validate.have_upper_letters_numbers_and_special_characters('abc 123@def')
        self.assertFalse(actual)


