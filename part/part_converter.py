from abc import ABC, abstractmethod

from entry.entry import Directory
from part.part import Part


class IPartConverter(ABC):
    @abstractmethod
    def convert(self, directories: set[Directory]) -> set[Part]:
        pass


class PartConverter(IPartConverter):
    def convert(self, directories: set[Directory]):
        parts = set[Part]()

        for directory in directories:
            part = Part(name=directory.name)
            parts.add(part)

        return parts
