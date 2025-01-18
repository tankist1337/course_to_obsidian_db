from abc import ABC, abstractmethod


class InvalidCharactersForPathProvider(ABC):
    @abstractmethod
    def get_characters():
        pass


class LinuxInvalidCharactersForPathProvider(InvalidCharactersForPathProvider):
    characters = ["//"]

    def get_characters(self):
        return self.characters
