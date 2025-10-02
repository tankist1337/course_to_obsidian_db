from abc import ABC
import dataclasses
from entry.entry import File


@dataclasses.dataclass(frozen=True)
class TypedFile(File, ABC):
    pass


@dataclasses.dataclass(frozen=True)
class Duration:
    seconds: int


@dataclasses.dataclass(frozen=True)
class Video(TypedFile):
    duration: Duration


@dataclasses.dataclass(frozen=True)
class Subtitles(TypedFile):
    pass


@dataclasses.dataclass(frozen=True)
class UnknownFile(TypedFile):
    pass
