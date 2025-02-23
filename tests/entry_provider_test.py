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
    FakeEntryProviderArgumentsBuilder,
    FakeInvalidCharactersInNameProvider,
    FakeNeutralEntriesProvider,
    FakeNoEntryNamesProvider,
    FakeNonDirectoryPathProvider,
    FakeNotExistingEntryProvider,
    FakeNotExistingPathProvider,
    FakeReservedEntryNameProvider,
)


class TestEntryProvider(unittest.TestCase):
    def setUp(self):
        self.directory_path = "directory/for/tests/"
        self.arguments = FakeEntryProviderArgumentsBuilder().build()

    def test_get(self):
        entry_provider = FakeNeutralEntriesProvider(self.arguments)

        entries = entry_provider.get(self.directory_path)

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
        entry_provider = FakeNoEntryNamesProvider(self.arguments)

        entries = entry_provider.get(self.directory_path)

        self.assertEqual(len(entries), 0, "There must be no entry")

    def test_get_with_directory_path_not_closed_by_separator(self):
        self.directory_path = "directory/for/tests"
        entry_provider = FakeNeutralEntriesProvider(self.arguments)

        entries = entry_provider.get(self.directory_path)

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
        entry_provider = FakeNotExistingPathProvider(self.arguments)

        with self.assertRaises(NotExistingPathException):
            entry_provider.get(self.directory_path)

    def test_get_with_non_directory_path(self):
        entry_provider = FakeNonDirectoryPathProvider(self.arguments)

        with self.assertRaises(NonDirectoryPathException):
            entry_provider.get(self.directory_path)

    def test_get_with_invalid_characters_in_name(self):
        entry_provider = FakeInvalidCharactersInNameProvider(self.arguments)

        with self.assertRaises(InvalidEntryNameCharacterException):
            entry_provider.get(self.directory_path)

    def test_get_with_reserved_entry_name(self):
        entry_provider = FakeReservedEntryNameProvider(self.arguments)

        with self.assertRaises(InvalidEntryNameException):
            entry_provider.get(self.directory_path)

    def test_get_with_not_existing_entry(self):
        entry_provider = FakeNotExistingEntryProvider(self.arguments)

        with self.assertRaises(NotExistingPathException):
            entry_provider.get(self.directory_path)

    def test_get_with_empty_entry_name(self):
        self.test_get_with_reserved_entry_name()
