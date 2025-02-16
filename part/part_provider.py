from abc import ABC, abstractmethod

from part.part import Part
from part.part_converter import IPartConverter
from path.provider.path_provider import IPathManager
from directory.directory_provider import IDirectoryProvider


class IPartProvider(ABC):
    @abstractmethod
    def get(self) -> set[Part]:
        pass


class PartProvider(IPartProvider):
    def __init__(
        self,
        path_provider: IPathManager,
        directory_provider: IDirectoryProvider,
        converter: IPartConverter,
    ):
        self.path_provider = path_provider
        self.directory_provider = directory_provider
        self.converter = converter

    def get(self) -> set[Part]:
        directory_path = self.path_provider.get()
        directories = self.directory_provider.get(directory_path)

        parts = self.converter.convert(directories)

        return parts
