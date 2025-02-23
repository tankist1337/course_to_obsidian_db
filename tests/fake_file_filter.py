from abc import ABC, abstractmethod
from dataclasses import dataclass
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
    IInvalidEntryNameCharacterProvider,
    LinuxInvalidEntryNameCharacterProvider,
)
from entry.invalid_entry_names_provider import (
    IInvalidEntryNameProvider,
    LinuxInvalidEntryNameProvider,
)
from file.file_filter import FileFilter
from tests.fake_path_validator import (
    FakeNonFilePathValidator,
    FakeNotExistingPathValidator,
    IFakeNonFilePathValidator,
    IFakeNotExistingPathValidator,
)


@dataclass
class FakeRowFileFilterArguments:
    not_existing_path_validator: Optional[IFakeNotExistingPathValidator] = None
    non_file_path_validator: Optional[IFakeNonFilePathValidator] = None
    invalid_names_provider: Optional[IInvalidEntryNameProvider] = None
    invalid_name_validator: Optional[IValidator] = None
    invalid_characters_provider: Optional[IInvalidEntryNameCharacterProvider] = None
    invalid_characters_validator: Optional[IValidator] = None
    not_existing_entry_validator: Optional[IValidator] = None
    non_file_entry_validator: Optional[IValidator] = None
    factory: Optional[IEntryFactory] = None


@dataclass
class FakeFileFilterArguments:
    not_existing_path_validator: IFakeNotExistingPathValidator
    non_file_path_validator: IFakeNonFilePathValidator
    invalid_names_provider: IInvalidEntryNameProvider
    invalid_name_validator: IValidator
    invalid_characters_provider: IInvalidEntryNameCharacterProvider
    invalid_characters_validator: IValidator
    not_existing_entry_validator: IValidator
    non_file_entry_validator: IValidator
    factory: IEntryFactory


class IFakeFileFilterArgumentsBuilder(ABC):
    @abstractmethod
    def build(
        self, arguments: Optional[FakeRowFileFilterArguments]
    ) -> FakeFileFilterArguments:
        pass


class FakeFileFilterArgumentsBuilder(IFakeFileFilterArgumentsBuilder):
    def build(
        self, arguments: Optional[FakeRowFileFilterArguments] = None
    ) -> FakeFileFilterArguments:
        if arguments is None:
            arguments = FakeRowFileFilterArguments()

        if arguments.not_existing_path_validator is None:
            arguments.not_existing_path_validator = FakeNotExistingPathValidator()

        if arguments.non_file_path_validator is None:
            arguments.non_file_path_validator = FakeNonFilePathValidator()

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

        if arguments.non_file_entry_validator is None:
            arguments.non_file_entry_validator = EntryAdapterForPathValidator(
                arguments.non_file_path_validator
            )

        if arguments.factory is None:
            arguments.factory = FileFactory()

        return FakeFileFilterArguments(
            not_existing_path_validator=arguments.not_existing_path_validator,
            non_file_path_validator=arguments.non_file_path_validator,
            invalid_names_provider=arguments.invalid_names_provider,
            invalid_name_validator=arguments.invalid_name_validator,
            invalid_characters_provider=arguments.invalid_characters_provider,
            invalid_characters_validator=arguments.invalid_characters_validator,
            not_existing_entry_validator=arguments.not_existing_entry_validator,
            non_file_entry_validator=arguments.non_file_entry_validator,
            factory=arguments.factory,
        )


class   FakeFileFilter(FileFilter):
    def __init__(self, arguments: FakeFileFilterArguments):
        self.not_existing_path_validator = arguments.not_existing_path_validator
        self.non_file_path_validator = arguments.non_file_path_validator
        self.invalid_names_provider = arguments.invalid_names_provider
        self.invalid_characters_provider = arguments.invalid_characters_provider

        filter_validators = [
            arguments.invalid_name_validator,
            arguments.invalid_characters_validator,
            arguments.not_existing_entry_validator,
            arguments.non_file_entry_validator,
        ]

        validator = ValidatorManager[FileSystemEntry](validators=filter_validators)

        factory = arguments.factory

        super().__init__(validator, factory)


class FakeNeutralFileFilter(FakeFileFilter):
    def filter(self, entries):
        self.non_file_path_validator.update_files(
            {entry.path: "file" in entry.name for entry in entries}
        )
        return super().filter(entries)


class FakeNotExistingEntryFileFilter(FakeFileFilter):
    def filter(self, entries):
        self.not_existing_path_validator.update_existing_paths(
            {entry.path: False for entry in entries}
        )
        return super().filter(entries)
