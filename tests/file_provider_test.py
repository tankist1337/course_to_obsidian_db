import unittest

from base.validator import ValidatorManager
from entry.converter.entry_arguments import SetEntryArguments
from entry.converter.entry_converter import SetEntryConverter
from entry.entry import File, FileSystemEntry
from entry.entry_factory import FileFactory
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
    LinuxInvalidEntryNameProvider,
)
from entry.separator_provider import LinuxSeparatorProvider
from file.file_filter import FileFilter
from file.file_provider import FileProvider
from path.validator.path_exception import (
    NonDirectoryPathException,
    NotExistingPathException,
)
from tests.directory_provider_test import (
    FakeOsListdirEntryNamesProvider,
)
from tests.fake_entry_name_provider import FakeNoFilesStrategy
from tests.fake_path_validator import FakeNonFilePathValidator
from tests.path_validator_test import (
    FakeNonDirectoryPathValidator,
    FakeExistingPathValidator,
)


class TestFileProvider(unittest.TestCase):
    def setUp(self):
        # Directory path validator
        self.existing_path_validator = FakeExistingPathValidator()
        self.non_directory_path_validator = FakeNonDirectoryPathValidator()
        directory_path_validators = [
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
        invalid_characters_provider = LinuxInvalidEntryNameCharacterProvider()
        existing_entry_validator = EntryAdapterForPathValidator(
            self.existing_path_validator
        )
        invalid_characters_validator = InvalidEntryNameCharactersValidator(
            invalid_characters_provider
        )

        invalid_names_provider = LinuxInvalidEntryNameProvider()
        invalid_name_validator = InvalidEntryNameValidator(invalid_names_provider)

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
            entry_names_provider=self.entry_names_provider,
            converter=self.converter,
            entry_validator=entry_validator_manager,
        )

        # Directory filter
        self.non_file_path_validator = FakeNonFilePathValidator()
        non_file_entry_validator = EntryAdapterForPathValidator(
            self.non_file_path_validator
        )

        file_factory = FileFactory()
        file_filter = FileFilter(
            validator=non_file_entry_validator,
            factory=file_factory,
        )

        # directory provider
        self.file_provider = FileProvider(
            entry_provider=self.entry_provider,
            file_filter=file_filter,
            directory_path_validator=directory_path_validator_manager,
        )

    def test_get(self):
        entry_names = self.entry_names_provider.get(self.directory_path)
        entries = self.converter.convert(
            SetEntryArguments(entry_names, self.directory_path)
        )
        self.non_file_path_validator.update_files(
            {
                entry.path: ("all_good.txt" in entry.name) or ("file" in entry.name)
                for entry in entries
            }
        )

        files = self.file_provider.get(self.directory_path)

        expected_files = {
            File(
                name="file1",
                directory_path="directory/for/tests/",
                path="directory/for/tests/file1",
            ),
            File(
                name="all_good.txt",
                directory_path="directory/for/tests/",
                path="directory/for/tests/all_good.txt",
            ),
        }
        self.assertEqual(
            files,
            expected_files,
            "The files aren't the same as expected",
        )

    def test_get_with_no_files(self):
        self.entry_names_provider.set_strategy(FakeNoFilesStrategy())
        entry_names = self.entry_names_provider.get(self.directory_path)
        entries = self.converter.convert(
            SetEntryArguments(entry_names, self.directory_path)
        )
        self.non_file_path_validator.update_files(
            {
                entry.path: ("all_good.txt" in entry.name) or ("file" in entry.name)
                for entry in entries
            }
        )

        files = self.file_provider.get(self.directory_path)

        self.assertEqual(
            len(files),
            0,
            f'The directory "{self.directory_path}" mustn\'t have any files',
        )

    def test_get_with_directory_path_not_closed_by_separator(self):
        self.directory_path = "directory/for/tests"
        self.non_directory_path_validator.set_directories(
            {self.directory_path: True},
        )
        entry_names = self.entry_names_provider.get(self.directory_path)
        entries = self.converter.convert(
            SetEntryArguments(entry_names, self.directory_path)
        )
        self.non_file_path_validator.update_files(
            {
                entry.path: ("all_good.txt" in entry.name) or ("file" in entry.name)
                for entry in entries
            }
        )

        files = self.file_provider.get(self.directory_path)

        expected_files = {
            File(
                name="file1",
                directory_path="directory/for/tests",
                path="directory/for/tests/file1",
            ),
            File(
                name="all_good.txt",
                directory_path="directory/for/tests",
                path="directory/for/tests/all_good.txt",
            ),
        }
        self.assertEqual(
            files, expected_files, "Directories aren't the same as expected"
        )

    def test_get_with_not_existing_directory_path(self):
        self.existing_path_validator.update_existing_paths(
            {self.directory_path: False}
        )

        with self.assertRaises(NotExistingPathException):
            self.file_provider.get(self.directory_path)

    def test_get_with_non_directory_path(self):
        self.non_directory_path_validator.update_directories(
            {self.directory_path: False}
        )

        with self.assertRaises(NonDirectoryPathException):
            self.file_provider.get(self.directory_path)
