from abc import ABC, abstractmethod


class IInvalidEntryNameCharactersProvider(ABC):
    @abstractmethod
    def get(self) -> set[str]:
        pass


class LinuxInvalidEntryNameCharactersProvider(IInvalidEntryNameCharactersProvider):
    def get(self) -> set[str]:
        return {"/"}
