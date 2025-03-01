import unittest
from unittest.mock import MagicMock

from directory.directory_provider import DirectoryProvider
from entry.entry import Directory, FileSystemEntry
from path.validator.path_exception import (
    NonDirectoryPathException,
    NotExistingPathException,
)
from tests.fake_directory_provider import (
    FakeDefaultDirectoryProvider,
    FakeDirectoryProviderWithFilePath,
    FakeDirectoryProviderWithNotExistingPath,
    FakeEmptyDirectoryProvider,
)


class TestDirectoryProvider(unittest.TestCase):
    def test_get(self):
        path = "directory/for/tests/"
        provider = FakeDefaultDirectoryProvider()

        directories = provider.get(path)

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

    def test_get_without_directories(self):
        path = "directory/for/tests/"
        provider = FakeEmptyDirectoryProvider()

        directories = provider.get(path)

        self.assertEqual(
            len(directories),
            0,
            f'The directory "{path}" mustn\'t have any directory',
        )

    def test_get_with_not_closed_by_separator_path(self):
        path = "directory/for/tests"
        provider = FakeDefaultDirectoryProvider()

        directories = provider.get(path)

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

    def test_get_with_not_existing_path(self):
        path = "directory/for/tests/"
        provider = FakeDirectoryProviderWithNotExistingPath()

        with self.assertRaises(NotExistingPathException):
            provider.get(path)

    def test_get_with_file_path(self):
        path = "directory/for/file.py"
        provider = FakeDirectoryProviderWithFilePath()

        with self.assertRaises(NonDirectoryPathException):
            provider.get(path)
