import unittest

from base.validator import ValidatorManager
from entry.converter.entry_arguments import SetEntryArguments
from entry.converter.entry_converter import SetEntryConverter
from entry.entry import FileSystemEntry
from entry.entry_validator import (
    EntryAdapterForPathValidator,
    InvalidEntryNameCharactersValidator,
    InvalidEntryNameValidator,
)
from entry.invalid_entry_name_characters_provider import (
    LinuxInvalidEntryNameCharactersProvider,
)
from entry.invalid_entry_names_provider import LinuxInvalidEntryNamesProvider
from entry.separator_provider import LinuxSeparatorProvider
from part.part import Part
from path.provider.path_provider import PathManager
from path.validator.path_validator import NonePathValidator
from subdirectories.directory_filter import DirectoryFilter
from subdirectories.entry_factory import DirectoryFactory
from subdirectories.subdirectories_manager import (
    SubdirectoriesManager,
    SubdirectoriesProvider,
    SubdirectoriesProviderArguments,
)
from subdirectories.validator.subdirectories_validator import NoSubdirectoriesValidator
from tests.path_provider_test import FakeCliPathProvider, FakeGoodPathStrategy
from tests.path_validator_test import (
    FakeNonDirectoryPathValidator,
    FakeNotExistingPathValidator,
)
from tests.subdirectories_manager_test import (
    FakeNeutralStrategy,
    FakeNoDirectoriesStrategy,
    FakeOsListdirEntryNamesProvider,
)


class TestPartsProvider(unittest.TestCase):
    def setUp(self):
        separator_provider = LinuxSeparatorProvider()
        self.converter = SetEntryConverter(separator_provider)

        invalid_characters_provider = LinuxInvalidEntryNameCharactersProvider()
        invalid_characters_validator = InvalidEntryNameCharactersValidator(
            invalid_characters_provider
        )

        invalid_names_provider = LinuxInvalidEntryNamesProvider()
        invalid_name_validator = InvalidEntryNameValidator(invalid_names_provider)

        not_existing_path_validator = FakeNotExistingPathValidator()
        not_existing_entry_validator = EntryAdapterForPathValidator(
            not_existing_path_validator
        )

        self.non_directory_path_validator = FakeNonDirectoryPathValidator()
        non_directory_entry_validator = EntryAdapterForPathValidator(
            self.non_directory_path_validator
        )

        none_path_validator = NonePathValidator()

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

        subdirectories_provider = SubdirectoriesProvider(
            SubdirectoriesProviderArguments(
                directory_filter=directory_filter,
                converter=self.converter,
                entry_names_provider=self.entry_names_provider,
            )
        )

        provider_manager_validator = NoSubdirectoriesValidator()

        manager = SubdirectoriesManager(
            subdirectories_provider, provider_manager_validator
        )

        path_provider = FakeCliPathProvider()
        path_strategy = FakeGoodPathStrategy()
        path_provider.set_strategy(path_strategy)
        self.directory_path = path_strategy.get()

        directory_path_validators = [
            none_path_validator,
            not_existing_path_validator,
            self.non_directory_path_validator,
        ]
        directory_path_validator_manager = ValidatorManager[str](
            directory_path_validators
        )

        path_manager = PathManager(
            provider=path_provider, validator=directory_path_validator_manager
        )

        self.parts_provider = PartsProvider(
            path_provider=path_manager, subdirectories_provider=manager
        )

    def test_get(self):
        entry_names = self.entry_names_provider.get(self.directory_path)
        entries = self.converter.convert(
            SetEntryArguments(entry_names, self.directory_path)
        )
        self.non_directory_path_validator.update_directories(
            {entry.path: "directory" in entry.name for entry in entries},
            {self.directory_path: True},
        )

        parts = self.parts_provider.get()

        expected_parts = {Part(name="directory1")}
        self.assertEqual(
            parts,
            expected_parts,
            "The parts aren't the same as expected",
        )

    def test_get_without_parts(self):
        self.entry_names_provider.set_strategy(FakeNoDirectoriesStrategy())
        entry_names = self.entry_names_provider.get(self.directory_path)
        entries = self.converter.convert(
            SetEntryArguments(entry_names, self.directory_path)
        )
        self.non_directory_path_validator.update_directories(
            {entry.path: False for entry in entries}, {self.directory_path: True}
        )

        with self.assertRaises(NoPartsException):
            self.parts_provider.get()
