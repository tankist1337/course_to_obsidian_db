from abc import ABC, abstractmethod
from dataclasses import dataclass
from base.validator import IValidator
from entry.converter.entry_arguments import (
    SetEntryArguments,
)
from entry.converter.entry_converter import IEntryConverter
from entry.entry import Directory
from entry.entry_validator import IEntryValidator
from subdirectories.directory_filter import IDirectoryFilter
from subdirectories.provider.entry_names_provider import IEntryNamesProvider


class ISubdirectoriesProvider(ABC):
    @abstractmethod
    def get(self, directory_path) -> set[Directory]:
        pass


@dataclass
class SubdirectoriesProviderArguments:
    directory_path_validator: IValidator
    directory_filter: IDirectoryFilter
    converter: IEntryConverter
    entry_names_provider: IEntryNamesProvider
    entry_validator: IEntryValidator | None = None


class SubdirectoriesProvider(ISubdirectoriesProvider):
    def __init__(
        self,
        arguments: SubdirectoriesProviderArguments,
    ):
        self.arguments = arguments

    def get(self, directory_path) -> set[Directory]:
        self.arguments.directory_path_validator.validate(directory_path)

        entry_names = self.arguments.entry_names_provider.get(directory_path)

        entries = self.arguments.converter.convert(
            SetEntryArguments(entry_names, directory_path)
        )

        if self.arguments.entry_validator:
            for entry in entries:
                self.arguments.entry_validator.validate(entry)

        directories = self.arguments.directory_filter.filter(entries)

        return directories
