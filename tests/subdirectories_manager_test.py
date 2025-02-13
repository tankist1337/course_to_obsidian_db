import unittest
from abc import ABC, abstractmethod

from base.validator import ValidatorManager
from entry.converter.entry_arguments import SetEntryArguments
from entry.converter.entry_converter import SetEntryConverter
from entry.entry import Directory, FileSystemEntry
from entry.entry_exception import (
    InvalidEntryNameCharactersException,
    InvalidEntryNameException,
)
from entry.entry_validator import (
    EntryAdapterForPathValidator,
    InvalidEntryNameCharactersValidator,
    InvalidEntryNameValidator,
)
from entry.invalid_entry_name_characters_provider import (
    LinuxInvalidEntryNameCharactersProvider,
)
from entry.invalid_entry_names_provider import (
    IInvalidEntryNamesProvider,
    LinuxInvalidEntryNamesProvider,
)
from entry.separator_provider import LinuxSeparatorProvider
from path.validator.path_exception import (
    NonDirectoryPathException,
    NotExistingPathException,
)
from subdirectories.directory_filter import DirectoryFilter
from subdirectories.entry_factory import DirectoryFactory
from subdirectories.provider.entry_names_provider import OsListdirEntryNamesProvider
from subdirectories.subdirectories_manager import (
    SubdirectoriesProvider,
    SubdirectoriesProviderArguments,
)
from tests.entry_validator_test import FakeEntryWithInvalidCharactersMaker
from tests.path_validator_test import (
    FakeNonDirectoryPathValidator,
    FakeNotExistingPathValidator,
)


class TestSubdirectoriesProvider(unittest.TestCase):
    def setUp(self):
        separator_provider = LinuxSeparatorProvider()
        self.converter = SetEntryConverter(separator_provider)

        self.invalid_characters_provider = LinuxInvalidEntryNameCharactersProvider()
        invalid_characters_validator = InvalidEntryNameCharactersValidator(
            self.invalid_characters_provider
        )

        self.invalid_names_provider = LinuxInvalidEntryNamesProvider()
        invalid_name_validator = InvalidEntryNameValidator(self.invalid_names_provider)

        self.not_existing_path_validator = FakeNotExistingPathValidator()
        not_existing_entry_validator = EntryAdapterForPathValidator(
            self.not_existing_path_validator
        )

        self.non_directory_path_validator = FakeNonDirectoryPathValidator()
        non_directory_entry_validator = EntryAdapterForPathValidator(
            self.non_directory_path_validator
        )

        directory_factory = DirectoryFactory()

        filter_validators = [
            invalid_name_validator,
            invalid_characters_validator,
            not_existing_entry_validator,
            non_directory_entry_validator,
        ]
        filter_validator_manager = ValidatorManager[FileSystemEntry](
            validators=filter_validators
        )

        directory_filter = DirectoryFilter(
            validator_manager=filter_validator_manager,
            directory_factory=directory_factory,
        )

        self.entry_names_provider = FakeOsListdirEntryNamesProvider()
        self.entry_names_provider.set_strategy(FakeNeutralStrategy())

        directory_path_validators = [
            self.not_existing_path_validator,
            self.non_directory_path_validator,
        ]
        directory_path_validator_manager = ValidatorManager[str](
            directory_path_validators
        )

        self.provider = SubdirectoriesProvider(
            SubdirectoriesProviderArguments(
                directory_path_validator=directory_path_validator_manager,
                directory_filter=directory_filter,
                converter=self.converter,
                entry_names_provider=self.entry_names_provider,
            )
        )
        self.directory_path = "path/to/subdirectories/"

    def test_get(self):
        entry_names = self.entry_names_provider.get(self.directory_path)
        entries = self.converter.convert(
            SetEntryArguments(entry_names, self.directory_path)
        )
        self.non_directory_path_validator.update_directories(
            {entry.path: "directory" in entry.name for entry in entries},
            {self.directory_path: True},
        )

        directories = self.provider.get(self.directory_path)

        expected_directories = {
            Directory(
                name="directory1",
                directory_path="path/to/subdirectories/",
                path="path/to/subdirectories/directory1",
            )
        }
        self.assertEqual(
            directories,
            expected_directories,
            "The subdirectories aren't the same as expected",
        )

    def test_get_with_no_entry_names(self):
        self.entry_names_provider.set_strategy(FakeNoEntryNamesStrategy())

        directories = self.provider.get(self.directory_path)

        self.assertEqual(
            len(directories),
            0,
            f'The directory "{self.directory_path}" must be empty',
        )

    def test_get_with_no_directories(self):
        self.entry_names_provider.set_strategy(FakeNoDirectoriesStrategy())
        entry_names = self.entry_names_provider.get(self.directory_path)
        entries = self.converter.convert(
            SetEntryArguments(entry_names, self.directory_path)
        )
        self.non_directory_path_validator.update_directories(
            {entry.path: False for entry in entries}, {self.directory_path: True}
        )

        directories = self.provider.get(self.directory_path)

        self.assertEqual(
            len(directories),
            0,
            f'The directory "{self.directory_path}" mustn\'t have any directory',
        )

    def test_get_with_invalid_characters_in_name(self):
        self.entry_names_provider.set_strategy(
            FakeInvalidCharactersInName(
                FakeEntryWithInvalidCharactersMaker(self.invalid_characters_provider)
            )
        )

        with self.assertRaises(InvalidEntryNameCharactersException):
            self.provider.get(self.directory_path)

    def test_get_with_reserved_entry_name(self):
        self.entry_names_provider.set_strategy(
            FakeInvalidNamesStrategy(self.invalid_names_provider)
        )

        with self.assertRaises(InvalidEntryNameException):
            self.provider.get(self.directory_path)

    def test_get_with_empty_entry_name(self):
        self.test_get_with_reserved_entry_name()

    def test_get_with_not_existing_entry(self):
        self.entry_names_provider.set_strategy(FakeNeutralStrategy())
        entry_names = self.entry_names_provider.get(self.directory_path)
        entries = self.converter.convert(
            SetEntryArguments(entry_names, self.directory_path)
        )
        self.not_existing_path_validator.update_existing_paths(
            {entry.path: False for entry in entries}
        )

        with self.assertRaises(NotExistingPathException):
            self.provider.get(self.directory_path)

    def test_get_with_directory_path_not_closed_by_separator(self):
        self.entry_names_provider.set_strategy(FakeGoodDirectoryStrategy())
        self.directory_path = "path/to/subdirectories"

        directories = self.provider.get(self.directory_path)

        expected_path = "path/to/subdirectories/directory1"
        self.assertEqual(
            directories.pop().path, expected_path, "The path isn't the same as expected"
        )

    def test_get_with_not_existing_directory_path(self):
        self.not_existing_path_validator.update_existing_paths(
            {self.directory_path: False}
        )

        with self.assertRaises(NotExistingPathException):
            self.provider.get(self.directory_path)

    def test_get_with_non_directory_path(self):
        self.non_directory_path_validator.update_directories(
            {self.directory_path: False}
        )

        with self.assertRaises(NonDirectoryPathException):
            self.provider.get(self.directory_path)


class FakeOsListdirEntryNamesStrategy(OsListdirEntryNamesProvider, ABC):
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
    def __init__(self, invalid_names_provider: IInvalidEntryNamesProvider):
        self.invalid_names_provider = invalid_names_provider

    def get(self, directory_path):
        return self.invalid_names_provider.get()


class FakeGoodDirectoryStrategy(FakeOsListdirEntryNamesStrategy):
    def get(self, directory_path):
        return {"directory1"}


class FakeOsListdirEntryNamesProvider(OsListdirEntryNamesProvider):
    def __init__(self, strategy: FakeOsListdirEntryNamesStrategy | None = None):
        self.strategy = strategy

    def set_strategy(self, strategy):
        self.strategy = strategy

    def get(self, directory_path) -> set[str]:
        if self.strategy:
            return self.strategy.get(directory_path)
        raise TypeError
