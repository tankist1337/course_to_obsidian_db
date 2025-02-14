import unittest

from entry.invalid_entry_name_character_provider import (
    LinuxInvalidEntryNameCharacterProvider,
)


class TestLinuxInvalidEntryNameCharacterProvider(unittest.TestCase):
    def test_get(self):
        provider = LinuxInvalidEntryNameCharacterProvider()

        invalid_characters = provider.get()

        expected_set = {"/"}
        self.assertEqual(
            invalid_characters,
            expected_set,
            "It doesn't return expected invalid names for the system file entry in Linux",
        )
