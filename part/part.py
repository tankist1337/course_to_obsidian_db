from dataclasses import dataclass


@dataclass(unsafe_hash=True)
class Part:
    name: str
