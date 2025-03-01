from abc import ABC, abstractmethod
from entry.entry import FileSystemEntry
from entry.invalid_entry_name_character_provider import (
    IInvalidEntryNameCharacterProvider,
)


class IEntryWithInvalidCharactersMaker(ABC):
    @abstractmethod
    def get(self, directory_path: str) -> set[FileSystemEntry]:
        pass


class FakeEntryWithInvalidCharactersMaker(IEntryWithInvalidCharactersMaker):
    def __init__(
        self,
        invalid_characters_provider: IInvalidEntryNameCharacterProvider,
    ):
        self.invalid_characters_provider = invalid_characters_provider

    def get(self, directory_path="directory/for/tests/"):
        invalid_characters = self.invalid_characters_provider.get()
        invalid_entries = set()

        for character in invalid_characters:
            name = "name_with_invalid_characters"

            invalid_name = f"{character}{name}"
            invalid_entry = FileSystemEntry(
                name=invalid_name,
                directory_path=directory_path,
                path=directory_path + invalid_name,
            )
            invalid_entries.add(invalid_entry)

            invalid_name = self.__put_character_in_center(name, character)
            invalid_entry = FileSystemEntry(
                name=invalid_name,
                directory_path=directory_path,
                path=directory_path + invalid_name,
            )
            invalid_entries.add(invalid_entry)

            invalid_name = f"{name}{character}"
            invalid_entry = FileSystemEntry(
                name=invalid_name,
                directory_path=directory_path,
                path=directory_path + invalid_name,
            )
            invalid_entries.add(invalid_entry)

        return invalid_entries

    def __put_character_in_center(self, name, character):
        center_index = int(len(name) / 2)
        return name[:center_index] + character + name[center_index:]
