import unittest

from base.validator import ValidatorManager
from entry.entry import File, FileSystemEntry
from entry.entry_exception import (
    InvalidEntryNameCharacterException,
    InvalidEntryNameException,
)
from entry.entry_factory import FileFactory
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
from file.file_filter import FileFilter
from path.validator.path_exception import NotExistingPathException
from tests.entry_validator_test import (
    FakeEntryWithInvalidCharactersMaker,
)
from tests.fake_path_validator import FakeNonFilePathValidator
from tests.path_validator_test import (
    FakeNotExistingPathValidator,
)


class TestFileFilter(unittest.TestCase):
    def setUp(self):
        self.invalid_characters_provider = LinuxInvalidEntryNameCharacterProvider()

        self.not_existing_path_validator = FakeNotExistingPathValidator()
        self.non_file_path_validator = FakeNonFilePathValidator()

        invalid_characters_validator = InvalidEntryNameCharactersValidator(
            self.invalid_characters_provider
        )
        self.invalid_names_provider = LinuxInvalidEntryNameProvider()
        invalid_name_validator = InvalidEntryNameValidator(self.invalid_names_provider)
        not_existing_entry_validator = EntryAdapterForPathValidator(
            self.not_existing_path_validator
        )
        non_file_entry_validator = EntryAdapterForPathValidator(
            self.non_file_path_validator
        )

        filter_validators = [
            invalid_name_validator,
            invalid_characters_validator,
            not_existing_entry_validator,
            non_file_entry_validator,
        ]

        file_filter_validator = ValidatorManager[FileSystemEntry](
            validators=filter_validators
        )

        file_factory = FileFactory()
        self.file_filter = FileFilter(
            validator=file_filter_validator,
            factory=file_factory,
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
        self.non_file_path_validator.update_files(
            {entry.path: "file" in entry.name for entry in entries}
        )

        files = self.file_filter.filter(entries)

        expected_files = {
            File(
                name="file1.txt",
                directory_path="directory1/",
                path="directory1/file1.txt",
            ),
            File(
                name="file2",
                directory_path="directory1/",
                path="directory1/file2",
            ),
        }

        self.assertEqual(
            files,
            expected_files,
            "Files are not the same as the expected ones",
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
            self.file_filter.filter(entries)

    def test_filter_with_invalid_characters_in_name(self):
        invalid_entry_maker = FakeEntryWithInvalidCharactersMaker(
            self.invalid_characters_provider
        )
        entries = invalid_entry_maker.get()

        for entry in entries:
            with self.assertRaises(InvalidEntryNameCharacterException):
                self.file_filter.filter({entry})

    def test_filter_with_empty_entry_name(self):
        entry = FileSystemEntry(
            name="",
            directory_path="directory1/",
            path="directory1/",
        )
        entries = {entry}

        with self.assertRaises(InvalidEntryNameException):
            self.file_filter.filter(entries)

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
                self.file_filter.filter({entry})

    def test_filter_with_no_files(self):
        entries = {
            FileSystemEntry(
                name="directory1",
                directory_path="directory1/",
                path="directory1/directory1",
            ),
            FileSystemEntry(
                name="directory2",
                directory_path="directory1/",
                path="directory1/directory2",
            ),
        }
        self.non_file_path_validator.update_files(
            {entry.path: "file" in entry.name for entry in entries}
        )

        filtered_entries = self.file_filter.filter(entries)

        self.assertEqual(len(filtered_entries), 0, "There shouldn't be any files")

    def test_filter_with_no_entries(self):
        entry_paths = set()

        files = self.file_filter.filter(entry_paths)

        self.assertEqual(len(files), 0, "There shouldn't be any entries")
