import unittest

from subdirectories.provider.entry_names_provider import OsListdirEntryNamesProvider


class TestOsListdirEntryNamesProvider(unittest.TestCase):
    def test_get(self):
        provider = OsListdirEntryNamesProvider()

        actual = provider.get("directory/for/tests")

        expected = {"subdirectory1", "subdirectory2", "raise.txt"}
        self.assertEqual(actual, expected)
