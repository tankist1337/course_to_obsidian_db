import unittest


from base.validator import ValidatorManager
from entry.converter.entry_arguments import SetEntryArguments
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
from entry.separator_provider import LinuxSeparatorProvider
from path.validator.path_exception import (
    NonDirectoryPathException,
    NotExistingPathException,
)
from path.validator.path_validator import NonePathValidator
from tests.entry_validator_test import FakeEntryWithInvalidCharactersMaker
from tests.fake_entry_name_provider import (
    FakeInvalidCharactersInName,
    FakeInvalidNamesStrategy,
    FakeNoEntryNamesStrategy,
    FakeOsListdirEntryNamesProvider,
)
from tests.path_validator_test import (
    FakeNonDirectoryPathValidator,
    FakeExistingPathValidator,
)


class TestEntryProvider(unittest.TestCase):
    def setUp(self):
        # Directory path validator
        none_path_validator = NonePathValidator()
        self.existing_path_validator = FakeExistingPathValidator()
        self.non_directory_path_validator = FakeNonDirectoryPathValidator()
        directory_path_validators = [
            none_path_validator,
            self.existing_path_validator,
            self.non_directory_path_validator,
        ]
        directory_path_validator_manager = ValidatorManager[str](
            directory_path_validators
        )

        # Directory path
        self.directory_path = "directory/for/tests/"

        self.non_directory_path_validator.update_directories(
            {self.directory_path: True},
        )

        # Entry validator
        self.invalid_characters_provider = LinuxInvalidEntryNameCharacterProvider()
        existing_entry_validator = EntryAdapterForPathValidator(
            self.existing_path_validator
        )
        invalid_characters_validator = InvalidEntryNameCharactersValidator(
            self.invalid_characters_provider
        )

        self.invalid_names_provider = LinuxInvalidEntryNameProvider()
        invalid_name_validator = InvalidEntryNameValidator(self.invalid_names_provider)

        self.entry_names_provider = FakeOsListdirEntryNamesProvider()

        entry_validators = [
            invalid_name_validator,
            invalid_characters_validator,
            existing_entry_validator,
        ]
        entry_validator_manager = ValidatorManager[FileSystemEntry](
            validators=entry_validators
        )

        # Converter
        separator_provider = LinuxSeparatorProvider()
        self.converter = SetEntryConverter(separator_provider)

        # Entry provider
        self.entry_provider = EntryProvider(
            directory_path_validator=directory_path_validator_manager,
            entry_names_provider=self.entry_names_provider,
            converter=self.converter,
            entry_validator=entry_validator_manager,
        )

    def test_get(self):
        entries = self.entry_provider.get(self.directory_path)

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
        self.entry_names_provider.set_strategy(FakeNoEntryNamesStrategy())

        entries = self.entry_provider.get(self.directory_path)

        self.assertEqual(len(entries), 0, "There must be no entry")

    def test_get_with_directory_path_not_closed_by_separator(self):
        self.directory_path = "directory/for/tests"
        self.non_directory_path_validator.set_directories({self.directory_path: True})

        entries = self.entry_provider.get(self.directory_path)

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
        self.existing_path_validator.update_existing_paths(
            {self.directory_path: False}
        )

        with self.assertRaises(NotExistingPathException):
            self.entry_provider.get(self.directory_path)

    def test_get_with_non_directory_path(self):
        self.non_directory_path_validator.update_directories(
            {self.directory_path: False}
        )

        with self.assertRaises(NonDirectoryPathException):
            self.entry_provider.get(self.directory_path)

    def test_get_with_invalid_characters_in_name(self):
        self.entry_names_provider.set_strategy(
            FakeInvalidCharactersInName(
                FakeEntryWithInvalidCharactersMaker(self.invalid_characters_provider)
            )
        )

        with self.assertRaises(InvalidEntryNameCharacterException):
            self.entry_provider.get(self.directory_path)

    def test_get_with_reserved_entry_name(self):
        self.entry_names_provider.set_strategy(
            FakeInvalidNamesStrategy(self.invalid_names_provider)
        )

        with self.assertRaises(InvalidEntryNameException):
            self.entry_provider.get(self.directory_path)

    def test_get_with_not_existing_entry(self):
        entry_names = self.entry_names_provider.get(self.directory_path)
        entries = self.converter.convert(
            SetEntryArguments(entry_names, self.directory_path)
        )
        self.existing_path_validator.update_existing_paths(
            {entry.path: False for entry in entries}
        )

        with self.assertRaises(NotExistingPathException):
            self.entry_provider.get(self.directory_path)

    def test_get_with_empty_entry_name(self):
        self.test_get_with_reserved_entry_name()
