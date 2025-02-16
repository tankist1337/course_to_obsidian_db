import unittest

from entry.entry import FileSystemEntry
from entry.entry_validator import EntryAdapterForPathValidator
from path.validator.path_exception import (
    NonePathException,
    NonDirectoryPathException,
    NotExistingPathException,
)
from path.validator.path_validator import (
    NonePathValidator,
)
from tests.fake_path_validator import (
    FakeNonDirectoryPathValidator,
    FakeNotExistingPathValidator,
    FakePathValidator,
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
