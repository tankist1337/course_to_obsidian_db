from abc import ABC, abstractmethod
from typing import Optional

from base.validator import IValidator, ValidatorManager
from entry.entry import FileSystemEntry
from entry.entry_factory import FileFactory, IEntryFactory
from entry.entry_validator import (
    EntryAdapterForPathValidator,
    InvalidEntryNameCharactersValidator,
    InvalidEntryNameValidator,
)
from entry.invalid_entry_name_character_provider import (
    LinuxInvalidEntryNameCharacterProvider,
)
from entry.invalid_entry_names_provider import LinuxInvalidEntryNameProvider
from file.file_filter import FileFilter, IFileFilter
from tests.fake_path_validator import (
    FakeExistingPathValidator,
    FakeFilePathValidator,
    IFakeExistingPathValidator,
    IFakeFilePathValidator,
)


class IFakeFileFilter(IFileFilter, ABC):
    @abstractmethod
    def build(self):
        pass

    @abstractmethod
    def set_validator(self, validator: Optional[IValidator[FileSystemEntry]]):
        pass

    @abstractmethod
    def set_file_path_validator(self, validator: IFakeFilePathValidator):
        pass

    @abstractmethod
    def set_existing_path_validator(self, validator: IFakeExistingPathValidator):
        pass


class FakeDefaultFileFilter(IFakeFileFilter):
    _file_factory: IEntryFactory
    _validator: Optional[IValidator[FileSystemEntry]]
    _file_path_validator: Optional[IFakeFilePathValidator]
    _existing_path_validator: Optional[IFakeExistingPathValidator]
    _file_filter: IFileFilter

    def __init__(self):
        self._setup()

        self.build()

    def build(self):
        self._file_filter = FileFilter(
            validator=self._validator, factory=self._file_factory
        )

    def _setup(self):
        self._invalid_characters_provider = LinuxInvalidEntryNameCharacterProvider()

        self._existing_path_validator = FakeExistingPathValidator()
        self._file_path_validator = FakeFilePathValidator()

        invalid_characters_validator = InvalidEntryNameCharactersValidator(
            self._invalid_characters_provider
        )
        self._invalid_names_provider = LinuxInvalidEntryNameProvider()
        invalid_name_validator = InvalidEntryNameValidator(self._invalid_names_provider)
        existing_entry_validator = EntryAdapterForPathValidator(
            self._existing_path_validator
        )
        file_entry_validator = EntryAdapterForPathValidator(self._file_path_validator)

        validators = [
            invalid_name_validator,
            invalid_characters_validator,
            existing_entry_validator,
            file_entry_validator,
        ]

        self._validator = ValidatorManager[FileSystemEntry](validators=validators)

        self._file_factory = FileFactory()

    def set_file_path_validator(self, validator):
        self._file_path_validator = validator

    def set_existing_path_validator(self, validator):
        self._existing_path_validator = validator

    # TODO: Review this logic because
    # it looks unstable and unpredictable for the complicated system
    # by default i have validator with sequence of validators
    # two of these validators are fakes
    # that i need adjust outer to get expected test cases
    def set_validator(self, validator: Optional[IValidator[FileSystemEntry]]):
        self._existing_path_validator = None
        self._file_path_validator = None
        self._validator = validator

    def filter(self, entries):
        if self._file_path_validator:
            self._file_path_validator.update(
                {
                    entry.path: ("all_good.txt" in entry.name) or ("file" in entry.name)
                    for entry in entries
                }
            )
        return self._file_filter.filter(entries)


class FakeFileFilterWithNotExistingEntry(FakeDefaultFileFilter):
    def filter(self, entries):
        self._existing_path_validator.update({entry.path: False for entry in entries})
        return self._file_filter.filter(entries)
