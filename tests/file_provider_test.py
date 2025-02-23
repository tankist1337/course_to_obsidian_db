import unittest

from entry.entry import File
from path.validator.path_exception import (
    NonDirectoryPathException,
    NotExistingPathException,
)
from tests.fake_file_provider import (
    FakeFileProviderArgumentsBuilder,
    FakeNeutralFileProvider,
    FakeNoFilesFileProvider,
    FakeNonDirectoryPathFileProvider,
    FakeNotExistingPathFileProvider,
)


class TestFileProvider(unittest.TestCase):
    def setUp(self):
        self.arguments = FakeFileProviderArgumentsBuilder().build()

    def test_get(self):
        directory_path = "directory/for/tests/"
        file_provider = FakeNeutralFileProvider(self.arguments)

        files = file_provider.get(directory_path)

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
        directory_path = "directory/for/tests/"
        file_provider = FakeNoFilesFileProvider(self.arguments)

        files = file_provider.get(directory_path)

        self.assertEqual(
            len(files),
            0,
            f'The directory "{directory_path}" mustn\'t have any files',
        )

    def test_get_with_directory_path_not_closed_by_separator(self):
        directory_path = "directory/for/tests"
        file_provider = FakeNeutralFileProvider(self.arguments)

        files = file_provider.get(directory_path)

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
        directory_path = "directory/for/tests/"
        file_provider = FakeNotExistingPathFileProvider(self.arguments)

        file_provider.not_existing_path_validator.update_existing_paths(
            {directory_path: False}
        )

        with self.assertRaises(NotExistingPathException):
            file_provider.get(directory_path)

    def test_get_with_non_directory_path(self):
        directory_path = "directory/for/tests/"
        file_provider = FakeNonDirectoryPathFileProvider(self.arguments)

        with self.assertRaises(NonDirectoryPathException):
            file_provider.get(directory_path)
