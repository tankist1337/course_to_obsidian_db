from abc import ABC, abstractmethod

from part.part import Part
from part.part_converter import IPartConverter
from path.provider.path_provider import IPathManager
from subdirectories.subdirectories_provider import ISubdirectoriesProvider


class IPartsProvider(ABC):
    @abstractmethod
    def get(self) -> set[Part]:
        pass


class PartsProvider(IPartsProvider):
    def __init__(
        self,
        path_provider: IPathManager,
        subdirectories_provider: ISubdirectoriesProvider,
        converter: IPartConverter,
    ):
        self.path_provider = path_provider
        self.subdirectories_provider = subdirectories_provider
        self.converter = converter

    def get(self) -> set[Part]:
        directory_path = self.path_provider.get()
        subdirectories = self.subdirectories_provider.get(directory_path)

        parts = self.converter.convert(subdirectories)

        return parts
