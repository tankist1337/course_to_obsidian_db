from abc import ABC, abstractmethod
from base.validator import IValidator
from entry.entry import Directory, FileSystemEntry

from path.validator.path_exception import NonDirectoryPathException
from subdirectories.entry_factory import IEntryFactory


class IDirectoryFilter(ABC):
    @abstractmethod
    def filter(self, entries: list[FileSystemEntry]) -> list[Directory]:
        pass


class DirectoryFilter(IDirectoryFilter):
    def __init__(self, validator_manager: IValidator, directory_factory: IEntryFactory):
        self.validator_manager = validator_manager
        self.directory_factory = directory_factory

    def filter(self, entries: list[FileSystemEntry]) -> list[Directory]:
        directories = []

        for entry in set(
            entries
        ):  # remove set from there to save order and extract this logic to another class
            try:
                self.validator_manager.validate(entry)
                directories.append(self.directory_factory.from_entry(entry))
            except NonDirectoryPathException:
                continue

        return directories
