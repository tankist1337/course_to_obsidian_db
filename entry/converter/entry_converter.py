from abc import ABC, abstractmethod

from entry.converter.entry_arguments import (
    ArgumentsToConvertToEntry,
    SingleEntryArguments,
    ListEntryArguments,
)
from entry.entry import FileSystemEntry
from entry.separator_provider import ISeparatorProvider


class IEntryConverter[T](ABC):
    @abstractmethod
    def convert(self, arguments: ArgumentsToConvertToEntry) -> T:
        pass


class SingleEntryConverter(IEntryConverter[FileSystemEntry]):
    def __init__(self, separator_provider: ISeparatorProvider):
        self.separator_provider = separator_provider

    def convert(self, arguments: SingleEntryArguments) -> FileSystemEntry:
        is_path_not_closed_by_separator = not arguments.directory_path.endswith(
            self.separator_provider.get()
        )

        path = arguments.directory_path
        if is_path_not_closed_by_separator:
            path += self.separator_provider.get()
        path += arguments.name

        return FileSystemEntry(
            name=arguments.name,
            directory_path=arguments.directory_path,
            path=path,
        )


class ListEntryConverter(IEntryConverter[list[FileSystemEntry]]):
    def __init__(self, separator_provider: ISeparatorProvider):
        self.separator_provider = separator_provider

    def convert(self, arguments: ListEntryArguments) -> list[FileSystemEntry]:
        is_path_not_closed_by_separator = not arguments.directory_path.endswith(
            self.separator_provider.get()
        )

        entries = []

        for name in arguments.names:
            path = arguments.directory_path
            if is_path_not_closed_by_separator:
                path += self.separator_provider.get()
            path += name

            entry = FileSystemEntry(
                name=name, directory_path=arguments.directory_path, path=path
            )

            entries.append(entry)

        return entries
