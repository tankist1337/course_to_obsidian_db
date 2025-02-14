import unittest

from base.validator import ValidatorManager

from entry.entry import Directory, FileSystemEntry
from entry.entry_exception import (
    InvalidEntryNameCharacterException,
    InvalidEntryNameException,
)
from entry.entry_validator import (
    EntryAdapterForPathValidator,
    InvalidEntryNameCharactersValidator,
    InvalidEntryNameValidator,
)
from entry.invalid_entry_name_character_provider import (
    LinuxInvalidEntryNameCharacterProvider,
)
from entry.invalid_entry_names_provider import (
    LinuxInvalidEntryNameProvider,
)
from path.validator.path_exception import NotExistingPathException
from directory.directory_filter import DirectoryFilter
from entry.entry_factory import DirectoryFactory
from tests.entry_validator_test import (
    FakeEntryWithInvalidCharactersMaker,
)
from tests.path_validator_test import (
    FakeNonDirectoryPathValidator,
    FakeNotExistingPathValidator,
)


class TestDirectoryFilter(unittest.TestCase):
    def setUp(self):
        self.invalid_characters_provider = LinuxInvalidEntryNameCharacterProvider()
        invalid_characters_validator = InvalidEntryNameCharactersValidator(
            self.invalid_characters_provider
        )
        self.invalid_names_provider = LinuxInvalidEntryNameProvider()
        invalid_name_validator = InvalidEntryNameValidator(self.invalid_names_provider)
        self.non_directory_path_validator = FakeNonDirectoryPathValidator()
        non_directory_entry_validator = EntryAdapterForPathValidator(
            self.non_directory_path_validator
        )
        self.not_existing_path_validator = FakeNotExistingPathValidator()
        not_existing_entry_validator = EntryAdapterForPathValidator(
            self.not_existing_path_validator
        )
        validators = [
            invalid_name_validator,
            invalid_characters_validator,
            not_existing_entry_validator,
            non_directory_entry_validator,
        ]
        validator_manager = ValidatorManager[FileSystemEntry](validators=validators)
        self.directory_factory = DirectoryFactory()

        self.directory_filter = DirectoryFilter(
            validator_manager=validator_manager,
            directory_factory=self.directory_factory,
        )

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
        self.non_directory_path_validator.update_directories(
            {entry.path: "directory" in entry.name for entry in entries}
        )

        directories = self.directory_filter.filter(entries)

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
        self.not_existing_path_validator.update_existing_paths(
            {
                entry.path: False,
            }
        )

        with self.assertRaises(NotExistingPathException):
            self.directory_filter.filter(entries)

    def test_filter_with_invalid_characters_in_name(self):
        invalid_entry_maker = FakeEntryWithInvalidCharactersMaker(
            self.invalid_characters_provider
        )
        entries = invalid_entry_maker.get()

        for entry in entries:
            with self.assertRaises(InvalidEntryNameCharacterException):
                self.directory_filter.filter({entry})

    def test_filter_with_empty_entry_name(self):
        entry = FileSystemEntry(
            name="",
            directory_path="directory1/",
            path="directory1/",
        )
        entries = {entry}

        with self.assertRaises(InvalidEntryNameException):
            self.directory_filter.filter(entries)

    def test_filter_with_reserved_entry_name(self):
        invalid_names = self.invalid_names_provider.get()

        entries = {
            FileSystemEntry(
                name=invalid_name,
                directory_path="directory1/",
                path=f"directory1/{invalid_name}",
            )
            for invalid_name in invalid_names
        }

        for entry in entries:
            with self.assertRaises(InvalidEntryNameException):
                self.directory_filter.filter({entry})

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
        self.non_directory_path_validator.update_directories(
            {entry.path: "directory" in entry.name for entry in entries}
        )

        filtered_entries = self.directory_filter.filter(entries)

        self.assertEqual(len(filtered_entries), 0, "There shouldn't be any directories")

    def test_filter_with_no_entries(self):
        entry_paths = set()

        directories = self.directory_filter.filter(entry_paths)

        self.assertEqual(len(directories), 0, "There shouldn't be any entries")
