from dataclasses import dataclass

from entry.entry import Directory


@dataclass(unsafe_hash=True)
class Part:
    directory: Directory
