import unittest

from entry.entry import FileSystemEntry
from entry.entry_validator import EntryAdapterForPathValidator
from path.validator.path_exception import (
    NonePathException,
)
from path.validator.path_validator import (
    NonePathValidator,
)
from tests.fake_path_validator import (
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
