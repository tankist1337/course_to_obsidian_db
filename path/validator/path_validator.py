from abc import ABC, abstractmethod
import os

from base.validator import IValidator
from path.validator.path_exception import (
    NonePathException,
    NonDirectoryPathException,
    NotExistingPathException,
)


class IPathValidator(IValidator[str], ABC):
    @abstractmethod
    def validate(self, item: str):
        pass


class NonePathValidator(IPathValidator):
    def validate(self, item):
        if item is None:
            raise NonePathException("The path must be not None")


# todo: Review this class os.path.isdir
class NonDirectoryPathValidator(IPathValidator):
    def validate(self, item):
        if not os.path.isdir(item):
            raise NonDirectoryPathException(f"The path {item} is not a directory")


# todo: Review this class os.path.exists
class NotExistingPathValidator(IPathValidator):
    def validate(self, item):
        if not os.path.exists(item):
            raise NotExistingPathException(f"The path {item} doesn't exist")
