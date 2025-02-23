from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional
from base.validator import IValidator, ValidatorManager
from entry.converter.entry_arguments import SetEntryArguments
from entry.converter.entry_converter import IEntryConverter, SetEntryConverter
from entry.entry import FileSystemEntry
from entry.entry_provider import EntryProvider
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
from entry.separator_provider import ISeparatorProvider, LinuxSeparatorProvider
from tests.fake_entry_name_provider import (
    FakeInvalidCharactersInName,
    FakeInvalidNamesStrategy,
    FakeNeutralStrategy,
    FakeNoEntryNamesStrategy,
    FakeOsListdirEntryNamesProvider,
    IFakeOsListdirEntryNamesProvider,
)
from tests.fake_entry_validator import FakeEntryWithInvalidCharactersMaker
from tests.fake_path_validator import (
    FakeNonDirectoryPathValidator,
    FakeNotExistingPathValidator,
    IFakeNonDirectoryPathValidator,
    IFakeNotExistingPathValidator,
)


@dataclass
class FakeRowEntryProviderArguments:
    not_existing_path_validator: Optional[IFakeNotExistingPathValidator] = None
    non_directory_path_validator: Optional[IFakeNonDirectoryPathValidator] = None
    invalid_names_provider: Optional[IInvalidEntryNameProvider] = None
    invalid_name_validator: Optional[IValidator] = None
    invalid_characters_provider: Optional[IInvalidEntryNameCharacterProvider] = None
    invalid_characters_validator: Optional[IValidator] = None
    not_existing_entry_validator: Optional[IValidator] = None
    entry_names_provider: Optional[IFakeOsListdirEntryNamesProvider] = None
    separator_provider: Optional[ISeparatorProvider] = None
    converter: Optional[IEntryConverter] = None


@dataclass
class FakeEntryProviderArguments:
    not_existing_path_validator: IFakeNotExistingPathValidator
    non_directory_path_validator: IFakeNonDirectoryPathValidator
    invalid_names_provider: IInvalidEntryNameProvider
    invalid_name_validator: IValidator
    invalid_characters_provider: IInvalidEntryNameCharacterProvider
    invalid_characters_validator: IValidator
    not_existing_entry_validator: IValidator
    entry_names_provider: IFakeOsListdirEntryNamesProvider
    separator_provider: ISeparatorProvider
    converter: IEntryConverter


class IFakeEntryProviderArgumentsBuilder(ABC):
    @abstractmethod
    def build(
        self, arguments: Optional[FakeRowEntryProviderArguments]
    ) -> FakeEntryProviderArguments:
        pass


class FakeEntryProviderArgumentsBuilder(IFakeEntryProviderArgumentsBuilder):
    def build(
        self, arguments: Optional[FakeRowEntryProviderArguments] = None
    ) -> FakeEntryProviderArguments:
        if arguments is None:
            arguments = FakeRowEntryProviderArguments()

        if arguments.not_existing_path_validator is None:
            arguments.not_existing_path_validator = FakeNotExistingPathValidator()

        if arguments.non_directory_path_validator is None:
            arguments.non_directory_path_validator = FakeNonDirectoryPathValidator()

        if arguments.invalid_names_provider is None:
            arguments.invalid_names_provider = LinuxInvalidEntryNameProvider()

        if arguments.invalid_name_validator is None:
            arguments.invalid_name_validator = InvalidEntryNameValidator(
                arguments.invalid_names_provider
            )

        if arguments.invalid_characters_provider is None:
            arguments.invalid_characters_provider = (
                LinuxInvalidEntryNameCharacterProvider()
            )

        if arguments.invalid_characters_validator is None:
            arguments.invalid_characters_validator = (
                InvalidEntryNameCharactersValidator(
                    arguments.invalid_characters_provider
                )
            )

        if arguments.not_existing_entry_validator is None:
            arguments.not_existing_entry_validator = EntryAdapterForPathValidator(
                arguments.not_existing_path_validator
            )

        if arguments.entry_names_provider is None:
            arguments.entry_names_provider = FakeOsListdirEntryNamesProvider()

        if arguments.separator_provider is None:
            arguments.separator_provider = LinuxSeparatorProvider()

        if arguments.converter is None:
            arguments.converter = SetEntryConverter(arguments.separator_provider)

        return FakeEntryProviderArguments(
            not_existing_path_validator=arguments.not_existing_path_validator,
            non_directory_path_validator=arguments.non_directory_path_validator,
            invalid_names_provider=arguments.invalid_names_provider,
            invalid_name_validator=arguments.invalid_name_validator,
            invalid_characters_provider=arguments.invalid_characters_provider,
            invalid_characters_validator=arguments.invalid_characters_validator,
            not_existing_entry_validator=arguments.not_existing_entry_validator,
            entry_names_provider=arguments.entry_names_provider,
            separator_provider=arguments.separator_provider,
            converter=arguments.converter,
        )


class FakeEntryProvider(EntryProvider):
    def __init__(self, arguments: FakeEntryProviderArguments):
        self.not_existing_path_validator = arguments.not_existing_path_validator
        self.non_directory_path_validator = arguments.non_directory_path_validator

        directory_path_validators = [
            arguments.not_existing_path_validator,
            arguments.non_directory_path_validator,
        ]
        directory_path_validator_manager = ValidatorManager[str](
            directory_path_validators
        )

        # Entry validator
        self.invalid_characters_provider = arguments.invalid_characters_provider

        self.invalid_names_provider = arguments.invalid_names_provider

        self.entry_names_provider = arguments.entry_names_provider

        entry_validators = [
            arguments.invalid_name_validator,
            arguments.invalid_characters_validator,
            arguments.not_existing_entry_validator,
        ]
        entry_validator_manager = ValidatorManager[FileSystemEntry](
            validators=entry_validators
        )

        # Converter
        self.converter = arguments.converter

        super().__init__(
            directory_path_validator=directory_path_validator_manager,
            entry_names_provider=arguments.entry_names_provider,
            converter=arguments.converter,
            entry_validator=entry_validator_manager,
        )


class FakeNeutralEntriesProvider(FakeEntryProvider):
    def __init__(self, arguments):
        super().__init__(arguments)

        self.entry_names_provider.set_strategy(FakeNeutralStrategy())


class FakeNoEntryNamesProvider(FakeEntryProvider):
    def __init__(self, arguments):
        super().__init__(arguments)

        self.entry_names_provider.set_strategy(FakeNoEntryNamesStrategy())


class FakeNonDirectoryPathProvider(FakeEntryProvider):
    def __init__(self, arguments):
        super().__init__(arguments)

        self.entry_names_provider.set_strategy(FakeNoEntryNamesStrategy())

    def get(self, directory_path):
        self.non_directory_path_validator.set_directories({directory_path: False})

        return super().get(directory_path)


class FakeNotExistingPathProvider(FakeEntryProvider):
    def get(self, directory_path):
        self.not_existing_path_validator.set_existing_paths({directory_path: False})
        return super().get(directory_path)


class FakeInvalidCharactersInNameProvider(FakeEntryProvider):
    def __init__(self, arguments):
        super().__init__(arguments)

        self.entry_names_provider.set_strategy(
            FakeInvalidCharactersInName(
                FakeEntryWithInvalidCharactersMaker(self.invalid_characters_provider)
            )
        )


class FakeReservedEntryNameProvider(FakeEntryProvider):
    def __init__(self, arguments):
        super().__init__(arguments)

        self.entry_names_provider.set_strategy(
            FakeInvalidNamesStrategy(self.invalid_names_provider)
        )


class FakeNotExistingEntryProvider(FakeEntryProvider):
    def get(self, directory_path):
        entry_names = self.entry_names_provider.get(directory_path)
        entries = self.converter.convert(SetEntryArguments(entry_names, directory_path))
        self.not_existing_path_validator.update_existing_paths(
            {entry.path: False for entry in entries}
        )
        return super().get(directory_path)
