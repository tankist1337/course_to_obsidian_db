from abc import ABC, abstractmethod
from typing import Optional
from base.validator import IValidator, ValidatorManager
from entry.converter.entry_arguments import SetEntryArguments
from entry.converter.entry_converter import IEntryConverter, SetEntryConverter
from entry.entry import FileSystemEntry
from entry.entry_name_provider import IEntryNameProvider
from entry.entry_provider import EntryProvider, IEntryProvider
from entry.entry_validator import (
    EntryAdapterForPathValidator,
    InvalidEntryNameCharactersValidator,
    InvalidEntryNameValidator,
)
from entry.invalid_entry_name_character_provider import (
    IInvalidEntryNameCharacterProvider,
    LinuxInvalidEntryNameCharacterProvider,
)
from entry.invalid_entry_names_provider import (
    IInvalidEntryNameProvider,
    LinuxInvalidEntryNameProvider,
)
from entry.separator_provider import LinuxSeparatorProvider
from tests.fake_entry_name_provider import (
    FakeInvalidCharactersInName,
    FakeInvalidNamesStrategy,
    FakeNoDirectoriesStrategy,
    FakeNoEntryNamesStrategy,
    FakeNoFilesStrategy,
    FakeOsListdirEntryNamesProvider,
)
from tests.fake_entry_validator import FakeEntryWithInvalidCharactersMaker
from tests.fake_path_validator import (
    FakeDirectoryPathValidator,
    FakeExistingPathValidator,
    IFakeDirectoryPathValidator,
    IFakeExistingPathValidator,
)


class IFakeEntryProvider(IEntryProvider, ABC):
    @abstractmethod
    def set_directory_path_validator(
        self, validator: Optional[IFakeDirectoryPathValidator]
    ):
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


class FakeDefaultEntryProvider(IFakeEntryProvider):
    _existing_path_validator: Optional[IFakeExistingPathValidator]
    _directory_path_validator: Optional[IFakeDirectoryPathValidator]
    _path_validator: Optional[IValidator[str]]
    _entry_validator: IValidator[FileSystemEntry]
    _entry_names_provider: IEntryNameProvider
    _converter: IEntryConverter
    _invalid_characters_provider: IInvalidEntryNameCharacterProvider
    _invalid_names_provider: IInvalidEntryNameProvider
    _entry_provider: IFakeEntryProvider

    def __init__(self):
        self._setup()

        self.build()

    def build(self):
        self._entry_provider = EntryProvider(
            directory_path_validator=self._path_validator,
            entry_names_provider=self._entry_names_provider,
            converter=self._converter,
            entry_validator=self._entry_validator,
        )

    def _setup(self):
        # Path validator
        self._existing_path_validator = FakeExistingPathValidator()
        self._directory_path_validator = FakeDirectoryPathValidator()
        directory_path_validators = [
            self._existing_path_validator,
            self._directory_path_validator,
        ]
        self._path_validator = ValidatorManager[str](directory_path_validators)

        # Entry validator
        self._invalid_characters_provider = LinuxInvalidEntryNameCharacterProvider()
        existing_entry_validator = EntryAdapterForPathValidator(
            self._existing_path_validator
        )
        invalid_characters_validator = InvalidEntryNameCharactersValidator(
            self._invalid_characters_provider
        )

        self._invalid_names_provider = LinuxInvalidEntryNameProvider()
        invalid_name_validator = InvalidEntryNameValidator(self._invalid_names_provider)

        self._entry_names_provider = FakeOsListdirEntryNamesProvider()

        entry_validators = [
            invalid_name_validator,
            invalid_characters_validator,
            existing_entry_validator,
        ]
        self._entry_validator = ValidatorManager[FileSystemEntry](
            validators=entry_validators
        )

        # Converter
        separator_provider = LinuxSeparatorProvider()
        self._converter = SetEntryConverter(separator_provider)

    def set_directory_path_validator(
        self, validator: Optional[IFakeDirectoryPathValidator]
    ):
        self._directory_path_validator = validator

    def set_existing_path_validator(
        self, validator: Optional[IFakeExistingPathValidator]
    ):
        self._existing_path_validator = validator

    def set_path_validator(self, validator: Optional[IValidator[str]]):
        self._path_validator = validator

    def get(self, directory_path):
        if self._directory_path_validator:
            self._directory_path_validator.update({directory_path: True})
        return self._entry_provider.get(directory_path)


class FakeEntryProviderWithNoEntryNames(FakeDefaultEntryProvider):
    def __init__(self):
        super().__init__()

        self._entry_names_provider.set_strategy(FakeNoEntryNamesStrategy())


class FakeEntryProviderWithNotExistingDirectoryPath(FakeDefaultEntryProvider):
    def get(self, directory_path):
        if self._existing_path_validator:
            self._existing_path_validator.update({directory_path: False})
        return super().get(directory_path)


class FakeEntryProviderWithFilePath(FakeDefaultEntryProvider):
    def get(self, directory_path):
        if self._directory_path_validator:
            self._directory_path_validator.update({directory_path: False})
        return self._entry_provider.get(directory_path)


class FakeEntryProviderWithInvalidCharactersInName(FakeDefaultEntryProvider):
    def __init__(self):
        super().__init__()

        # todo: extract invalid_entry_maker to arguments
        invalid_entry_maker = FakeEntryWithInvalidCharactersMaker(
            self._invalid_characters_provider
        )

        self._entry_names_provider.set_strategy(
            FakeInvalidCharactersInName(invalid_entry_maker)
        )


class FakeEntryProviderWithReservedName(FakeDefaultEntryProvider):
    def __init__(self):
        super().__init__()

        self._entry_names_provider.set_strategy(
            FakeInvalidNamesStrategy(self._invalid_names_provider)
        )


class FakeEntryProviderWithNotExistingEntry(FakeDefaultEntryProvider):
    def get(self, directory_path):
        if self._existing_path_validator:
            entry_names = self._entry_names_provider.get(directory_path)
            entries = self._converter.convert(
                SetEntryArguments(entry_names, directory_path)
            )
            self._existing_path_validator.update({entry.path: False for entry in entries})
        return super().get(directory_path)


class FakeEntryProviderWithoutDirectories(FakeDefaultEntryProvider):
    def __init__(self):
        super().__init__()

        self._entry_names_provider.set_strategy(FakeNoDirectoriesStrategy())


class FakeEntryProviderWithoutFiles(FakeDefaultEntryProvider):
    def __init__(self):
        super().__init__()

        self._entry_names_provider.set_strategy(FakeNoFilesStrategy())
