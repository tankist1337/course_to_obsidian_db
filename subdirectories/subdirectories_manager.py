from abc import ABC, abstractmethod
from entry.converter.entry_arguments import (
    ListEntryArguments,
)
from entry.converter.entry_converter import IEntryConverter
from entry.entry import Directory
from entry.entry_validator import IEntryValidator
from path.validator.path_validator import IPathValidator
from subdirectories.directory_filter import IDirectoryFilter
from subdirectories.provider.entry_names_provider import IEntryNamesProvider
from subdirectories.unique_item_filter import IUniqueItemFilter
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
        directory_path_validator: IPathValidator,
        unique_item_filter: IUniqueItemFilter,
        directory_filter: IDirectoryFilter,
        converter: IEntryConverter,
        entry_validator: IEntryValidator,
        entry_names_provider: IEntryNamesProvider,
    ):
        self.directory_path_validator = directory_path_validator
        self.unique_item_filter = unique_item_filter
        self.directory_filter = directory_filter
        self.converter = converter
        self.entry_validator = entry_validator
        self.entry_names_provider = entry_names_provider

    def get(self, directory_path) -> list[Directory]:
        self.directory_path_validator.validate(directory_path)

        entry_names = self.entry_names_provider.get(directory_path)
        unique_names = self.unique_item_filter.filter(entry_names)

        entries = self.converter.convert(
            ListEntryArguments(unique_names, directory_path)
        )

        for entry in entries:
            self.entry_validator.validate(entry)

        directories = self.directory_filter.filter(entries)

        return directories
