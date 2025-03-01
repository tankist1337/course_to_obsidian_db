import unittest

from entry.entry import File
from path.validator.path_exception import (
    NonDirectoryPathException,
    NotExistingPathException,
)

from tests.fake_file_provider import (
    FakeDefaultFileProvider,
    FakeEmptyFileProvider,
    FakeFileProviderWithFilePath,
    FakeFileProviderWithNotExistingPath,
)


class TestFileProvider(unittest.TestCase):
    def test_get(self):
        path = "directory/for/tests/"
        provider = FakeDefaultFileProvider()

        files = provider.get(path)

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
        path = "directory/for/tests/"
        provider = FakeEmptyFileProvider()

        files = provider.get(path)

        self.assertEqual(
            len(files),
            0,
            f'The directory "{path}" mustn\'t have any files',
        )

    def test_get_with_directory_path_not_closed_by_separator(self):
        path = "directory/for/tests"
        provider = FakeDefaultFileProvider()

        files = provider.get(path)

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
        path = "directory/for/tests/"
        provider = FakeFileProviderWithNotExistingPath()

        with self.assertRaises(NotExistingPathException):
            provider.get(path)

    def test_get_with_file_path(self):
        path = "directory/for/file1.txt"
        provider = FakeFileProviderWithFilePath()

        with self.assertRaises(NonDirectoryPathException):
            provider.get(path)
