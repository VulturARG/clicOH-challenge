from __future__ import annotations


class Validate:
    """Validate class"""

    def is_less_than_zero(self, value: int | float) -> bool:
        """Validate if value is less than zero."""

        return value < 0

    def is_only_letters(self, value: str) -> bool:
        """Validate if value is only letters."""

        return value.isalpha()

    def have_letters_numbers_and_special_characters(self, value: str) -> bool:
        """Validate if value have letters, numbers and special characters."""

        return value.isalnum()

    def have_string_in_string(self, value: str, string: str) -> bool:
        """Validate if value have string in string."""

        return string in value
