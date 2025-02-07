from abc import ABC


class IFilter[T, Y](ABC):
    def filter(self, items: list[T]) -> list[Y]:
        pass
