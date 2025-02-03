import unittest

from base.validator import ValidatorManager

from entry.entry import FileSystemEntry
from entry.entry_exception import (
    InvalidEntryNameCharactersException,
    InvalidEntryNameException,
)
from entry.entry_validator import (
    InvalidEntryNameCharactersValidator,
    InvalidEntryNameValidator,
)
from entry.invalid_entry_name_characters_provider import (
    LinuxInvalidEntryNameCharactersProvider,
)
from entry.invalid_entry_names_provider import (
    LinuxInvalidEntryNamesProvider,
)
from path.validator.path_exception import NotExistingPathException
from subdirectories.directory_filter import DirectoryFilter
from subdirectories.entry_factory import DirectoryFactory
from tests.entry_validator_test import (
    FakeEntryWithInvalidCharactersMaker,
    FakeNonDirectoryEntryValidator,
    FakeNotExistingEntryValidator,
)


class TestDirectoryFilter(unittest.TestCase):
    def setUp(self):
        self.invalid_characters_provider = LinuxInvalidEntryNameCharactersProvider()
        invalid_characters_validator = InvalidEntryNameCharactersValidator(
            self.invalid_characters_provider
        )
        self.invalid_names_provider = LinuxInvalidEntryNamesProvider()
        invalid_name_validator = InvalidEntryNameValidator(self.invalid_names_provider)
        self.non_directory_validator = FakeNonDirectoryEntryValidator()
        self.not_existing_path_validator = FakeNotExistingEntryValidator()
        validators = [
            invalid_name_validator,
            invalid_characters_validator,
            self.not_existing_path_validator,
            self.non_directory_validator,
        ]
        validator_manager = ValidatorManager[FileSystemEntry](validators=validators)
        self.directory_factory = DirectoryFactory()

        self.directory_filter = DirectoryFilter(
            validator_manager=validator_manager,
            directory_factory=self.directory_factory,
        )

    def test_filter(self):
        entries = [
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
        ]
        self.non_directory_validator.directory_entries_dictionary = {
            entry: "directory" in entry.name for entry in entries
        }

        directories = self.directory_filter.filter(entries)

        directory_set = set(directories)
        expected_set = {self.directory_factory.from_entry(entries[2])}

        self.assertEqual(
            directory_set,
            expected_set,
            "Directories are not the same as the expected ones",
        )

    def test_filter_with_not_existing_entry(self):
        entries = [
            FileSystemEntry(
                name="not_existing_directory1",
                directory_path="directory1/",
                path="directory1/not_existing_directory1",
            ),
        ]
        self.not_existing_path_validator.existing_entries_dictionary = {
            entries[0]: False,
        }

        with self.assertRaises(NotExistingPathException):
            self.directory_filter.filter(entries)

    def test_filter_with_invalid_characters_in_name(self):
        invalid_entries_maker = FakeEntryWithInvalidCharactersMaker(
            self.invalid_characters_provider
        )
        entries = invalid_entries_maker.get()

        for entry in entries:
            with self.assertRaises(InvalidEntryNameCharactersException):
                self.directory_filter.filter([entry])

    def test_filter_with_empty_entry_name(self):
        entries = [
            FileSystemEntry(
                name="",
                directory_path="directory1/",
                path="directory1/",
            )
        ]

        with self.assertRaises(InvalidEntryNameException):
            self.directory_filter.filter(entries)

    def test_filter_with_reserved_entry_name(self):
        invalid_names = self.invalid_names_provider.get()

        entries = [
            FileSystemEntry(
                name=invalid_name,
                directory_path="directory1/",
                path=f"directory1/{invalid_name}",
            )
            for invalid_name in invalid_names
        ]

        for entry in entries:
            with self.assertRaises(InvalidEntryNameException):
                self.directory_filter.filter([entry])

    def test_filter_with_no_directories(self):
        entries = [
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
        ]
        self.non_directory_validator.directory_entries_dictionary = {
            entry: "directory" in entry.name for entry in entries
        }

        filtered_entries = self.directory_filter.filter(entries)

        self.assertEqual(len(filtered_entries), 0, "There shouldn't be any directories")

    def test_filter_with_no_entries(self):
        entries_paths = []

        directories = self.directory_filter.filter(entries_paths)

        self.assertEqual(len(directories), 0, "There shouldn't be any entries")

    def test_filter_with_duplicated_directories(self):
        entries = [
            FileSystemEntry(
                name="directory1",
                directory_path="directory/",
                path="directory/directory1",
            ),
            FileSystemEntry(
                name="directory1",
                directory_path="directory/",
                path="directory/directory1",
            ),
        ]

        directories = self.directory_filter.filter(entries)

        expected_list = [self.directory_factory.from_entry(entries[0])]
        self.assertEqual(
            directories,
            expected_list,
            "Directories are not the same as the expected ones",
        )
