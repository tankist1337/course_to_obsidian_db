import unittest
from unittest.mock import MagicMock


from base.validator import ValidatorManager
from entry.converter.entry_converter import SetEntryConverter
from entry.entry import FileSystemEntry
from entry.entry_exception import (
    InvalidEntryNameCharacterException,
    InvalidEntryNameException,
)
from entry.entry_provider import EntryProvider
from entry.entry_validator import (
    EntryAdapterForPathValidator,
    InvalidEntryNameCharactersValidator,
    InvalidEntryNameValidator,
)
from entry.invalid_entry_name_character_provider import (
    LinuxInvalidEntryNameCharacterProvider,
)
from entry.invalid_entry_names_provider import LinuxInvalidEntryNameProvider
from entry.path_normalizer import DirectoryPathNormalizer
from entry.separator_provider import LinuxSeparatorProvider
from path.validator.path_exception import (
    NonDirectoryPathException,
    NotExistingPathException,
)
from tests.entry_validator_test import FakeEntryWithInvalidCharactersMaker
from tests.fake_path_validator import (
    FakeDirectoryPathValidator,
    FakeExistingPathValidator,
)


class TestEntryProvider(unittest.TestCase):
    def setUp(self):
        invalid_characters_provider = LinuxInvalidEntryNameCharacterProvider()
        invalid_characters_validator = InvalidEntryNameCharactersValidator(
            invalid_characters_provider
        )
        invalid_names_provider = LinuxInvalidEntryNameProvider()
        invalid_name_validator = InvalidEntryNameValidator(invalid_names_provider)
        existing_path_validator = MagicMock()
        existing_path_validator.validate.side_effect = (
            FakeExistingPathValidator.validate
        )
        existing_entry_validator = EntryAdapterForPathValidator(existing_path_validator)
        validators = [
            invalid_name_validator,
            invalid_characters_validator,
            existing_entry_validator,
        ]
        entry_validator = ValidatorManager[FileSystemEntry](validators=validators)

        path_normalizer = DirectoryPathNormalizer(LinuxSeparatorProvider())
        converter = SetEntryConverter(path_normalizer)

        self.entry_names_provider = MagicMock()
        self.entry_names_provider.get.return_value = {
            "file1.txt",
            "file2",
            "directory1",
        }

        directory_path_validator = MagicMock()
        directory_path_validator.validate.side_effect = (
            FakeDirectoryPathValidator.validate
        )
        path_validator_manager = ValidatorManager[str](
            [existing_path_validator, directory_path_validator]
        )
        self.entry_provider = EntryProvider(
            entry_names_provider=self.entry_names_provider,
            converter=converter,
            entry_validator=entry_validator,
            directory_path_validator=path_validator_manager,
        )

    def test_get(self):
        directory_path = "directory/for/tests/"

        entries = self.entry_provider.get(directory_path)

        expected = {
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
        self.assertEqual(entries, expected, "Entries aren't the same as expected")

    def test_get_with_no_entry_names(self):
        directory_path = "directory/for/tests/"
        self.entry_names_provider.get.return_value = set()

        entries = self.entry_provider.get(directory_path)

        self.assertEqual(len(entries), 0, "There must be no entry")

    def test_get_with_directory_path_not_closed_by_separator(self):
        directory_path = "directory/for/tests"

        entries = self.entry_provider.get(directory_path)

        expected = {
            FileSystemEntry(
                name="file1.txt",
                directory_path="directory/for/tests",
                path="directory/for/tests/file1.txt",
            ),
            FileSystemEntry(
                name="file2",
                directory_path="directory/for/tests",
                path="directory/for/tests/file2",
            ),
            FileSystemEntry(
                name="directory1",
                directory_path="directory/for/tests",
                path="directory/for/tests/directory1",
            ),
        }
        self.assertEqual(entries, expected, "Entries aren't the same as expected")

    def test_get_with_not_existing_directory_path(self):
        directory_path = "not_existing_path"

        with self.assertRaises(NotExistingPathException):
            self.entry_provider.get(directory_path)

    def test_get_with_non_directory_path(self):
        directory_path = "directory/for/tests/file2"

        with self.assertRaises(NonDirectoryPathException):
            self.entry_provider.get(directory_path)

    def test_get_with_invalid_characters_in_name(self):
        directory_path = "directory/for/tests/"
        invalid_characters_provider = LinuxInvalidEntryNameCharacterProvider()
        invalid_entries = FakeEntryWithInvalidCharactersMaker(
            invalid_characters_provider
        ).get(directory_path)
        self.entry_names_provider.get.return_value = {
            entry.name for entry in invalid_entries
        }

        with self.assertRaises(InvalidEntryNameCharacterException):
            self.entry_provider.get(directory_path)

    def test_get_with_reserved_entry_name(self):
        directory_path = "directory/for/tests/"
        invalid_names_provider = LinuxInvalidEntryNameProvider()
        self.entry_names_provider.get.return_value = invalid_names_provider.get()

        with self.assertRaises(InvalidEntryNameException):
            self.entry_provider.get(directory_path)

    def test_get_with_not_existing_entry(self):
        directory_path = "directory/for/tests/"
        self.entry_names_provider.get.return_value = {"not_existing_entry"}

        with self.assertRaises(NotExistingPathException):
            self.entry_provider.get(directory_path)

    def test_get_with_empty_entry_name(self):
        self.test_get_with_reserved_entry_name()
