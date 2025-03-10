import unittest

from entry.entry import FileSystemEntry
from entry.entry_exception import (
    InvalidEntryNameCharacterException,
    InvalidEntryNameException,
)
from entry.entry_validator import (
    InvalidEntryNameCharactersValidator,
    InvalidEntryNameValidator,
)
from entry.invalid_entry_name_character_provider import (
    LinuxInvalidEntryNameCharacterProvider,
)
from entry.invalid_entry_names_provider import (
    LinuxInvalidEntryNameProvider,
)
from tests.fake_entry_validator import FakeEntryWithInvalidCharactersMaker


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
