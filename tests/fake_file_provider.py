from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional
from base.validator import IValidator, StubValidator, ValidatorManager
from entry.converter.entry_arguments import SetEntryArguments
from entry.converter.entry_converter import IEntryConverter, SetEntryConverter
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
from entry.separator_provider import ISeparatorProvider, LinuxSeparatorProvider
from file.file_provider import FileProvider
from path.validator.path_validator import IPathValidator, NonePathValidator
from tests.fake_entry_name_provider import (
    FakeNeutralStrategy,
    FakeNoFilesStrategy,
    FakeOsListdirEntryNamesProvider,
    IFakeOsListdirEntryNamesProvider,
)
from tests.fake_entry_provider import (
    FakeEntryProvider,
    FakeEntryProviderArgumentsBuilder,
    FakeRowEntryProviderArguments,
)
from tests.fake_file_filter import (
    FakeFileFilter,
    FakeFileFilterArgumentsBuilder,
    FakeRowFileFilterArguments,
)
from tests.fake_path_validator import (
    FakeNonDirectoryPathValidator,
    FakeNonFilePathValidator,
    FakeNotExistingPathValidator,
    FakeStubNonDirectoryPathValidator,
    FakeStubNotExistingPathValidator,
    IFakeNonDirectoryPathValidator,
    IFakeNonFilePathValidator,
    IFakeNotExistingPathValidator,
)


@dataclass
class FakeRowFileProviderArguments:
    none_path_validator: Optional[IPathValidator] = None
    not_existing_path_validator: Optional[IFakeNotExistingPathValidator] = None
    non_directory_path_validator: Optional[IFakeNonDirectoryPathValidator] = None
    invalid_names_provider: Optional[IInvalidEntryNameProvider] = None
    invalid_name_validator: Optional[IValidator] = None
    invalid_characters_provider: Optional[IInvalidEntryNameCharacterProvider] = None
    invalid_characters_validator: Optional[IValidator] = None
    not_existing_entry_validator: Optional[IValidator] = None
    entry_names_provider: Optional[IFakeOsListdirEntryNamesProvider] = None
    separator_provider: Optional[ISeparatorProvider] = None
    entry_converter: Optional[IEntryConverter] = None
    file_factory: Optional[IEntryFactory] = None
    non_file_path_validator: Optional[IFakeNonFilePathValidator] = None
    non_file_entry_validator: Optional[IValidator] = None


@dataclass
class FakeFileProviderArguments:
    none_path_validator: IPathValidator
    not_existing_path_validator: IFakeNotExistingPathValidator
    non_directory_path_validator: IFakeNonDirectoryPathValidator
    invalid_names_provider: IInvalidEntryNameProvider
    invalid_name_validator: IValidator
    invalid_characters_provider: IInvalidEntryNameCharacterProvider
    invalid_characters_validator: IValidator
    not_existing_entry_validator: IValidator
    entry_names_provider: IFakeOsListdirEntryNamesProvider
    separator_provider: ISeparatorProvider
    entry_converter: IEntryConverter
    file_factory: IEntryFactory
    non_file_path_validator: IFakeNonFilePathValidator
    non_file_entry_validator: IValidator


class IFakeFileProviderArgumentsBuilder(ABC):
    @abstractmethod
    def build(
        self, arguments: Optional[FakeRowFileProviderArguments]
    ) -> FakeFileProviderArguments:
        pass


class FakeFileProviderArgumentsBuilder(IFakeFileProviderArgumentsBuilder):
    def build(
        self, arguments: Optional[FakeRowFileProviderArguments] = None
    ) -> FakeFileProviderArguments:
        if arguments is None:
            arguments = FakeRowFileProviderArguments()

        if arguments.none_path_validator is None:
            arguments.none_path_validator = NonePathValidator()

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

        if arguments.entry_converter is None:
            arguments.entry_converter = SetEntryConverter(arguments.separator_provider)

        if arguments.not_existing_entry_validator is None:
            arguments.not_existing_entry_validator = EntryAdapterForPathValidator(
                arguments.not_existing_path_validator
            )

        if arguments.non_file_path_validator is None:
            arguments.non_file_path_validator = FakeNonFilePathValidator()

        if arguments.non_file_entry_validator is None:
            arguments.non_file_entry_validator = EntryAdapterForPathValidator(
                arguments.non_file_path_validator
            )

        if arguments.file_factory is None:
            arguments.file_factory = FileFactory()

        return FakeFileProviderArguments(
            none_path_validator=arguments.none_path_validator,
            not_existing_path_validator=arguments.not_existing_path_validator,
            non_directory_path_validator=arguments.non_directory_path_validator,
            invalid_names_provider=arguments.invalid_names_provider,
            invalid_name_validator=arguments.invalid_name_validator,
            invalid_characters_provider=arguments.invalid_characters_provider,
            invalid_characters_validator=arguments.invalid_characters_validator,
            not_existing_entry_validator=arguments.not_existing_entry_validator,
            entry_names_provider=arguments.entry_names_provider,
            separator_provider=arguments.separator_provider,
            entry_converter=arguments.entry_converter,
            file_factory=arguments.file_factory,
            non_file_path_validator=arguments.non_file_path_validator,
            non_file_entry_validator=arguments.non_file_entry_validator,
        )


class FakeFileProvider(FileProvider):
    def __init__(self, arguments: FakeFileProviderArguments):
        self.not_existing_path_validator = arguments.not_existing_path_validator
        self.non_directory_path_validator = arguments.non_directory_path_validator
        self.entry_converter = arguments.entry_converter

        directory_path_validator = ValidatorManager[str](
            validators=[
                self.not_existing_path_validator,
                self.non_directory_path_validator,
            ]
        )

        stub_validator = StubValidator()
        stub_not_existing_path_validator = FakeStubNotExistingPathValidator()
        stub_non_directory_path_validator = FakeStubNonDirectoryPathValidator()

        file_filter_arguments = FakeFileFilterArgumentsBuilder().build(
            FakeRowFileFilterArguments(
                not_existing_path_validator=stub_not_existing_path_validator,
                invalid_name_validator=stub_validator,
                invalid_characters_validator=stub_validator,
            )
        )

        entry_provider_arguments = FakeEntryProviderArgumentsBuilder().build(
            FakeRowEntryProviderArguments(
                not_existing_path_validator=stub_not_existing_path_validator,
                non_directory_path_validator=stub_non_directory_path_validator,
            )
        )

        self.entry_provider = FakeEntryProvider(entry_provider_arguments)

        self.file_filter = FakeFileFilter(file_filter_arguments)

        super().__init__(
            entry_provider=self.entry_provider,
            file_filter=self.file_filter,
            directory_path_validator=directory_path_validator,
        )


class FakeNeutralFileProvider(FakeFileProvider):
    def __init__(self, arguments):
        super().__init__(arguments)

        self.entry_provider.entry_names_provider.set_strategy(FakeNeutralStrategy())

    def get(self, directory_path):
        self.non_directory_path_validator.set_directories({directory_path: True})
        entry_names = self.entry_provider.entry_names_provider.get(directory_path)
        entries = self.entry_converter.convert(
            SetEntryArguments(entry_names, directory_path)
        )
        self.file_filter.non_file_path_validator.update_files(
            {
                entry.path: ("all_good.txt" in entry.name) or ("file" in entry.name)
                for entry in entries
            }
        )

        return super().get(directory_path)


class FakeNoFilesFileProvider(FakeFileProvider):
    def __init__(self, arguments):
        super().__init__(arguments)

        self.entry_provider.entry_names_provider.set_strategy(FakeNoFilesStrategy())

    def get(self, directory_path):
        self.non_directory_path_validator.set_directories({directory_path: True})
        entry_names = self.entry_provider.entry_names_provider.get(directory_path)
        entries = self.entry_converter.convert(
            SetEntryArguments(entry_names, directory_path)
        )
        self.file_filter.non_file_path_validator.update_files(
            {
                entry.path: ("all_good.txt" in entry.name) or ("file" in entry.name)
                for entry in entries
            }
        )
        return super().get(directory_path)


class FakeNotExistingPathFileProvider(FakeFileProvider):
    def get(self, directory_path):
        self.not_existing_path_validator.update_existing_paths({directory_path: False})
        return super().get(directory_path)


class FakeNonDirectoryPathFileProvider(FakeFileProvider):
    def get(self, directory_path):
        self.non_directory_path_validator.update_directories({directory_path: False})
        return super().get(directory_path)
