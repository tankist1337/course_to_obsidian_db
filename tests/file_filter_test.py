import unittest
from unittest.mock import MagicMock

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
from tests.fake_path_validator import (
    FakeExistingPathValidator,
    FakeFilePathValidator,
)


class TestFileFilter(unittest.TestCase):
    def setUp(self):
        invalid_characters_provider = LinuxInvalidEntryNameCharacterProvider()
        invalid_characters_validator = InvalidEntryNameCharactersValidator(
            invalid_characters_provider
        )
        invalid_names_provider = LinuxInvalidEntryNameProvider()
        invalid_name_validator = InvalidEntryNameValidator(invalid_names_provider)
        file_path_validator = MagicMock()
        file_path_validator.validate.side_effect = FakeFilePathValidator.validate
        file_entry_validator = EntryAdapterForPathValidator(file_path_validator)
        existing_path_validator = MagicMock()
        existing_path_validator.validate.side_effect = (
            FakeExistingPathValidator.validate
        )
        existing_entry_validator = EntryAdapterForPathValidator(existing_path_validator)

        validators = [
            invalid_name_validator,
            invalid_characters_validator,
            existing_entry_validator,
            file_entry_validator,
        ]
        file_filter_validator = ValidatorManager[FileSystemEntry](validators=validators)

        file_factory = FileFactory()
        self.file_filter = FileFilter(
            validator=file_filter_validator,
            factory=file_factory,
        )

    def test_filter(self):
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
            FileSystemEntry(
                name="directory1",
                directory_path="directory/for/tests/",
                path="directory/for/tests/directory1",
            ),
        }

        files = self.file_filter.filter(entries)

        expected_files = {
            File(
                name="file1.txt",
                directory_path="directory/for/tests/",
                path="directory/for/tests/file1.txt",
            ),
            File(
                name="file2",
                directory_path="directory/for/tests/",
                path="directory/for/tests/file2",
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
            directory_path="directory/for/tests/",
            path="directory/for/tests/not_existing_directory1",
        )
        entries = {entry}

        with self.assertRaises(NotExistingPathException):
            self.file_filter.filter(entries)

    def test_filter_with_invalid_characters_in_name(self):
        invalid_characters_provider = LinuxInvalidEntryNameCharacterProvider()
        invalid_entry_maker = FakeEntryWithInvalidCharactersMaker(
            invalid_characters_provider
        )
        entries = invalid_entry_maker.get()

        for entry in entries:
            with self.assertRaises(InvalidEntryNameCharacterException):
                self.file_filter.filter({entry})

    def test_filter_with_empty_entry_name(self):
        entry = FileSystemEntry(
            name="",
            directory_path="directory/for/tests/",
            path="directory/for/tests/",
        )
        entries = {entry}

        with self.assertRaises(InvalidEntryNameException):
            self.file_filter.filter(entries)

    def test_filter_with_reserved_entry_name(self):
        invalid_names_provider = LinuxInvalidEntryNameProvider()
        invalid_names = invalid_names_provider.get()
        entries = {
            FileSystemEntry(
                name=name,
                directory_path="directory/for/tests/",
                path=f"directory/for/tests/{name}",
            )
            for name in invalid_names
        }

        for entry in entries:
            with self.assertRaises(InvalidEntryNameException):
                self.file_filter.filter({entry})

    def test_filter_with_no_files(self):
        entries = {
            FileSystemEntry(
                name="directory1",
                directory_path="directory/for/tests/",
                path="directory/for/tests/directory1",
            ),
        }

        filtered_entries = self.file_filter.filter(entries)

        self.assertEqual(len(filtered_entries), 0, "There shouldn't be any files")

    def test_filter_with_no_entries(self):
        entry_paths = set()

        files = self.file_filter.filter(entry_paths)

        self.assertEqual(len(files), 0, "There shouldn't be any entries")
