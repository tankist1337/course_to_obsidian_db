from abc import ABC, abstractmethod


class IFilter[T, Y](ABC):
    @abstractmethod
    def filter(self, items: T) -> Y:
        pass
