from abc import ABC, abstractmethod

from base.validator import IValidator
from entry.entry import Directory
from subdirectories.subdirectories_exception import NoSubdirectoriesException


class ISubdirectoriesValidator(IValidator[set[Directory]], ABC):
    @abstractmethod
    def validate(self, item: set[Directory]):
        pass


class NoSubdirectoriesValidator(ISubdirectoriesValidator):
    def validate(self, item: set[Directory]):
        if not item:
            raise NoSubdirectoriesException("There are no subdirectories")
