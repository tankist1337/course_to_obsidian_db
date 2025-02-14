from abc import ABC, abstractmethod
from base.validator import IValidator
from entry.entry import Directory
from entry.entry_provider import IEntryProvider
from directory.directory_filter import IDirectoryFilter


class IDirectoryProvider(ABC):
    @abstractmethod
    def get(self, directory_path) -> set[Directory]:
        pass


class DirectoryProvider(IDirectoryProvider):
    def __init__(
        self,
        entry_provider: IEntryProvider,
        directory_filter: IDirectoryFilter,
        directory_path_validator: IValidator[str] | None = None,
    ):
        self.entry_provider = entry_provider
        self.directory_filter = directory_filter
        self.directory_path_validator = directory_path_validator

    def get(self, directory_path) -> set[Directory]:
        if self.directory_path_validator:
            self.directory_path_validator.validate(directory_path)

        entries = self.entry_provider.get(directory_path)

        directories = self.directory_filter.filter(entries)

        return directories
