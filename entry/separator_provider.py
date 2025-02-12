from abc import ABC, abstractmethod


class ISeparatorProvider(ABC):
    @abstractmethod
    def get(self) -> str:
        pass


class LinuxSeparatorProvider(ISeparatorProvider):
    def get(self) -> str:
        return "/"
