import unittest

from entry.invalid_entry_name_characters_provider import (
    LinuxInvalidEntryNameCharactersProvider,
)


class TestLinuxInvalidEntryNameCharactersProvider(unittest.TestCase):
    def test_get(self):
        provider = LinuxInvalidEntryNameCharactersProvider()

        invalid_characters = provider.get()

        expected_set = {"/"}
        self.assertEqual(
            invalid_characters,
            expected_set,
            "It returns not expected invalid names for the system file entry in Linux",
        )
