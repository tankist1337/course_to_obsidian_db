from abc import ABC, abstractmethod


class IInvalidEntryNameCharacterProvider(ABC):
    @abstractmethod
    def get(self) -> set[str]:
        pass


class LinuxInvalidEntryNameCharacterProvider(IInvalidEntryNameCharacterProvider):
    def get(self) -> set[str]:
        return {"/"}
