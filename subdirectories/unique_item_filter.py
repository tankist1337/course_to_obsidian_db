from abc import ABC

from base.filter import IFilter


class IUniqueItemFilter[T](IFilter[T, T], ABC):
    def filter(self, items: list[T]) -> list[T]:
        pass


class StringUniqueItemFilter(IUniqueItemFilter[str]):
    def filter(self, items: list[str]) -> list[str]:
        seen = set()
        seen_add = seen.add
        return [item for item in items if not (item in seen or seen_add(item))]
