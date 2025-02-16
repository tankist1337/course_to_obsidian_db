from abc import ABC, abstractmethod

from base.validator import IValidator
from entry.entry import File
from entry.entry_provider import IEntryProvider
from file.file_filter import IFileFilter


class IFileProvider(ABC):
    @abstractmethod
    def get(self, directory_path) -> set[File]:
        pass


class FileProvider(IFileProvider):
    def __init__(
        self,
        entry_provider: IEntryProvider,
        file_filter: IFileFilter,
        directory_path_validator: IValidator[str] | None = None,
    ):
        self.entry_provider = entry_provider
        self.file_filter = file_filter
        self.directory_path_validator = directory_path_validator

    def get(self, directory_path) -> set[File]:
        if self.directory_path_validator:
            self.directory_path_validator.validate(directory_path)

        entries = self.entry_provider.get(directory_path)

        files = self.file_filter.filter(entries)

        return files
