import unittest

from entry.entry import Directory, FileSystemEntry
from entry.entry_factory import DirectoryFactory


class TestDirectoryFactory(unittest.TestCase):
    def test_from_entry(self):
        entry = FileSystemEntry(
            name="file_or_directory",
            directory_path="directory/for/tests",
            path="directory/for/tests/file_or_directory",
        )
        factory = DirectoryFactory()

        directory = factory.from_entry(entry)

        directory_expected = Directory(
            name="file_or_directory",
            directory_path="directory/for/tests",
            path="directory/for/tests/file_or_directory",
        )
        self.assertEqual(
            directory, directory_expected, "The directory isn't the same as expected"
        )
