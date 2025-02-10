from abc import ABC, abstractmethod

from base.filter import IFilter


class IUniqueItemFilter[T](IFilter[T, T], ABC):
    @abstractmethod
    def filter(self, items: T) -> T:
        pass


class StringUniqueItemFilter(IUniqueItemFilter[list[str]]):
    def filter(self, items: list[str]) -> list[str]:
        seen = set()
        seen_add = seen.add
        return [item for item in items if not (item in seen or seen_add(item))]
