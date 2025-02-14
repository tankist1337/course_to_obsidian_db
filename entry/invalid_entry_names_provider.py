from abc import ABC, abstractmethod


class IInvalidEntryNameProvider(ABC):
    @abstractmethod
    def get(self) -> set[str]:
        pass


class LinuxInvalidEntryNameProvider(IInvalidEntryNameProvider):
    def get(self) -> set[str]:
        return {".", "..", ""}
