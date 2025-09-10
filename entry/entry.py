"""
There are naming convention for file system entries.

FileSystemEntry can be as files (.mp4, .jpeg, .txt) or directories (/home, /etc, /user)

/home/user/projects/project1/main.py
                            ________ file (entry) name

/home/user/projects/project1/
                   __________ directory (entry) name

/home/user/projects/project1/main.py
____________________________         directory path

/home/user/projects/project1/main.py
____________________________________ path

/home/user/projects/project1/lib/main.py
                            ____________ relative path

/home/user/projects/project1/lib/main.py
________________________________________ absolute path

/home/user/projects/project1/lib/main.py
                                     ___ extension name

/home/user/projects/project1/lib/main.py
_                                           root path (/ , C:\\)

separator (/, \\):

/home/user/projects/project1/lib/main.py - for linux
_    _    _        _        _   _

C:\\home\\user\\projects\\project1\\lib\\main.py - for windows
  __    __    __        __        __   __
"""

import dataclasses


@dataclasses.dataclass(frozen=True)
class FileSystemEntry:
    name: str
    directory_path: str
    path: str


@dataclasses.dataclass(frozen=True)
class Directory(FileSystemEntry):
    pass


@dataclasses.dataclass(frozen=True)
class File(FileSystemEntry):
    pass
