from abc import ABC
import unittest

from base.validator import ValidatorManager
from entry.converter.entry_arguments import (
    ListEntryArguments,
)
from entry.converter.entry_converter import (
    ListEntryConverter,
)
from entry.entry import Directory, FileSystemEntry
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
    IInvalidEntryNamesProvider,
    LinuxInvalidEntryNamesProvider,
)
from entry.separator_provider import LinuxSeparatorProvider
from path.validator.path_exception import NotExistingPathException
from subdirectories.directory_filter import DirectoryFilter
from subdirectories.entry_factory import DirectoryFactory
from subdirectories.provider.entry_names_provider import (
    OsListdirEntryNamesProvider,
)
from subdirectories.subdirectories_exception import NoSubdirectoriesException
from subdirectories.subdirectories_manager import (
    SubdirectoriesProvider,
    SubdirectoriesManager,
)
from subdirectories.validator.subdirectories_validator import NoSubdirectoriesValidator
from tests.entry_validator_test import (
    FakeEntryWithInvalidCharactersMaker,
    FakeNonDirectoryEntryValidator,
    FakeNotExistingEntryValidator,
)


class TestSubdirectoriesManager(unittest.TestCase):
    def setUp(self):
        separator_provider = LinuxSeparatorProvider()
        self.converter = ListEntryConverter(separator_provider)

        self.invalid_characters_provider = LinuxInvalidEntryNameCharactersProvider()
        invalid_characters_validator = InvalidEntryNameCharactersValidator(
            self.invalid_characters_provider
        )

        self.invalid_names_provider = LinuxInvalidEntryNamesProvider()
        invalid_name_validator = InvalidEntryNameValidator(self.invalid_names_provider)

        self.not_existing_path_validator = FakeNotExistingEntryValidator()
        self.non_directory_validator = FakeNonDirectoryEntryValidator()

        directory_factory = DirectoryFactory()

        filter_validators = [
            invalid_name_validator,
            invalid_characters_validator,
            self.not_existing_path_validator,
            self.non_directory_validator,
        ]
        filter_validator_manager = ValidatorManager[FileSystemEntry](
            validators=filter_validators
        )

        directory_filter = DirectoryFilter(
            validator_manager=filter_validator_manager,
            directory_factory=directory_factory,
        )

        provider_validators = [
            invalid_name_validator,
            invalid_characters_validator,
            self.not_existing_path_validator,
        ]
        provider_validator_manager = ValidatorManager[FileSystemEntry](
            validators=provider_validators
        )

        self.entry_names_provider = FakeOsListdirEntryNamesProvider()

        self.provider = SubdirectoriesProvider(
            directory_filter=directory_filter,
            converter=self.converter,
            validator=provider_validator_manager,
            entry_names_provider=self.entry_names_provider,
        )

        provider_manager_validator = NoSubdirectoriesValidator()

        self.manager = SubdirectoriesManager(self.provider, provider_manager_validator)
        self.directory_path = "directory/for/tests/"

    def test_get(self):
        self.entry_names_provider.set_strategy(FakeGoodEntryNamesStrategy())
        entry_names = self.entry_names_provider.get(self.directory_path)
        entries = self.converter.convert(
            ListEntryArguments(entry_names, self.directory_path)
        )
        self.non_directory_validator.directory_entries_dictionary = {
            entry: "directory" in entry.name for entry in entries
        }

        directories = self.manager.get(self.directory_path)

        expected_set = {
            Directory(
                name="directory1",
                directory_path="directory/for/tests/",
                path="directory/for/tests/directory1",
            )
        }
        directory_set = set(directories)
        self.assertEqual(
            directory_set, expected_set, "The directories aren't the same as expected"
        )

    def test_get_with_empty_directory(self):
        self.entry_names_provider.set_strategy(FakeNoDirectoriesStrategy())
        entry_names = self.entry_names_provider.get(self.directory_path)
        entries = self.converter.convert(
            ListEntryArguments(entry_names, self.directory_path)
        )
        self.non_directory_validator.directory_entries_dictionary = {
            entry: False for entry in entries
        }

        with self.assertRaises(NoSubdirectoriesException):
            self.manager.get(self.directory_path)

    def test_get_with_not_existing_directory_path(self):
        self.fail()

    def test_get_with_non_directory_path(self):
        self.fail()


class TestSubdirectoriesProvider(unittest.TestCase):
    def setUp(self):
        separator_provider = LinuxSeparatorProvider()
        self.converter = ListEntryConverter(separator_provider)

        self.invalid_characters_provider = LinuxInvalidEntryNameCharactersProvider()
        invalid_characters_validator = InvalidEntryNameCharactersValidator(
            self.invalid_characters_provider
        )

        self.invalid_names_provider = LinuxInvalidEntryNamesProvider()
        invalid_name_validator = InvalidEntryNameValidator(self.invalid_names_provider)

        self.not_existing_path_validator = FakeNotExistingEntryValidator()
        self.non_directory_validator = FakeNonDirectoryEntryValidator()

        directory_factory = DirectoryFactory()

        validators_for_filter = [
            invalid_name_validator,
            invalid_characters_validator,
            self.not_existing_path_validator,
            self.non_directory_validator,
        ]
        validator_manager_for_filter = ValidatorManager[FileSystemEntry](
            validators=validators_for_filter
        )

        directory_filter = DirectoryFilter(
            validator_manager=validator_manager_for_filter,
            directory_factory=directory_factory,
        )

        validators_for_provider = [
            invalid_name_validator,
            invalid_characters_validator,
            self.not_existing_path_validator,
        ]
        validator_manager_for_provider = ValidatorManager[FileSystemEntry](
            validators=validators_for_provider
        )

        self.entry_names_provider = FakeOsListdirEntryNamesProvider()

        self.provider = SubdirectoriesProvider(
            directory_filter=directory_filter,
            converter=self.converter,
            validator=validator_manager_for_provider,
            entry_names_provider=self.entry_names_provider,
        )

    def test_get(self):
        self.entry_names_provider.set_strategy(FakeGoodEntryNamesStrategy())
        directory_path = "path/to/subdirectories/"
        entry_names = self.entry_names_provider.get(directory_path)
        entries = self.converter.convert(
            ListEntryArguments(entry_names, directory_path)
        )
        self.non_directory_validator.directory_entries_dictionary = {
            entry: "directory" in entry.name for entry in entries
        }

        directories = self.provider.get(directory_path)

        expected_list = [
            Directory(
                name="directory1",
                directory_path="path/to/subdirectories",
                path="path/to/subdirectories/directory1",
            )
        ]
        self.assertEqual(
            directories, expected_list, "The subdirectories isn't the same as expected"
        )

    def test_get_with_no_entry_names(self):
        self.entry_names_provider.set_strategy(FakeNoEntryNamesStrategy())
        directory_path = "path/to/subdirectories/"

        directories = self.provider.get(directory_path)

        self.assertEqual(
            len(directories), 0, f'The directory "{directory_path}" must be empty'
        )

    def test_get_with_no_directories(self):
        self.entry_names_provider.set_strategy(FakeNoDirectoriesStrategy())
        directory_path = "path/to/subdirectories/"
        entry_names = self.entry_names_provider.get(directory_path)
        entries = self.converter.convert(
            ListEntryArguments(entry_names, directory_path)
        )
        self.non_directory_validator.directory_entries_dictionary = {
            entry: False for entry in entries
        }

        directories = self.provider.get(directory_path)

        self.assertEqual(
            len(directories),
            0,
            f'The directory "{directory_path}" mustn\'t have any directory',
        )

    def test_get_with_invalid_characters_in_name(self):
        self.entry_names_provider.set_strategy(
            FakeInvalidCharactersInName(
                FakeEntryWithInvalidCharactersMaker(self.invalid_characters_provider)
            )
        )
        directory_path = "path/to/subdirectories/"

        with self.assertRaises(InvalidEntryNameCharactersException):
            self.provider.get(directory_path)

    def test_get_with_reserved_entry_name(self):
        self.entry_names_provider.set_strategy(
            FakeInvalidNamesStrategy(self.invalid_names_provider)
        )
        directory_path = "path/to/subdirectories/"

        with self.assertRaises(InvalidEntryNameException):
            self.provider.get(directory_path)

    def test_get_with_empty_entry_name(self):
        self.test_get_with_reserved_entry_name()

    def test_get_with_not_existing_entry(self):
        self.entry_names_provider.set_strategy(FakeNotExistingEntryStrategy())
        directory_path = "path/to/subdirectories/"
        entry_names = self.entry_names_provider.get(directory_path)
        entries = self.converter.convert(
            ListEntryArguments(entry_names, directory_path)
        )
        self.not_existing_path_validator.existing_entries_dictionary = {
            entry: False for entry in entries
        }

        with self.assertRaises(NotExistingPathException):
            self.provider.get(directory_path)

    def test_get_with_duplicated_entry_names(self):
        self.entry_names_provider.set_strategy(FakeDuplicatedEntryNamesStrategy())
        directory_path = "path/to/subdirectories/"

        directories = self.provider.get(directory_path)

        expected_list = [
            Directory(
                name="duplicated_directory",
                directory_path="path/to/subdirectories",
                path="path/to/subdirectories/duplicated_directory",
            )
        ]
        self.assertEqual(
            directories, expected_list, "The subdirectories isn't the same as expected"
        )

    def test_get_with_directory_path_not_closed_by_separator(self):
        self.entry_names_provider.set_strategy(FakeGoodDirectoryStrategy())
        directory_path = "path/to/subdirectories"

        directories = self.provider.get(directory_path)

        expected_path = "path/to/subdirectories/directory1"
        self.assertEqual(
            directories[0].path, expected_path, "The path isn't the same as expected"
        )

    def test_get_with_not_existing_directory_path(self):
        self.fail()

    def test_get_with_non_directory_path(self):
        self.fail()


class FakeOsListdirEntryNamesStrategy(OsListdirEntryNamesProvider, ABC):
    def get(self, directory_path):
        pass


class FakeGoodEntryNamesStrategy(FakeOsListdirEntryNamesStrategy):
    def get(self, directory_path):
        return ["file1", "directory1", "all_good.txt"]


class FakeNoEntryNamesStrategy(FakeOsListdirEntryNamesStrategy):
    def get(self, directory_path):
        return []


class FakeNoDirectoriesStrategy(FakeOsListdirEntryNamesStrategy):
    def get(self, directory_path):
        return ["file1", "file2"]


class FakeDuplicatedEntryNamesStrategy(FakeOsListdirEntryNamesStrategy):
    def get(self, directory_path):
        return ["duplicated_directory", "duplicated_directory"]


class FakeInvalidCharactersInName(FakeOsListdirEntryNamesStrategy):
    def __init__(self, entry_with_invalid_characters_maker):
        self.entry_with_invalid_characters_maker = entry_with_invalid_characters_maker

    def get(self, directory_path):
        invalid_entries = self.entry_with_invalid_characters_maker.get()

        return [entry.name for entry in invalid_entries]


class FakeInvalidNamesStrategy(FakeOsListdirEntryNamesStrategy):
    def __init__(self, invalid_names_provider: IInvalidEntryNamesProvider):
        self.invalid_names_provider = invalid_names_provider

    def get(self, directory_path):
        return self.invalid_names_provider.get()


class FakeGoodDirectoryStrategy(FakeOsListdirEntryNamesStrategy):
    def get(self, directory_path):
        return ["directory1"]


class FakeNotExistingEntryStrategy(FakeOsListdirEntryNamesStrategy):
    def get(self, directory_path):
        return ["not existing file"]


class FakeOsListdirEntryNamesProvider(OsListdirEntryNamesProvider):
    def __init__(self, strategy: FakeOsListdirEntryNamesStrategy = None):
        self.strategy = strategy

    def set_strategy(self, strategy):
        self.strategy = strategy

    def get(self, directory_path):
        return self.strategy.get(directory_path)
