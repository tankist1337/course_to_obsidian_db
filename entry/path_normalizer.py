from abc import ABC, abstractmethod

from entry.separator_provider import ISeparatorProvider


class IPathNormalizer(ABC):
    @abstractmethod
    def ensure_trailing_separator(self, path: str) -> str:
        pass


class DirectoryPathNormalizer(IPathNormalizer):
    def __init__(self, separator_provider: ISeparatorProvider):
        self.separator = separator_provider.get()

    def _has_not_trailing_separator(self, path) -> bool:
        return not path.endswith(self.separator)

    def ensure_trailing_separator(self, path) -> str:
        if self._has_not_trailing_separator(path):
            path += self.separator
        return path
