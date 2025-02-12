import unittest

from entry.invalid_entry_names_provider import (
    LinuxInvalidEntryNamesProvider,
)


class TestLinuxInvalidEntryNamesProvider(unittest.TestCase):
    def test_get(self):
        provider = LinuxInvalidEntryNamesProvider()

        invalid_names = provider.get()

        expected_set = {"..", "", "."}
        self.assertEqual(
            invalid_names,
            expected_set,
            "It doesn't return expected invalid names for the system file entry in Linux",
        )
