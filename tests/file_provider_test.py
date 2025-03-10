import unittest
from unittest.mock import MagicMock

from base.validator import ValidatorManager
from entry.entry import File, FileSystemEntry
from entry.entry_factory import FileFactory
from entry.entry_validator import EntryAdapterForPathValidator
from file.file_filter import FileFilter
from file.file_provider import FileProvider
from path.validator.path_exception import (
    NonDirectoryPathException,
    NotExistingPathException,
)
from tests.fake_path_validator import (
    FakeDirectoryPathValidator,
    FakeExistingPathValidator,
    FakeFilePathValidator,
)


class TestFileProvider(unittest.TestCase):
    def setUp(self):
        self.entry_provider = MagicMock()
        self.entry_provider.get.return_value = {
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

        file_factory = FileFactory()
        file_path_validator = MagicMock()
        file_path_validator.validate.side_effect = FakeFilePathValidator.validate
        file_entry_validator = EntryAdapterForPathValidator(file_path_validator)
        file_filter = FileFilter(factory=file_factory, validator=file_entry_validator)

        existing_path_validator = MagicMock()
        existing_path_validator.validate.side_effect = (
            FakeExistingPathValidator.validate
        )
        directory_path_validator = MagicMock()
        directory_path_validator.validate.side_effect = (
            FakeDirectoryPathValidator.validate
        )
        path_validator_manager = ValidatorManager[str](
            [existing_path_validator, directory_path_validator]
        )

        self.file_provider = FileProvider(
            entry_provider=self.entry_provider,
            file_filter=file_filter,
            directory_path_validator=path_validator_manager,
        )

    def test_get(self):
        directory_path = "directory/for/tests/"

        files = self.file_provider.get(directory_path)

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
            "The files aren't the same as expected",
        )

    def test_get_with_no_files(self):
        directory_path = "directory/for/tests/"
        self.entry_provider.get.return_value = {
            FileSystemEntry(
                name="directory1",
                directory_path="directory/for/tests/",
                path="directory/for/tests/directory1",
            )
        }

        files = self.file_provider.get(directory_path)

        self.assertEqual(
            len(files),
            0,
            f'The directory "{directory_path}" mustn\'t have any files',
        )

    def test_get_with_directory_path_not_closed_by_separator(self):
        directory_path = "directory/for/tests"

        files = self.file_provider.get(directory_path)

        expected_files = {
            File(
                name="file1.txt",
                directory_path="directory/for/tests",
                path="directory/for/tests/file1.txt",
            ),
            File(
                name="file2",
                directory_path="directory/for/tests",
                path="directory/for/tests/file2",
            ),
        }
        self.assertEqual(
            files, expected_files, "Directories aren't the same as expected"
        )

    def test_get_with_not_existing_directory_path(self):
        directory_path = "not_existing_path"

        with self.assertRaises(NotExistingPathException):
            self.file_provider.get(directory_path)

    def test_get_with_non_directory_path(self):
        directory_path = "directory/for/tests/file2"

        with self.assertRaises(NonDirectoryPathException):
            self.file_provider.get(directory_path)
