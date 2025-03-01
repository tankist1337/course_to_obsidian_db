from abc import ABC, abstractmethod
from typing import Optional
from base.validator import IValidator, ValidatorManager
from directory.directory_filter import DirectoryFilter, IDirectoryFilter
from entry.entry import FileSystemEntry
from entry.entry_factory import DirectoryFactory, IEntryFactory
from entry.entry_validator import (
    EntryAdapterForPathValidator,
    InvalidEntryNameCharactersValidator,
    InvalidEntryNameValidator,
)
from entry.invalid_entry_name_character_provider import (
    LinuxInvalidEntryNameCharacterProvider,
)
from entry.invalid_entry_names_provider import LinuxInvalidEntryNameProvider
from tests.fake_path_validator import (
    FakeDirectoryPathValidator,
    FakeExistingPathValidator,
)


class IFakeDirectoryFilter(IDirectoryFilter, ABC):
    @abstractmethod
    def set_validator(self, validator: Optional[IValidator[FileSystemEntry]]):
        pass

    @abstractmethod
    def build(self):
        pass


class FakeDefaultDirectoryFilter(IFakeDirectoryFilter):
    _validator: Optional[IValidator[FileSystemEntry]]
    _directory_factory: IEntryFactory
    _filter: IDirectoryFilter

    def __init__(self):
        self._setup()

        self.build()

    def build(self):
        self._filter = DirectoryFilter(
            validator=self._validator,
            directory_factory=self._directory_factory,
        )

    def _setup(self):
        invalid_characters_provider = LinuxInvalidEntryNameCharacterProvider()
        invalid_names_provider = LinuxInvalidEntryNameProvider()
        self._directory_path_validator = FakeDirectoryPathValidator()
        self._existing_path_validator = FakeExistingPathValidator()

        invalid_characters_validator = InvalidEntryNameCharactersValidator(
            invalid_characters_provider
        )
        invalid_name_validator = InvalidEntryNameValidator(invalid_names_provider)
        directory_entry_validator = EntryAdapterForPathValidator(
            self._directory_path_validator
        )
        existing_entry_validator = EntryAdapterForPathValidator(
            self._existing_path_validator
        )
        validators = [
            invalid_name_validator,
            invalid_characters_validator,
            existing_entry_validator,
            directory_entry_validator,
        ]
        self._validator = ValidatorManager[FileSystemEntry](validators=validators)
        self._directory_factory = DirectoryFactory()

    def set_validator(self, validator: Optional[IValidator[FileSystemEntry]]):
        self._validator = validator

    def filter(self, entries):
        self._directory_path_validator.update(
            {entry.path: "directory" in entry.name for entry in entries}
        )
        return self._filter.filter(entries)


class FakeDirectoryFilterWithNotExistingEntry(FakeDefaultDirectoryFilter):
    def filter(self, entries):
        self._existing_path_validator.update({entry.path: False for entry in entries})
        return self._filter.filter(entries)
