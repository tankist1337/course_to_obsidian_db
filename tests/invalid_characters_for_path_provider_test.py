import unittest

from path.validator.invalid_characters_for_path_provider import (
    LinuxInvalidCharactersForPathProvider,
)


class TestLinuxInvalidCharactersForPathProvider(unittest.TestCase):
    def test_get_invalid_characters(self):
        characters_provider = LinuxInvalidCharactersForPathProvider()

        characters_expected = ["//"]

        characters = characters_provider.get_characters()

        self.assertEqual(
            len(characters_expected),
            len(characters),
            "The number of invalid characters is not as expected",
        )

        for symbol in characters_expected:
            self.assertIn(
                symbol, characters, "The invalid character is not in the list"
            )
