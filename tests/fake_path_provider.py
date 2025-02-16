from abc import ABC, abstractmethod
from path.provider.path_provider import IPathProvider


class FakeCliPathStrategy(IPathProvider, ABC):
    @abstractmethod
    def get(self) -> str | None:
        pass


class FakeGoodPathStrategy(FakeCliPathStrategy):
    def get(self):
        return "directory/for/tests/"


class FakeNoneStrategy(FakeCliPathStrategy):
    def get(self):
        return None


class FakeCliPathProvider(IPathProvider):
    def __init__(self, strategy: FakeCliPathStrategy | None = None):
        self.strategy = strategy

    def set_strategy(self, strategy):
        self.strategy = strategy

    def get(self):
        return self.strategy.get() if self.strategy else None
