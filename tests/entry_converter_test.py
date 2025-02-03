import unittest

from entry.converter.entry_arguments import (
    SingleEntryArguments,
    ListEntryArguments,
)
from entry.converter.entry_converter import (
    SingleEntryConverter,
    ListEntryConverter,
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
        self.assertEqual(expected_entry, actual_entry)

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
        self.assertEqual(expected_entry, actual_entry)

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
        self.assertEqual(expected_entry, actual_entry)

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
        self.assertEqual(expected_entry, actual_entry)

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
        self.assertEqual(expected_entry, actual_entry)

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
        self.assertEqual(expected_entry, actual_entry)


class TestListEntryConverter(unittest.TestCase):
    def setUp(self):
        separator_provider = LinuxSeparatorProvider()
        self.separator = separator_provider.get()
        self.converter = ListEntryConverter(separator_provider)

    def __assert_result(self, names, directory_path, separator, entries):
        expected_set = {
            FileSystemEntry(
                name=name,
                directory_path=directory_path,
                path=f"{directory_path}{separator}{name}",
            )
            for name in names
        }
        actual_set = set(entries)
        self.assertEqual(
            expected_set, actual_set, "The entries do not match the expected ones"
        )

    def test_convert_path_is_not_closed_by_separator(self):
        names = ["subdirectory1", "subdirectory2"]
        directory_path = "directory/for/tests"
        arguments = ListEntryArguments(names, directory_path)

        entries = self.converter.convert(arguments)

        self.__assert_result(names, directory_path, self.separator, entries)

    def test_convert_path_is_closed_by_separator(self):
        names = ["subdirectory1", "subdirectory2"]
        directory_path = "directory/for/tests/"
        arguments = ListEntryArguments(names, directory_path)

        entries = self.converter.convert(arguments)

        self.__assert_result(names, directory_path, "", entries)

    def test_convert_with_empty_names(self):
        names = ["", "subdirectory1"]
        directory_path = "directory/for/tests"
        arguments = ListEntryArguments(names, directory_path)

        entries = self.converter.convert(arguments)

        self.__assert_result(names, directory_path, self.separator, entries)

    def test_convert_with_empty_directory_path(self):
        names = ["subdirectory1", "subdirectory2"]
        directory_path = ""
        arguments = ListEntryArguments(names, directory_path)

        entries = self.converter.convert(arguments)

        self.__assert_result(names, directory_path, self.separator, entries)

    def test_convert_with_empty_name_list(self):
        names = []
        directory_path = ""
        arguments = ListEntryArguments(names, directory_path)

        entries = self.converter.convert(arguments)

        self.assertEqual(
            len(entries),
            0,
            "The empty list of names isn't returning the empty list of entries",
        )

    def test_convert_with_empty_name_and_directory_path(self):
        names = ["", "subdirectory1"]
        directory_path = ""
        arguments = ListEntryArguments(names, directory_path)

        entries = self.converter.convert(arguments)

        self.__assert_result(names, directory_path, self.separator, entries)

    def test_convert_with_invalid_path(self):
        names = ["//\\$@!^#&!$&,.*!^$~%()", "&*(n598327-)%(*=25#N-)"]
        directory_path = '\\&!#$%^,.@#&*%:?".'
        arguments = ListEntryArguments(names, directory_path)

        entries = self.converter.convert(arguments)

        self.__assert_result(names, directory_path, self.separator, entries)
