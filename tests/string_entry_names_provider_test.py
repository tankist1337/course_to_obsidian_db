import unittest

from subdirectories.provider.string_entry_names_provider import (
    IStringEntryNamesProvider,
)


class TestStringEntryNamesProvider(unittest.TestCase):
    def setUp(self):
        self.provider = FakeStringEntryNamesProvider()
        self.directory_path = "directory/for/tests"

    def test_get_names_with_not_empty_list(self):
        self.provider.is_directory_empty = False

        names = self.provider.get(self.directory_path)

        names_set = set(names)
        expected_set = {"file1", "file2", "directory1"}
        self.assertEqual(
            names_set,
            expected_set,
            "Expected list of string entry names doesn't match to actual",
        )

    def test_get_names_with_empty_list(self):
        self.provider.is_directory_empty = True

        names = self.provider.get(self.directory_path)

        self.assertEqual(len(names), 0, "Expected empty list of string entry names")

    def test_get_names_with_duplicated_names(self):
        self.fail()


class FakeStringEntryNamesProvider(IStringEntryNamesProvider):
    def __init__(self, is_directory_empty: bool = False):
        self.is_directory_empty = is_directory_empty

    def get(self, directory_path: str) -> list[str]:
        return [] if self.is_directory_empty else ["file2", "file1", "directory1"]
