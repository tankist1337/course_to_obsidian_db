from abc import ABC, abstractmethod
from typing import Optional

from base.validator import IValidator, ValidatorManager
from directory.directory_provider import DirectoryProvider, IDirectoryProvider
from entry.entry_validator import (
    EntryAdapterForPathValidator,
)
from tests.fake_director_filter import FakeDefaultDirectoryFilter, IFakeDirectoryFilter
from tests.fake_entry_provider import (
    FakeDefaultEntryProvider,
    IFakeEntryProvider,
    FakeEntryProviderWithoutDirectories,
)
from tests.fake_path_validator import (
    FakeDirectoryPathValidator,
    FakeExistingPathValidator,
    IFakeDirectoryPathValidator,
    IFakeExistingPathValidator,
)


class IFakeDirectoryProvider(IDirectoryProvider, ABC):
    @abstractmethod
    def set_existing_path_validator(self, validator: IFakeExistingPathValidator):
        pass

    @abstractmethod
    def build(self):
        pass


class FakeDefaultDirectoryProvider(IFakeDirectoryProvider):
    _entry_provider: IFakeEntryProvider
    _existing_path_validator: IFakeExistingPathValidator
    _directory_path_validator: IFakeDirectoryPathValidator
    _path_validator: Optional[IValidator[str]]
    _directory_filter: IFakeDirectoryFilter
    _directory_provider: IDirectoryProvider

    def __init__(self):
        self._setup()

        self.build()

    def build(self):
        self._directory_provider = DirectoryProvider(
            entry_provider=self._entry_provider,
            directory_filter=self._directory_filter,
            directory_path_validator=self._path_validator,
        )

    def _setup(self):
        # Directory path validator
        self._existing_path_validator = FakeExistingPathValidator()
        self._directory_path_validator = FakeDirectoryPathValidator()
        path_validators = [
            self._existing_path_validator,
            self._directory_path_validator,
        ]
        self._path_validator = ValidatorManager[str](path_validators)

        # Entry provider
        self._entry_provider = FakeDefaultEntryProvider()
        self._entry_provider.set_directory_path_validator(
            self._directory_path_validator
        )
        self._entry_provider.set_existing_path_validator(self._existing_path_validator)
        self._entry_provider.set_path_validator(None)
        self._entry_provider.build()

        # Directory filter
        directory_filter_validator = EntryAdapterForPathValidator(
            self._directory_path_validator
        )
        self._directory_filter = FakeDefaultDirectoryFilter()
        self._directory_filter.set_validator(directory_filter_validator)
        self._directory_filter.build()

    def set_existing_path_validator(self, validator: IFakeExistingPathValidator):
        self._existing_path_validator = validator

    def get(self, directory_path):
        entries = self._entry_provider.get(directory_path)
        self._directory_path_validator.update(
            {entry.path: "directory" in entry.name for entry in entries},
            {directory_path: True},
        )
        return self._directory_provider.get(directory_path)


class FakeEmptyDirectoryProvider(FakeDefaultDirectoryProvider):
    def _setup(self):
        super()._setup()
        self._entry_provider = FakeEntryProviderWithoutDirectories()
        self._entry_provider.set_directory_path_validator(
            self._directory_path_validator
        )
        self._entry_provider.set_existing_path_validator(self._existing_path_validator)
        self._entry_provider.set_path_validator(None)
        self._entry_provider.build()


class FakeDirectoryProviderWithNotExistingPath(FakeDefaultDirectoryProvider):
    def get(self, directory_path):
        self._existing_path_validator.update({directory_path: False})
        return self._directory_provider.get(directory_path)


class FakeDirectoryProviderWithFilePath(FakeDefaultDirectoryProvider):
    def get(self, directory_path):
        self._directory_path_validator.update({directory_path: False})
        return self._directory_provider.get(directory_path)
