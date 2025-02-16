from abc import ABC, abstractmethod

from base.validator import IValidator
from entry.entry import File, FileSystemEntry
from entry.entry_factory import IEntryFactory
from path.validator.path_exception import NonFilePathException


class IFileFilter(ABC):
    @abstractmethod
    def filter(self, entries: set[FileSystemEntry]) -> set[File]:
        pass


class FileFilter(IFileFilter):
    def __init__(self, validator: IValidator, factory: IEntryFactory):
        self.validator = validator
        self.factory = factory

    def filter(self, entries: set[FileSystemEntry]) -> set[File]:
        files = set()

        for entry in entries:
            try:
                self.validator.validate(entry)
                files.add(self.factory.from_entry(entry))
            except NonFilePathException:
                continue

        return files
