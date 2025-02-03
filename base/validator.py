from abc import ABC, abstractmethod


class IValidator[T](ABC):
    @abstractmethod
    def validate(self, item: T):
        pass


class ValidatorManager[T](IValidator[T], ABC):
    def __init__(self, validators: list[IValidator]):
        self.validators = validators

    def validate(self, item: T):
        for validator in self.validators:
            validator.validate(item)
