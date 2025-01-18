from abc import ABC, abstractmethod

from path.validator.path_validator import IPathValidator


class IPathValidatorManager(ABC):
    @abstractmethod
    def validate(path):
        pass


class PathValidatorManager(IPathValidatorManager):
    def __init__(self, validators: list[IPathValidator]):
        self.validators = validators

    def validate(self, path):
        for validator in self.validators:
            validator.validate(path)
