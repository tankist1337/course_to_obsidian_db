from abc import ABC, abstractmethod
import os

from path.validator.path_exception import (
    InvalidCharactersPathException,
    NonePathException,
    NotDirectoryException,
    NotExistingPathException,
)
from path.validator.invalid_characters_for_path_provider import (
    InvalidCharactersForPathProvider,
)


class IPathValidator(ABC):
    @abstractmethod
    def validate(path):
        pass


class LinuxInvalidCharactersPathValidator(IPathValidator):
    def __init__(self, invalid_characters_provider: InvalidCharactersForPathProvider):
        self.invalid_characters_provider = invalid_characters_provider

    def validate(self, path):
        invalid_characters = self.invalid_characters_provider.get_characters()

        for character in invalid_characters:
            if character in path:
                raise InvalidCharactersPathException(
                    f"The directory path has incorrect character: {character}"
                )


class NonePathValidator(IPathValidator):
    def validate(self, path):
        if path is None:
            raise NonePathException("The directory path is None")


# todo: Review this class os.path.isdir
class NotDirectoryValidator(IPathValidator):
    def validate(self, path):
        if not os.path.isdir(path):
            raise NotDirectoryException("The directory path is not a directory")


# todo: Review this class os.path.exists
class NotExistingPathValidator(IPathValidator):
    def validate(self, path):
        if not os.path.exists(path):
            raise NotExistingPathException("The directory path does not exist")
