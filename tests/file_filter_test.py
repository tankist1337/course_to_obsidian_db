import unittest

from entry.entry import File, FileSystemEntry
from entry.entry_exception import (
    InvalidEntryNameCharacterException,
    InvalidEntryNameException,
)
from path.validator.path_exception import NotExistingPathException
from tests.entry_validator_test import (
    FakeEntryWithInvalidCharactersMaker,
)
from tests.fake_file_filter import (
    FakeFileFilterArgumentsBuilder,
    FakeNeutralFileFilter,
    FakeNotExistingEntryFileFilter,
)


class TestFileFilter(unittest.TestCase):
    def setUp(self):
        self.arguments = FakeFileFilterArgumentsBuilder().build()
        self.file_filter = FakeNeutralFileFilter(self.arguments)

    def test_filter(self):
        entries = {
            FileSystemEntry(
                name="file1.txt",
                directory_path="directory1/",
                path="directory1/file1.txt",
            ),
            FileSystemEntry(
                name="file2",
                directory_path="directory1/",
                path="directory1/file2",
            ),
            FileSystemEntry(
                name="directory1",
                directory_path="directory1/",
                path="directory1/directory1",
            ),
        }

        files = self.file_filter.filter(entries)

        expected_files = {
            File(
                name="file1.txt",
                directory_path="directory1/",
                path="directory1/file1.txt",
            ),
            File(
                name="file2",
                directory_path="directory1/",
                path="directory1/file2",
            ),
        }

        self.assertEqual(
            files,
            expected_files,
            "Files are not the same as the expected ones",
        )

    def test_filter_with_not_existing_entry(self):
        self.file_filter = FakeNotExistingEntryFileFilter(self.arguments)
        entry = FileSystemEntry(
            name="not_existing_directory1",
            directory_path="directory1/",
            path="directory1/not_existing_directory1",
        )
        entries = {entry}

        with self.assertRaises(NotExistingPathException):
            self.file_filter.filter(entries)

    def test_filter_with_invalid_characters_in_name(self):
        invalid_entry_maker = FakeEntryWithInvalidCharactersMaker(
            self.file_filter.invalid_characters_provider
        )
        entries = invalid_entry_maker.get()

        for entry in entries:
            with self.assertRaises(InvalidEntryNameCharacterException):
                self.file_filter.filter({entry})

    def test_filter_with_empty_entry_name(self):
        entry = FileSystemEntry(
            name="",
            directory_path="directory1/",
            path="directory1/",
        )
        entries = {entry}

        with self.assertRaises(InvalidEntryNameException):
            self.file_filter.filter(entries)

    def test_filter_with_reserved_entry_name(self):
        invalid_names = self.file_filter.invalid_names_provider.get()

        entries = {
            FileSystemEntry(
                name=invalid_name,
                directory_path="directory1/",
                path=f"directory1/{invalid_name}",
            )
            for invalid_name in invalid_names
        }

        for entry in entries:
            with self.assertRaises(InvalidEntryNameException):
                self.file_filter.filter({entry})

    def test_filter_with_no_files(self):
        entries = {
            FileSystemEntry(
                name="directory1",
                directory_path="directory1/",
                path="directory1/directory1",
            ),
            FileSystemEntry(
                name="directory2",
                directory_path="directory1/",
                path="directory1/directory2",
            ),
        }

        filtered_entries = self.file_filter.filter(entries)

        self.assertEqual(len(filtered_entries), 0, "There shouldn't be any files")

    def test_filter_with_no_entries(self):
        entry_paths = set()

        files = self.file_filter.filter(entry_paths)

        self.assertEqual(len(files), 0, "There shouldn't be any entries")
