import unittest
from unittest.mock import MagicMock

from base.validator import ValidatorManager
from directory.directory_filter import DirectoryFilter
from entry.entry import Directory, FileSystemEntry
from entry.entry_exception import (
    InvalidEntryNameCharacterException,
    InvalidEntryNameException,
)
from entry.entry_factory import DirectoryFactory
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
from path.validator.path_exception import (
    NotExistingPathException,
)
from tests.entry_validator_test import (
    FakeEntryWithInvalidCharactersMaker,
)
from tests.fake_path_validator import (
    FakeDirectoryPathValidator,
    FakeExistingPathValidator,
)


class TestDirectoryFilter(unittest.TestCase):
    def setUp(self):
        invalid_characters_provider = LinuxInvalidEntryNameCharacterProvider()
        invalid_characters_validator = InvalidEntryNameCharactersValidator(
            invalid_characters_provider
        )
        invalid_names_provider = LinuxInvalidEntryNameProvider()
        invalid_name_validator = InvalidEntryNameValidator(invalid_names_provider)
        directory_path_validator = MagicMock()
        directory_path_validator.validate.side_effect = (
            FakeDirectoryPathValidator.validate
        )
        directory_entry_validator = EntryAdapterForPathValidator(
            directory_path_validator
        )
        existing_path_validator = MagicMock()
        existing_path_validator.validate.side_effect = (
            FakeExistingPathValidator.validate
        )
        existing_entry_validator = EntryAdapterForPathValidator(existing_path_validator)

        validators = [
            invalid_name_validator,
            invalid_characters_validator,
            existing_entry_validator,
            directory_entry_validator,
        ]
        validator_manager = ValidatorManager[FileSystemEntry](validators=validators)
        directory_factory = DirectoryFactory()

        self.directory_filter = DirectoryFilter(
            validator=validator_manager,
            directory_factory=directory_factory,
        )

    def test_filter(self):
        entries = {
            FileSystemEntry(
                name="file1.txt",
                directory_path="directory/for/tests/",
                path="directory/for/tests/file1.txt",
            ),
            FileSystemEntry(
                name="directory1",
                directory_path="directory/for/tests/",
                path="directory/for/tests/directory1",
            ),
        }

        directories = self.directory_filter.filter(entries)

        expected_directories = {
            Directory(
                name="directory1",
                directory_path="directory/for/tests/",
                path="directory/for/tests/directory1",
            )
        }
        self.assertEqual(
            directories,
            expected_directories,
            "Directories are not the same as the expected ones",
        )

    def test_filter_with_not_existing_entry(self):
        entry = FileSystemEntry(
            name="not_existing_entry",
            directory_path="directory/for/tests/",
            path="directory/for/tests/not_existing_entry",
        )
        entries = {entry}

        with self.assertRaises(NotExistingPathException):
            self.directory_filter.filter(entries)

    def test_filter_with_invalid_characters_in_name(self):
        invalid_characters_provider = LinuxInvalidEntryNameCharacterProvider()
        invalid_entry_maker = FakeEntryWithInvalidCharactersMaker(
            invalid_characters_provider
        )
        entries = invalid_entry_maker.get()

        for entry in entries:
            with self.assertRaises(InvalidEntryNameCharacterException):
                self.directory_filter.filter({entry})

    def test_filter_with_empty_entry_name(self):
        entry = FileSystemEntry(
            name="",
            directory_path="directory/for/tests/",
            path="directory/for/tests/",
        )
        entries = {entry}

        with self.assertRaises(InvalidEntryNameException):
            self.directory_filter.filter(entries)

    def test_filter_with_reserved_entry_name(self):
        invalid_names_provider = LinuxInvalidEntryNameProvider()
        invalid_names = invalid_names_provider.get()
        entries = {
            FileSystemEntry(
                name=name,
                directory_path="directory/for/tests/",
                path="directory/for/tests/" + name,
            )
            for name in invalid_names
        }

        for entry in entries:
            with self.assertRaises(InvalidEntryNameException):
                self.directory_filter.filter({entry})

    def test_filter_with_no_directories(self):
        entries = {
            FileSystemEntry(
                name="file1.txt",
                directory_path="directory/for/tests/",
                path="directory/for/tests/file1.txt",
            ),
            FileSystemEntry(
                name="file2",
                directory_path="directory/for/tests/",
                path="directory/for/tests/file2",
            ),
        }

        filtered_entries = self.directory_filter.filter(entries)

        self.assertEqual(len(filtered_entries), 0, "There shouldn't be any directories")

    def test_filter_with_no_entries(self):
        entries = set()

        directories = self.directory_filter.filter(entries)

        self.assertEqual(len(directories), 0, "There shouldn't be any entries")
