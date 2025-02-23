import unittest

from base.validator import ValidatorManager
from directory.directory_filter import DirectoryFilter
from directory.directory_provider import DirectoryProvider
from entry.converter.entry_arguments import SetEntryArguments
from entry.converter.entry_converter import SetEntryConverter
from entry.entry import Directory, FileSystemEntry
from entry.entry_factory import DirectoryFactory
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
from part.part import Part
from part.part_converter import PartConverter
from part.part_provider import PartProvider
from path.provider.path_provider import PathManager
from path.validator.path_validator import NonePathValidator
from tests.fake_entry_name_provider import (
    FakeNeutralStrategy,
    FakeNoEntryNamesStrategy,
    FakeOsListdirEntryNamesProvider,
)
from tests.path_validator_test import (
    FakeNonDirectoryPathValidator,
    FakeNotExistingPathValidator,
)
from tests.path_provider_test import FakeCliPathProvider, FakeGoodPathStrategy


class TestPartProvider(unittest.TestCase):
    def setUp(self):
        # Directory path validator
        none_path_validator = NonePathValidator()
        self.not_existing_path_validator = FakeNotExistingPathValidator()
        self.non_directory_path_validator = FakeNonDirectoryPathValidator()
        directory_path_validators = [
            none_path_validator,
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

        # Directory path manager
        path_provider = FakeCliPathProvider(FakeGoodPathStrategy())
        path_manager = PathManager(
            provider=path_provider, validator=directory_path_validator_manager
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
            validator=directory_filter_validator,
            directory_factory=directory_factory,
        )

        # directory provider
        directory_provider = DirectoryProvider(
            entry_provider=self.entry_provider,
            directory_filter=directory_filter,
        )

        # Part provider
        part_converter = PartConverter()

        self.part_provider = PartProvider(
            path_provider=path_manager,
            directory_provider=directory_provider,
            converter=part_converter,
        )

    def test_get(self):
        entry_names = self.entry_names_provider.get(self.directory_path)
        entries = self.converter.convert(
            SetEntryArguments(entry_names, self.directory_path)
        )
        self.non_directory_path_validator.update_directories(
            {entry.path: "directory" in entry.name for entry in entries},
        )

        parts = self.part_provider.get()

        expected_parts = {
            Part(
                directory=Directory(
                    name="directory1",
                    directory_path="directory/for/tests/",
                    path="directory/for/tests/directory1",
                ),
            )
        }
        self.assertEqual(
            parts,
            expected_parts,
            "The parts aren't the same as expected",
        )

    def test_get_no_parts(self):
        self.entry_names_provider.set_strategy(FakeNoEntryNamesStrategy())

        parts = self.part_provider.get()

        self.assertEqual(len(parts), 0, "It must be empty")
