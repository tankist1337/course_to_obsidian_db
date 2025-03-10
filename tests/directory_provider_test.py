import unittest
from unittest.mock import MagicMock

from base.validator import ValidatorManager
from directory.directory_filter import DirectoryFilter
from directory.directory_provider import DirectoryProvider
from entry.entry import Directory, FileSystemEntry
from entry.entry_factory import DirectoryFactory
from entry.entry_validator import EntryAdapterForPathValidator
from path.validator.path_exception import (
    NonDirectoryPathException,
    NotExistingPathException,
)
from tests.entry_provider_test import (
    FakeDirectoryPathValidator,
    FakeExistingPathValidator,
)


class TestDirectoryProvider(unittest.TestCase):
    def setUp(self):
        self.entry_provider = MagicMock()
        self.entry_provider.get.return_value = {
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
            FileSystemEntry(
                name="all_good.txt",
                directory_path="directory/for/tests/",
                path="directory/for/tests/all_good.txt",
            ),
        }
        directory_factory = DirectoryFactory()
        directory_path_validator = MagicMock()
        directory_path_validator.validate.side_effect = (
            FakeDirectoryPathValidator.validate
        )
        directory_entry_validator = EntryAdapterForPathValidator(
            directory_path_validator
        )
        directory_filter = DirectoryFilter(
            directory_factory=directory_factory, validator=directory_entry_validator
        )
        existing_path_validator = MagicMock()
        existing_path_validator.validate.side_effect = (
            FakeExistingPathValidator.validate
        )
        path_validator_manager = ValidatorManager[str](
            [existing_path_validator, directory_path_validator]
        )

        self.directory_provider = DirectoryProvider(
            entry_provider=self.entry_provider,
            directory_filter=directory_filter,
            directory_path_validator=path_validator_manager,
        )

    def test_get(self):
        directory_path = "directory/for/tests/"

        directories = self.directory_provider.get(directory_path)

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
        directory_path = "directory/for/tests/"
        self.entry_provider.get.return_value = {
            FileSystemEntry(
                name="file2",
                directory_path="directory/for/tests/",
                path="directory/for/tests/file2",
            ),
            FileSystemEntry(
                name="all_good.txt",
                directory_path="directory/for/tests/",
                path="directory/for/tests/all_good.txt",
            ),
        }

        directories = self.directory_provider.get(directory_path)

        self.assertEqual(
            len(directories),
            0,
            f'The directory "{directory_path}" mustn\'t have any directory',
        )

    def test_get_with_directory_path_not_closed_by_separator(self):
        directory_path = "directory/for/tests"

        directories = self.directory_provider.get(directory_path)

        expected_directories = {
            Directory(
                name="directory1",
                directory_path="directory/for/tests",
                path="directory/for/tests/directory1",
            )
        }
        self.assertEqual(
            directories, expected_directories, "Directories aren't the same as expected"
        )

    def test_get_with_not_existing_directory_path(self):
        directory_path = "not_existing_path"

        with self.assertRaises(NotExistingPathException):
            self.directory_provider.get(directory_path)

    def test_get_with_non_directory_path(self):
        directory_path = "directory/for/tests/file2"

        with self.assertRaises(NonDirectoryPathException):
            self.directory_provider.get(directory_path)
