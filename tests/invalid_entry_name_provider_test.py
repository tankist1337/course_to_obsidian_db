import unittest

from entry.invalid_entry_names_provider import (
    LinuxInvalidEntryNameProvider,
)


class TestLinuxInvalidEntryNameProvider(unittest.TestCase):
    def test_get(self):
        provider = LinuxInvalidEntryNameProvider()

        invalid_names = provider.get()

        expected_set = {"..", "", "."}
        self.assertEqual(
            invalid_names,
            expected_set,
            "It doesn't return expected invalid names for the system file entry in Linux",
        )
