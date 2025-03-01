import unittest

from entry.entry import FileSystemEntry
from entry.entry_exception import (
    InvalidEntryNameCharacterException,
    InvalidEntryNameException,
)
from entry.entry_validator import (
    EntryAdapterForPathValidator,
    InvalidEntryNameCharactersValidator,
    InvalidEntryNameValidator,
)
from entry.invalid_entry_name_character_provider import (
    LinuxInvalidEntryNameCharacterProvider,
)
from entry.invalid_entry_names_provider import (
    LinuxInvalidEntryNameProvider,
)
from path.validator.path_exception import (
    NonDirectoryPathException,
    NotExistingPathException,
)
from tests.fake_entry_validator import FakeEntryWithInvalidCharactersMaker
from tests.path_validator_test import (
    FakeDirectoryPathValidator,
    FakeExistingPathValidator,
)


class TestInvalidEntryNameValidator(unittest.TestCase):
    def setUp(self):
        self.invalid_names_provider = LinuxInvalidEntryNameProvider()
        self.validator = InvalidEntryNameValidator(self.invalid_names_provider)

    def test_validate_with_valid_name(self):
        entry = FileSystemEntry(
            name="valid_name",
            directory_path="directory/for/tests",
            path="directory/for/tests/valid_name",
        )

        self.validator.validate(entry)

    def test_validate_with_invalid_name(self):
        invalid_names = self.invalid_names_provider.get()
        directory_path = "directory/for/tests/"
        invalid_entries = {
            FileSystemEntry(
                name=invalid_name,
                directory_path=directory_path,
                path=directory_path + invalid_name,
            )
            for invalid_name in invalid_names
        }

        for invalid_entry in invalid_entries:
            with self.assertRaises(InvalidEntryNameException):
                self.validator.validate(invalid_entry)


class TestInvalidEntryNameCharactersValidator(unittest.TestCase):
    def setUp(self):
        self.invalid_characters_provider = LinuxInvalidEntryNameCharacterProvider()
        self.validator = InvalidEntryNameCharactersValidator(
            self.invalid_characters_provider
        )

    def test_validate_with_valid_characters_in_name(self):
        entry = FileSystemEntry(
            name="valid_name",
            directory_path="directory/for/tests",
            path="directory/for/tests/valid_name",
        )

        self.validator.validate(entry)

    def test_validate_with_invalid_characters_in_name(self):
        invalid_entries_maker = FakeEntryWithInvalidCharactersMaker(
            self.invalid_characters_provider
        )
        entries = invalid_entries_maker.get()

        for entry in entries:
            with self.assertRaises(InvalidEntryNameCharacterException):
                self.validator.validate(entry)


class TestExistingEntryValidator(unittest.TestCase):
    def setUp(self):
        self.path_validator = FakeExistingPathValidator()
        self.entry_validator = EntryAdapterForPathValidator(self.path_validator)

    def test_validate_existing_entry(self):
        entry = FileSystemEntry(
            name="subdirectory2",
            directory_path="directory/for/tests/",
            path="directory/for/tests/subdirectory2",
        )
        self.path_validator.update({entry.path: True})

        self.entry_validator.validate(entry)

    def test_validate_not_existing_entry(self):
        entry = FileSystemEntry(
            name="not_existing_entry",
            directory_path="path/to/directory/",
            path="path/to/directory/not_existing_entry",
        )
        self.path_validator.update({entry.path: False})

        with self.assertRaises(NotExistingPathException):
            self.entry_validator.validate(entry)


class TestDirectoryEntryValidator(unittest.TestCase):
    def setUp(self):
        self.path_validator = FakeDirectoryPathValidator()
        self.entry_validator = EntryAdapterForPathValidator(self.path_validator)

    def test_validate_directory(self):
        entry = FileSystemEntry(
            name="directory1",
            directory_path="path/to/directory/",
            path="path/to/directory/directory1",
        )
        self.path_validator.set({entry.path: True})

        self.entry_validator.validate(entry)

    def test_validate_non_directory(self):
        entry = FileSystemEntry(
            name="file1",
            directory_path="path/to/directory/",
            path="path/to/directory/file1",
        )
        self.path_validator.set({entry.path: False})

        with self.assertRaises(NonDirectoryPathException):
            self.entry_validator.validate(entry)
