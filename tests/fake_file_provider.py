from abc import ABC, abstractmethod
from typing import Optional

from base.validator import IValidator, ValidatorManager
from entry.entry_validator import (
    EntryAdapterForPathValidator,
)
from file.file_provider import FileProvider, IFileProvider
from tests.fake_entry_provider import (
    FakeDefaultEntryProvider,
    FakeEntryProviderWithoutFiles,
    IFakeEntryProvider,
)
from tests.fake_file_filter import FakeDefaultFileFilter, IFakeFileFilter
from tests.fake_path_validator import (
    FakeDirectoryPathValidator,
    FakeExistingPathValidator,
    FakeFilePathValidator,
    IFakeDirectoryPathValidator,
    IFakeExistingPathValidator,
    IFakeFilePathValidator,
)


class IFakeFileProvider(IFileProvider, ABC):
    @abstractmethod
    def set_file_path_validator(self, validator: Optional[IFakeFilePathValidator]):
        pass

    @abstractmethod
    def set_existing_path_validator(
        self, validator: Optional[IFakeExistingPathValidator]
    ):
        pass

    @abstractmethod
    def set_path_validator(self, validator: Optional[IValidator[str]]):
        pass

    @abstractmethod
    def build(self):
        pass


class FakeDefaultFileProvider(IFakeFileProvider):
    _file_path_validator: Optional[IFakeFilePathValidator]
    _directory_path_validator: Optional[IFakeDirectoryPathValidator]
    _existing_path_validator: Optional[IFakeExistingPathValidator]
    _path_validator: Optional[IValidator[str]]
    _entry_provider: IFakeEntryProvider
    _file_filter: IFakeFileFilter
    _file_provider: IFileProvider

    def __init__(self):
        self._setup()

        self.build()

    def build(self):
        self._file_provider = FileProvider(
            entry_provider=self._entry_provider,
            file_filter=self._file_filter,
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

        # File filter
        self._file_filter = FakeDefaultFileFilter()

        self._file_path_validator = FakeFilePathValidator()
        file_entry_validator = EntryAdapterForPathValidator(self._file_path_validator)

        self._file_filter.set_validator(file_entry_validator)
        self._file_filter.set_file_path_validator(self._file_path_validator)
        self._file_filter.build()

        # directory provider
        self.file_provider = FileProvider(
            entry_provider=self._entry_provider,
            file_filter=self._file_filter,
            directory_path_validator=self._path_validator,
        )

    def set_file_path_validator(self, validator: Optional[IFakeFilePathValidator]):
        self._file_path_validator = validator

    def set_existing_path_validator(
        self, validator: Optional[IFakeExistingPathValidator]
    ):
        self._existing_path_validator = validator

    def set_path_validator(self, validator: Optional[IValidator[str]]):
        self._path_validator = validator

    def get(self, directory_path):
        self._existing_path_validator.update({directory_path: True})
        return self._file_provider.get(directory_path)


class FakeEmptyFileProvider(FakeDefaultFileProvider):
    def _setup(self):
        super()._setup()

        self._entry_provider = FakeEntryProviderWithoutFiles()
        self._entry_provider.set_directory_path_validator(
            self._directory_path_validator
        )
        self._entry_provider.set_existing_path_validator(self._existing_path_validator)
        self._entry_provider.set_path_validator(None)
        self._entry_provider.build()


class FakeFileProviderWithNotExistingPath(FakeDefaultFileProvider):
    def get(self, directory_path):
        self._existing_path_validator.update({directory_path: False})
        return self._file_provider.get(directory_path)


class FakeFileProviderWithFilePath(FakeDefaultFileProvider):
    def get(self, directory_path):
        self._directory_path_validator.update({directory_path: False})
        return self._file_provider.get(directory_path)
