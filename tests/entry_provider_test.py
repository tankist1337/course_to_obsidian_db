import unittest


from entry.entry import FileSystemEntry
from entry.entry_exception import (
    InvalidEntryNameCharacterException,
    InvalidEntryNameException,
)
from path.validator.path_exception import (
    NonDirectoryPathException,
    NotExistingPathException,
)
from tests.fake_entry_provider import (
    FakeDefaultEntryProvider,
    FakeEntryProviderWithInvalidCharactersInName,
    FakeEntryProviderWithNoEntryNames,
    FakeEntryProviderWithFilePath,
    FakeEntryProviderWithNotExistingDirectoryPath,
    FakeEntryProviderWithNotExistingEntry,
    FakeEntryProviderWithReservedName,
)


class TestEntryProvider(unittest.TestCase):
    def test_get(self):
        directory_path = "directory/for/tests/"
        entry_provider = FakeDefaultEntryProvider()

        entries = entry_provider.get(directory_path)

        expected = {
            FileSystemEntry(
                name="file1",
                directory_path="directory/for/tests/",
                path="directory/for/tests/file1",
            ),
            FileSystemEntry(
                name="directory1",
                directory_path="directory/for/tests/",
                path="directory/for/tests/directory1",
            ),
            FileSystemEntry(
                name="all_good.txt",
                directory_path="directory/for/tests/",
                path="directory/for/tests/all_good.txt",
            ),
        }
        self.assertEqual(entries, expected, "Entries aren't the same as expected")

    def test_get_with_no_entry_names(self):
        directory_path = "directory/for/tests/"
        entry_provider = FakeEntryProviderWithNoEntryNames()

        entries = entry_provider.get(directory_path)

        self.assertEqual(len(entries), 0, "There must be no entry")

    def test_get_with_directory_path_not_closed_by_separator(self):
        directory_path = "directory/for/tests"
        entry_provider = FakeDefaultEntryProvider()

        entries = entry_provider.get(directory_path)

        expected = {
            FileSystemEntry(
                name="file1",
                directory_path="directory/for/tests",
                path="directory/for/tests/file1",
            ),
            FileSystemEntry(
                name="directory1",
                directory_path="directory/for/tests",
                path="directory/for/tests/directory1",
            ),
            FileSystemEntry(
                name="all_good.txt",
                directory_path="directory/for/tests",
                path="directory/for/tests/all_good.txt",
            ),
        }
        self.assertEqual(entries, expected, "Entries aren't the same as expected")

    def test_get_with_not_existing_directory_path(self):
        directory_path = "directory/for/tests/"
        entry_provider = FakeEntryProviderWithNotExistingDirectoryPath()

        with self.assertRaises(NotExistingPathException):
            entry_provider.get(directory_path)

    def test_get_with_file_path(self):
        directory_path = "directory/for/file.txt"
        entry_provider = FakeEntryProviderWithFilePath()

        with self.assertRaises(NonDirectoryPathException):
            entry_provider.get(directory_path)

    def test_get_with_invalid_characters_in_name(self):
        directory_path = "directory/for/tests/"
        entry_provider = FakeEntryProviderWithInvalidCharactersInName()

        with self.assertRaises(InvalidEntryNameCharacterException):
            entry_provider.get(directory_path)

    def test_get_with_reserved_entry_name(self):
        directory_path = "directory/for/tests/"
        entry_provider = FakeEntryProviderWithReservedName()

        with self.assertRaises(InvalidEntryNameException):
            entry_provider.get(directory_path)

    def test_get_with_not_existing_entry(self):
        directory_path = "directory/for/tests/"
        entry_provider = FakeEntryProviderWithNotExistingEntry()

        with self.assertRaises(NotExistingPathException):
            entry_provider.get(directory_path)

    def test_get_with_empty_entry_name(self):
        self.test_get_with_reserved_entry_name()
