import unittest

from entry.entry import Directory, FileSystemEntry
from entry.entry_exception import (
    InvalidEntryNameCharacterException,
    InvalidEntryNameException,
)
from entry.invalid_entry_name_character_provider import (
    LinuxInvalidEntryNameCharacterProvider,
)
from entry.invalid_entry_names_provider import (
    LinuxInvalidEntryNameProvider,
)
from path.validator.path_exception import NotExistingPathException
from tests.entry_validator_test import (
    FakeEntryWithInvalidCharactersMaker,
)
from tests.fake_director_filter import (
    FakeDefaultDirectoryFilter,
    FakeDirectoryFilterWithNotExistingEntry,
)


class TestDirectoryFilter(unittest.TestCase):
    def test_filter(self):
        entries = {
            FileSystemEntry(
                name="file1.txt",
                directory_path="directory1/",
                path="directory1/file1.txt",
            ),
            FileSystemEntry(
                name="file2",
                directory_path="directory1/",
                path="directory1/file2",
            ),
            FileSystemEntry(
                name="directory1",
                directory_path="directory1/",
                path="directory1/directory1",
            ),
        }
        directory_filter = FakeDefaultDirectoryFilter()

        directories = directory_filter.filter(entries)

        expected_directories = {
            Directory(
                name="directory1",
                directory_path="directory1/",
                path="directory1/directory1",
            )
        }

        self.assertEqual(
            directories,
            expected_directories,
            "Directories are not the same as the expected ones",
        )

    def test_filter_with_not_existing_entry(self):
        entry = FileSystemEntry(
            name="not_existing_directory1",
            directory_path="directory1/",
            path="directory1/not_existing_directory1",
        )
        entries = {entry}
        directory_filter = FakeDirectoryFilterWithNotExistingEntry()

        with self.assertRaises(NotExistingPathException):
            directory_filter.filter(entries)

    def test_filter_with_invalid_characters_in_name(self):
        invalid_characters_provider = LinuxInvalidEntryNameCharacterProvider()
        invalid_entry_maker = FakeEntryWithInvalidCharactersMaker(
            invalid_characters_provider
        )
        entries = invalid_entry_maker.get()

        directory_filter = FakeDefaultDirectoryFilter()

        for entry in entries:
            with self.assertRaises(InvalidEntryNameCharacterException):
                directory_filter.filter({entry})

    def test_filter_with_empty_entry_name(self):
        entry = FileSystemEntry(
            name="",
            directory_path="directory1/",
            path="directory1/",
        )
        entries = {entry}
        directory_filter = FakeDefaultDirectoryFilter()

        with self.assertRaises(InvalidEntryNameException):
            directory_filter.filter(entries)

    def test_filter_with_reserved_entry_name(self):
        invalid_names_provider = LinuxInvalidEntryNameProvider()
        invalid_names = invalid_names_provider.get()
        entries = {
            FileSystemEntry(
                name=invalid_name,
                directory_path="directory1/",
                path=f"directory1/{invalid_name}",
            )
            for invalid_name in invalid_names
        }
        directory_filter = FakeDefaultDirectoryFilter()

        for entry in entries:
            with self.assertRaises(InvalidEntryNameException):
                directory_filter.filter({entry})

    def test_filter_with_no_directories(self):
        entries = {
            FileSystemEntry(
                name="file1.txt",
                directory_path="directory1/",
                path="directory1/file1.txt",
            ),
            FileSystemEntry(
                name="file2",
                directory_path="directory1/",
                path="directory1/file2",
            ),
        }
        directory_filter = FakeDefaultDirectoryFilter()

        filtered_entries = directory_filter.filter(entries)

        self.assertEqual(len(filtered_entries), 0, "There shouldn't be any directories")

    def test_filter_with_no_entries(self):
        entries = set()
        directory_filter = FakeDefaultDirectoryFilter()

        directories = directory_filter.filter(entries)

        self.assertEqual(len(directories), 0, "There shouldn't be any entries")
