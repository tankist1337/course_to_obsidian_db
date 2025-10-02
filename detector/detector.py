from abc import ABC, abstractmethod
from typing import Iterable, Optional, Sequence

from detector.detector_exception import (
    NoAnyDetectorException,
    NoFallbackDetectorException,
)
from entry.entry import File
from entry.typed_file import TypedFile, UnknownFile


class IDetector(ABC):
    @abstractmethod
    def detect(self, file: File) -> Optional[TypedFile]:
        pass


class IBatchDetector(ABC):
    @abstractmethod
    def detect_all(self, files: Iterable[File]) -> Iterable[Optional[TypedFile]]:
        pass


class IStrictDetector(IDetector):
    @abstractmethod
    def detect(self, file: File) -> TypedFile:
        pass


class IStrictBatchDetector(IBatchDetector):
    @abstractmethod
    def detect_all(self, files: Iterable[File]) -> Iterable[TypedFile]:
        pass


class DetectorChain(IStrictDetector, IStrictBatchDetector):
    def __init__(self, detectors: Sequence[IDetector]):
        self.detectors = detectors

    def detect(self, file: File) -> TypedFile:
        if not self.detectors:
            raise NoAnyDetectorException()

        for detector in self.detectors:
            typed_file = detector.detect(file)
            if typed_file is not None:
                return typed_file

        raise NoFallbackDetectorException()

    def detect_all(self, files: Iterable[File]) -> Iterable[TypedFile]:
        return [self.detect(file) for file in files]


class FallbackDetector(IStrictDetector):
    def detect(self, file: File) -> TypedFile:
        return UnknownFile(file.name, file.directory_path, file.path)
