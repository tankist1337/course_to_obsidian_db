from abc import ABC, abstractmethod

from entry.converter.entry_arguments import (
    ArgumentsToConvertToEntry,
    SetEntryArguments,
    SingleEntryArguments,
)
from entry.entry import FileSystemEntry
from entry.path_normalizer import IPathNormalizer


class IEntryConverter[T: ArgumentsToConvertToEntry, Y](ABC):
    @abstractmethod
    def convert(self, arguments: T) -> Y:
        pass


class SingleEntryConverter(IEntryConverter[SingleEntryArguments, FileSystemEntry]):
    def __init__(self, path_normalizer: IPathNormalizer):
        self.path_normalizer = path_normalizer

    def convert(self, arguments: SingleEntryArguments) -> FileSystemEntry:
        directory_path = self.path_normalizer.ensure_trailing_separator(
            arguments.directory_path
        )
        path = directory_path + arguments.name

        return FileSystemEntry(
            name=arguments.name,
            directory_path=directory_path,
            path=path,
        )


class SetEntryConverter(IEntryConverter[SetEntryArguments, set[FileSystemEntry]]):
    def __init__(self, path_normalizer: IPathNormalizer):
        self.path_normalizer = path_normalizer

    def convert(self, arguments: SetEntryArguments) -> set[FileSystemEntry]:
        directory_path = self.path_normalizer.ensure_trailing_separator(
            arguments.directory_path
        )

        entries = set()
        for name in arguments.names:
            path = directory_path + name
            entry = FileSystemEntry(name=name, directory_path=directory_path, path=path)
            entries.add(entry)

        return entries
