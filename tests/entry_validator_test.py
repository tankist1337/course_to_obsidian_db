import unittest

from entry.entry import FileSystemEntry
from entry.entry_exception import (
    InvalidEntryNameCharactersException,
    InvalidEntryNameException,
)
from entry.entry_validator import (
    IEntryValidator,
    InvalidEntryNameCharactersValidator,
    InvalidEntryNameValidator,
)
from entry.invalid_entry_name_characters_provider import (
    IInvalidEntryNameCharactersProvider,
    LinuxInvalidEntryNameCharactersProvider,
)
from entry.invalid_entry_names_provider import (
    LinuxInvalidEntryNamesProvider,
)
from path.validator.path_exception import (
    NonDirectoryPathException,
    NotExistingPathException,
)


class TestInvalidEntryNameValidator(unittest.TestCase):
    def setUp(self):
        self.invalid_names_provider = LinuxInvalidEntryNamesProvider()
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
        self.invalid_characters_provider = LinuxInvalidEntryNameCharactersProvider()
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
            with self.assertRaises(InvalidEntryNameCharactersException):
                self.validator.validate(entry)


class FakeEntryWithInvalidCharactersMaker:
    def __init__(
        self,
        invalid_characters_provider: IInvalidEntryNameCharactersProvider,
    ):
        self.invalid_characters_provider = invalid_characters_provider

    def get(self, directory_path="directory/for/tests/"):
        invalid_characters = self.invalid_characters_provider.get()
        invalid_entries = set()

        for character in invalid_characters:
            name = "name_with_invalid_characters"

            invalid_name = f"{character}{name}"
            invalid_entry = FileSystemEntry(
                name=invalid_name,
                directory_path=directory_path,
                path=directory_path + invalid_name,
            )
            invalid_entries.add(invalid_entry)

            invalid_name = self.__put_character_in_center(name, character)
            invalid_entry = FileSystemEntry(
                name=invalid_name,
                directory_path=directory_path,
                path=directory_path + invalid_name,
            )
            invalid_entries.add(invalid_entry)

            invalid_name = f"{name}{character}"
            invalid_entry = FileSystemEntry(
                name=invalid_name,
                directory_path=directory_path,
                path=directory_path + invalid_name,
            )
            invalid_entries.add(invalid_entry)

        return invalid_entries

    def __put_character_in_center(self, name, character):
        center_index = int(len(name) / 2)
        return name[:center_index] + character + name[center_index:]


class TestNotExistingEntryValidator(unittest.TestCase):
    def setUp(self):
        self.validator = FakeNotExistingEntryValidator()

    def test_validate_existing_entry(self):
        entry = FileSystemEntry(
            name="subdirectory2",
            directory_path="directory/for/tests/",
            path="directory/for/tests/subdirectory2",
        )
        self.validator.existing_entries_dictionary = {entry: True}

        self.validator.validate(entry)

    def test_validate_not_existing_entry(self):
        entry = FileSystemEntry(
            name="not_existing_entry",
            directory_path="path/to/directory/",
            path="path/to/directory/not_existing_entry",
        )
        self.validator.existing_entries_dictionary = {entry: False}

        with self.assertRaises(NotExistingPathException):
            self.validator.validate(entry)


class FakeNotExistingEntryValidator(IEntryValidator):
    def __init__(self, existing_entries_dictionary: dict[FileSystemEntry, bool] = None):
        self.existing_entries_dictionary = existing_entries_dictionary

    def validate(self, item: FileSystemEntry):
        if self.existing_entries_dictionary is not None:
            if self.existing_entries_dictionary.get(item) is False:
                raise NotExistingPathException(f"The entry {item.path} isn't existing")
        else:
            # All files system entries are directories
            pass


class TestNonDirectoryEntryValidator(unittest.TestCase):
    def setUp(self):
        self.validator = FakeNonDirectoryEntryValidator()

    def test_validate_directory(self):
        entry = FileSystemEntry(
            name="directory1",
            directory_path="path/to/directory/",
            path="path/to/directory/directory1",
        )
        self.validator.directory_entries_dictionary = {entry: True}

        self.validator.validate(entry)

    def test_validate_non_directory(self):
        entry = FileSystemEntry(
            name="file1",
            directory_path="path/to/directory/",
            path="path/to/directory/file1",
        )
        self.validator.directory_entries_dictionary = {entry: False}

        with self.assertRaises(NonDirectoryPathException):
            self.validator.validate(entry)


class FakeNonDirectoryEntryValidator(IEntryValidator):
    def __init__(
        self, directory_entries_dictionary: dict[FileSystemEntry, bool] = None
    ):
        self.directory_entries_dictionary = directory_entries_dictionary

    def validate(self, item: FileSystemEntry):
        if self.directory_entries_dictionary is not None:
            if self.directory_entries_dictionary.get(item) is False:
                raise NonDirectoryPathException(
                    f"The entry {item.path} isn't a directory"
                )
        else:
            # All files system entries are directories
            pass
