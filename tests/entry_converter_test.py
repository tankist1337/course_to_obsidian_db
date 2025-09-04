import unittest

from entry.converter.entry_arguments import (
    SetEntryArguments,
    SingleEntryArguments,
)
from entry.converter.entry_converter import (
    SetEntryConverter,
    SingleEntryConverter,
)
from entry.entry import FileSystemEntry
from entry.separator_provider import LinuxSeparatorProvider


class TestSingleEntryConverter(unittest.TestCase):
    def setUp(self):
        separator_provider = LinuxSeparatorProvider()
        self.separator = separator_provider.get()
        self.converter = SingleEntryConverter(separator_provider)

    def test_convert_path_is_not_closed_by_separator(self):
        name = "subdirectory1"
        directory_path = "directory/for/tests"
        arguments = SingleEntryArguments(name, directory_path)

        actual_entry = self.converter.convert(arguments)

        expected_entry = FileSystemEntry(
            name=name,
            directory_path=directory_path,
            path=directory_path + self.separator + name,
        )
        self.assertEqual(expected_entry, actual_entry, "Entry isn't as expected")

    def test_convert_path_is_closed_by_separator(self):
        name = "subdirectory1"
        directory_path = "directory/for/tests/"
        arguments = SingleEntryArguments(name, directory_path)

        actual_entry = self.converter.convert(arguments)

        expected_entry = FileSystemEntry(
            name=name,
            directory_path=directory_path,
            path=directory_path + name,
        )
        self.assertEqual(expected_entry, actual_entry, "Entry isn't as expected")

    def test_convert_with_empty_name(self):
        name = ""
        directory_path = "directory/for/tests"
        arguments = SingleEntryArguments(name, directory_path)

        actual_entry = self.converter.convert(arguments)

        expected_entry = FileSystemEntry(
            name=name,
            directory_path=directory_path,
            path=directory_path + self.separator + name,
        )
        self.assertEqual(expected_entry, actual_entry, "Entry isn't as expected")

    def test_convert_with_empty_directory_path(self):
        name = "subdirectory1"
        directory_path = ""
        arguments = SingleEntryArguments(name, directory_path)

        actual_entry = self.converter.convert(arguments)

        expected_entry = FileSystemEntry(
            name=name,
            directory_path=directory_path,
            path=directory_path + self.separator + name,
        )
        self.assertEqual(expected_entry, actual_entry, "Entry isn't as expected")

    def test_convert_with_empty_name_and_directory_path(self):
        name = ""
        directory_path = ""
        arguments = SingleEntryArguments(name, directory_path)

        actual_entry = self.converter.convert(arguments)

        expected_entry = FileSystemEntry(
            name=name,
            directory_path=directory_path,
            path=directory_path + self.separator + name,
        )
        self.assertEqual(expected_entry, actual_entry, "Entry isn't as expected")

    def test_convert_with_invalid_path(self):
        name = "//\\$@!^#&!$&,.*!^$~%()"
        directory_path = '\\&!#$%^,.@#&*%:?".'
        arguments = SingleEntryArguments(name, directory_path)

        actual_entry = self.converter.convert(arguments)

        expected_entry = FileSystemEntry(
            name=name,
            directory_path=directory_path,
            path=directory_path + self.separator + name,
        )
        self.assertEqual(expected_entry, actual_entry, "Entry isn't as expected")


class TestSetEntryConverter(unittest.TestCase):
    def setUp(self):
        separator_provider = LinuxSeparatorProvider()
        self.separator = separator_provider.get()
        self.converter = SetEntryConverter(separator_provider)

    def __assert_result(self, names, directory_path, separator, entries):
        expected = {
            FileSystemEntry(
                name=name,
                directory_path=directory_path,
                path=directory_path + separator + name,
            )
            for name in names
        }
        self.assertEqual(
            entries, expected, "The entries do not match the expected ones"
        )

    def test_convert_path_is_not_closed_by_separator(self):
        names = {"subdirectory1", "subdirectory2"}
        directory_path = "directory/for/tests"
        arguments = SetEntryArguments(names, directory_path)

        entries = self.converter.convert(arguments)

        self.__assert_result(names, directory_path, self.separator, entries)

    def test_convert_path_is_closed_by_separator(self):
        names = {"subdirectory1", "subdirectory2"}
        directory_path = "directory/for/tests/"
        arguments = SetEntryArguments(names, directory_path)

        entries = self.converter.convert(arguments)

        self.__assert_result(names, directory_path, "", entries)
