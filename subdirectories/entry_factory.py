from abc import ABC, abstractmethod

from entry.entry import Directory, FileSystemEntry


class IEntryFactory[T: FileSystemEntry](ABC):
    @abstractmethod
    def from_entry(self, entry: FileSystemEntry) -> T:
        pass


class DirectoryFactory(IEntryFactory[Directory]):
    def from_entry(self, entry: FileSystemEntry) -> Directory:
        return Directory(
            name=entry.name, directory_path=entry.directory_path, path=entry.path
        )
