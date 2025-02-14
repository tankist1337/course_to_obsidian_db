from abc import ABC, abstractmethod
from base.validator import IValidator


from entry.entry import FileSystemEntry
from entry.entry_exception import (
    InvalidEntryNameCharacterException,
    InvalidEntryNameException,
)
from entry.invalid_entry_name_character_provider import (
    IInvalidEntryNameCharacterProvider,
)
from entry.invalid_entry_names_provider import IInvalidEntryNameProvider
from path.validator.path_validator import IPathValidator


class IEntryValidator(IValidator[FileSystemEntry], ABC):
    @abstractmethod
    def validate(self, item: FileSystemEntry):
        pass


class InvalidEntryNameValidator(IEntryValidator):
    def __init__(self, invalid_names_provider: IInvalidEntryNameProvider):
        self.invalid_names_provider = invalid_names_provider

    def validate(self, item: FileSystemEntry):
        for invalid_name in self.invalid_names_provider.get():
            if item.name == invalid_name:
                raise InvalidEntryNameException(
                    f'The name "{item.name}" isn\'t valid for the file system entry'
                )


class InvalidEntryNameCharactersValidator(IEntryValidator):
    def __init__(self, invalid_characters_provider: IInvalidEntryNameCharacterProvider):
        self.invalid_characters_provider = invalid_characters_provider

    def validate(self, item: FileSystemEntry):
        for invalid_character in self.invalid_characters_provider.get():
            if invalid_character in item.name:
                raise InvalidEntryNameCharacterException(
                    f'The entry name "{item.name}" has invalid character: "{invalid_character}"'
                )


class EntryAdapterForPathValidator(IEntryValidator):
    def __init__(self, path_validator: IPathValidator):
        self.path_validator = path_validator

    def validate(self, item: FileSystemEntry):
        return self.path_validator.validate(item.path)
