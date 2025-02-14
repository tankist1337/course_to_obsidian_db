import unittest
from abc import ABC, abstractmethod

from base.validator import ValidatorManager
from entry.converter.entry_arguments import SetEntryArguments
from entry.converter.entry_converter import SetEntryConverter
from entry.entry import Directory, FileSystemEntry
from entry.entry_provider import EntryProvider
from entry.entry_validator import (
    EntryAdapterForPathValidator,
    InvalidEntryNameCharactersValidator,
    InvalidEntryNameValidator,
)
from entry.invalid_entry_name_character_provider import (
    LinuxInvalidEntryNameCharacterProvider,
)
from entry.invalid_entry_names_provider import (
    IInvalidEntryNameProvider,
    LinuxInvalidEntryNameProvider,
)
from entry.separator_provider import LinuxSeparatorProvider
from path.validator.path_exception import (
    NonDirectoryPathException,
    NotExistingPathException,
)
from directory.directory_filter import DirectoryFilter
from entry.entry_factory import DirectoryFactory
from entry.entry_name_provider import OsListdirEntryNameProvider
from directory.directory_provider import (
    DirectoryProvider,
)
from tests.path_validator_test import (
    FakeNonDirectoryPathValidator,
    FakeNotExistingPathValidator,
)


class TestDirectoryProvider(unittest.TestCase):
    def setUp(self):
        # Directory path validator
        self.not_existing_path_validator = FakeNotExistingPathValidator()
        self.non_directory_path_validator = FakeNonDirectoryPathValidator()
        directory_path_validators = [
            self.not_existing_path_validator,
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
        not_existing_entry_validator = EntryAdapterForPathValidator(
            self.not_existing_path_validator
        )
        invalid_characters_validator = InvalidEntryNameCharactersValidator(
            self.invalid_characters_provider
        )

        self.invalid_names_provider = LinuxInvalidEntryNameProvider()
        invalid_name_validator = InvalidEntryNameValidator(self.invalid_names_provider)

        self.entry_names_provider = FakeOsListdirEntryNamesProvider()
        self.entry_names_provider.set_strategy(FakeNeutralStrategy())

        entry_validators = [
            invalid_name_validator,
            invalid_characters_validator,
            not_existing_entry_validator,
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

        # Directory filter
        directory_filter_validator = EntryAdapterForPathValidator(
            self.non_directory_path_validator
        )

        directory_factory = DirectoryFactory()
        directory_filter = DirectoryFilter(
            validator_manager=directory_filter_validator,
            directory_factory=directory_factory,
        )

        # directory provider
        self.directory_provider = DirectoryProvider(
            entry_provider=self.entry_provider,
            directory_filter=directory_filter,
            directory_path_validator=directory_path_validator_manager,
        )

    def test_get(self):
        entry_names = self.entry_names_provider.get(self.directory_path)
        entries = self.converter.convert(
            SetEntryArguments(entry_names, self.directory_path)
        )
        self.non_directory_path_validator.update_directories(
            {entry.path: "directory" in entry.name for entry in entries}
        )

        directories = self.directory_provider.get(self.directory_path)

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
            "The directories aren't the same as expected",
        )

    def test_get_with_no_directories(self):
        self.entry_names_provider.set_strategy(FakeNoDirectoriesStrategy())
        entry_names = self.entry_names_provider.get(self.directory_path)
        entries = self.converter.convert(
            SetEntryArguments(entry_names, self.directory_path)
        )
        self.non_directory_path_validator.update_directories(
            {entry.path: False for entry in entries}
        )

        directories = self.directory_provider.get(self.directory_path)

        self.assertEqual(
            len(directories),
            0,
            f'The directory "{self.directory_path}" mustn\'t have any directory',
        )

    def test_get_with_directory_path_not_closed_by_separator(self):
        self.directory_path = "directory/for/tests"
        entry_names = self.entry_names_provider.get(self.directory_path)
        entries = self.converter.convert(
            SetEntryArguments(entry_names, self.directory_path)
        )
        self.non_directory_path_validator.set_directories(
            {entry.path: "directory" in entry.name for entry in entries},
            {self.directory_path: True},
        )

        entries = self.directory_provider.get(self.directory_path)

        expected = {
            Directory(
                name="directory1",
                directory_path="directory/for/tests",
                path="directory/for/tests/directory1",
            )
        }
        self.assertEqual(entries, expected, "Directories aren't the same as expected")

    def test_get_with_not_existing_directory_path(self):
        self.not_existing_path_validator.update_existing_paths(
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


class FakeOsListdirEntryNamesStrategy(OsListdirEntryNameProvider, ABC):
    @abstractmethod
    def get(self, directory_path) -> set[str]:
        pass


class FakeNeutralStrategy(FakeOsListdirEntryNamesStrategy):
    def get(self, directory_path) -> set[str]:
        return {"file1", "directory1", "all_good.txt"}


class FakeNoEntryNamesStrategy(FakeOsListdirEntryNamesStrategy):
    def get(self, directory_path) -> set[str]:
        return set()


class FakeNoDirectoriesStrategy(FakeOsListdirEntryNamesStrategy):
    def get(self, directory_path) -> set[str]:
        return {"file1", "file2"}


class FakeInvalidCharactersInName(FakeOsListdirEntryNamesStrategy):
    def __init__(self, entry_with_invalid_characters_maker):
        self.entry_with_invalid_characters_maker = entry_with_invalid_characters_maker

    def get(self, directory_path):
        invalid_entries = self.entry_with_invalid_characters_maker.get()

        return {entry.name for entry in invalid_entries}


class FakeInvalidNamesStrategy(FakeOsListdirEntryNamesStrategy):
    def __init__(self, invalid_names_provider: IInvalidEntryNameProvider):
        self.invalid_names_provider = invalid_names_provider

    def get(self, directory_path):
        return self.invalid_names_provider.get()


class FakeOsListdirEntryNamesProvider(OsListdirEntryNameProvider):
    def __init__(self, strategy: FakeOsListdirEntryNamesStrategy | None = None):
        self.strategy = strategy

    def set_strategy(self, strategy):
        self.strategy = strategy

    def get(self, directory_path) -> set[str]:
        if self.strategy:
            return self.strategy.get(directory_path)
        raise TypeError
