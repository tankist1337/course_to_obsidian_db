from abc import ABC, abstractmethod

from base.validator import IValidator
from entry.converter.entry_arguments import SetEntryArguments
from entry.converter.entry_converter import IEntryConverter
from entry.entry import FileSystemEntry
from subdirectories.provider.entry_names_provider import IEntryNamesProvider


class IEntryProvider(ABC):
    @abstractmethod
    def get(self, directory_path: str) -> set[FileSystemEntry]:
        pass


class EntryProvider(IEntryProvider):
    def __init__(
        self,
        entry_names_provider: IEntryNamesProvider,
        converter: IEntryConverter,
        entry_validator: IValidator[FileSystemEntry] | None = None,
        directory_path_validator: IValidator[str] | None = None,
    ):
        self.directory_path_validator = directory_path_validator
        self.entry_names_provider = entry_names_provider
        self.converter = converter
        self.entry_validator = entry_validator

    def get(self, directory_path: str) -> set[FileSystemEntry]:
        if self.directory_path_validator:
            self.directory_path_validator.validate(directory_path)

        entry_names = self.entry_names_provider.get(directory_path)

        entries = self.converter.convert(SetEntryArguments(entry_names, directory_path))

        if self.entry_validator:
            for entry in entries:
                self.entry_validator.validate(entry)

        return entries
