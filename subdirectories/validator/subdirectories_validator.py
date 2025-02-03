from abc import ABC, abstractmethod

from base.validator import IValidator
from entry.entry import FileSystemEntry
from subdirectories.subdirectories_exception import NoSubdirectoriesException


class ISubdirectoriesValidator(IValidator[list[FileSystemEntry]], ABC):
    @abstractmethod
    def validate(self, item: list[FileSystemEntry]):
        pass


class NoSubdirectoriesValidator(ISubdirectoriesValidator):
    def validate(self, item: list[FileSystemEntry]):
        if not item:
            raise NoSubdirectoriesException(
                f'Directory "{item.path}" hasn\'t subdirectories'
            )
