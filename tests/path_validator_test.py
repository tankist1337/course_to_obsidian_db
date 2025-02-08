import unittest

from entry.entry import FileSystemEntry
from entry.entry_validator import EntryAdapterForPathValidator
from path.validator.path_exception import (
    NonePathException,
    NonDirectoryPathException,
    NotExistingPathException,
)
from path.validator.path_validator import (
    IPathValidator,
    NonePathValidator,
)


class TestNonePathValidator(unittest.TestCase):
    def setUp(self):
        self.validator = NonePathValidator()

    def test_validate_without_none(self):
        path = "directory/for/tests/"

        self.validator.validate(path)

    def test_validate_with_none(self):
        path = None

        with self.assertRaises(NonePathException):
            self.validator.validate(path)


class TestNonDirectoryPathValidator(unittest.TestCase):
    def test_validate_is_directory(self):
        path = "directory/for/tests/"
        validator = FakeNonDirectoryPathValidator(directory_dictionary={path: True})

        validator.validate(path)

    def test_validate_is_not_directory(self):
        path = "directory/for/tests/raise.txt"
        validator = FakeNonDirectoryPathValidator(directory_dictionary={path: False})

        with self.assertRaises(NonDirectoryPathException):
            validator.validate(path)


class TestNotExistingPathValidator(unittest.TestCase):
    def test_validate_is_existing(self):
        path = "directory/for/tests/raise.txt"
        validator = FakeNotExistingPathValidator(existing_path_dictionary={path: True})

        validator.validate(path)

    def test_validate_is_not_existing(self):
        path = "directory/for/tests/raise.png"
        validator = FakeNotExistingPathValidator(existing_path_dictionary={path: False})

        with self.assertRaises(NotExistingPathException):
            validator.validate(path)


class FakeNotExistingPathValidator(IPathValidator):
    def __init__(self, existing_path_dictionary: dict[str, bool] = None):
        self.existing_path_dictionary = existing_path_dictionary

    def set_existing_paths(self, existing_path_dictionary: dict[str, bool]):
        self.existing_path_dictionary = existing_path_dictionary

    def update_existing_paths(self, *args: dict[str, bool]):
        merged_dictionary = {}
        for dictionary in args:
            merged_dictionary.update(dictionary)

        if self.existing_path_dictionary:
            self.existing_path_dictionary.update(merged_dictionary)
        else:
            self.set_existing_paths(merged_dictionary)

    def validate(self, item):
        if self.existing_path_dictionary is not None:
            if self.existing_path_dictionary.get(item) is not True:
                raise NotExistingPathException(f'The path "{item}" does not exist')
        else:
            # All paths are existing
            pass


class FakeNonDirectoryPathValidator(IPathValidator):
    def __init__(self, directory_dictionary: dict[str, bool] = None):
        self.directory_dictionary = directory_dictionary

    def set_directories(self, directory_dictionary: dict[str, bool]):
        self.directory_dictionary = directory_dictionary

    def update_directories(self, *args: dict[str, bool]):
        merged_dictionary = {}
        for dictionary in args:
            merged_dictionary.update(dictionary)

        if self.directory_dictionary:
            self.directory_dictionary.update(merged_dictionary)
        else:
            self.set_directories(merged_dictionary)

    def validate(self, item):
        if self.directory_dictionary is not None:
            if self.directory_dictionary.get(item) is not True:
                raise NonDirectoryPathException(f'The path "{item}" isn\'t a directory')
        else:
            # All paths are directories
            pass


class TestEntryAdapterForPathValidator(unittest.TestCase):
    def setUp(self):
        self.path_validator = FakePathValidator()
        self.entry_validator = EntryAdapterForPathValidator(self.path_validator)

    def test_validate(self):
        name = "subdirectory1"
        directory_path = "directory/for/tests/"
        path = directory_path + name
        entry = FileSystemEntry(name, directory_path, path)

        self.entry_validator.validate(entry)

        self.path_validator.assert_called_times(1)
        self.path_validator.assert_called_with(entry.path)


class FakePathValidator(IPathValidator, unittest.TestCase):
    __called_with = []
    __called_times = 0

    def assert_called_times(self, expected: int):
        self.assertEqual(self.__called_times, expected)

    def assert_called_with(self, expected: str):
        self.assertIn(expected, self.__called_with)

    def validate(self, item):
        self.__called_with.append(item)
        self.__called_times += 1
