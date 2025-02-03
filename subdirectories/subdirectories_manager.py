from abc import ABC, abstractmethod
from entry.converter.entry_arguments import (
    ListEntryArguments,
)
from entry.converter.entry_converter import IEntryConverter
from entry.entry import Directory
from path.validator.path_validator import IPathValidator
from subdirectories.directory_filter import IDirectoryFilter
from subdirectories.provider.string_entry_names_provider import (
    IStringEntryNamesProvider,
)
from subdirectories.validator.subdirectories_validator import ISubdirectoriesValidator


class ISubdirectoriesProvider(ABC):
    @abstractmethod
    def get(self, directory_path) -> list[Directory]:
        pass


class SubdirectoriesManager(ISubdirectoriesProvider):
    def __init__(
        self, provider: ISubdirectoriesProvider, validator: ISubdirectoriesValidator
    ):
        self.provider = provider
        self.validator = validator

    def get(self, directory_path) -> list[Directory]:
        directories = self.provider.get(directory_path)
        self.validator.validate(directories)

        return directories


class SubdirectoriesProvider(ISubdirectoriesProvider):
    def __init__(
        self,
        directory_filter: IDirectoryFilter,
        converter: IEntryConverter,
        validator: IPathValidator,
        entry_names_provider: IStringEntryNamesProvider,
    ):
        self.directory_filter = directory_filter
        self.converter = converter
        self.validator = validator
        self.entry_names_provider = entry_names_provider

    def get(self, directory_path) -> list[Directory]:
        entry_names = self.entry_names_provider.get(directory_path)

        entries = self.converter.convert(
            ListEntryArguments(entry_names, directory_path)
        )

        for entry in entries:
            self.validator.validate(entry)

        directories = self.directory_filter.filter(entries)

        return directories
