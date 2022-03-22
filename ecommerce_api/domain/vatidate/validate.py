from __future__ import annotations


class Validate:
    """Validate class"""

    def is_less_than_zero(self, value: int | float) -> bool:
        """Validate if value is less than zero."""

        return value < 0

    def is_only_letters(self, value: str) -> bool:
        """Validate if value is only letters."""

        return value.isalpha()

    def is_string_in_string(self, value: str, string: str) -> bool:
        """Validate if value is an string inside string."""

        return value in string

    def is_upper_letter_in_string(self, value: str) -> bool:
        """check if at least one letter of the string is uppercase."""

        return any(char.isupper() for char in value)

    def have_upper_letters_numbers_and_special_characters(self, value: str) -> bool:
        """Validate if value have letters, numbers and special characters."""

        return self.is_upper_letter_in_string(value) and not value.isalnum()


