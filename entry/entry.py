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


class FileSystemEntry:
    def __init__(self, name: str, directory_path: str, path: str):
        self.name = name
        self.directory_path = directory_path
        self.path = path

    def __eq__(self, other):
        if isinstance(other, FileSystemEntry):
            return self.path == other.path
        return False

    def __hash__(self):
        return hash((self.path))


class Directory(FileSystemEntry):
    def __eq__(self, other):
        if isinstance(other, Directory):
            return self.path == other.path
        return False

    def __hash__(self):
        return hash((self.path))


class File(FileSystemEntry):
    def __eq__(self, other):
        if isinstance(other, File):
            return self.path == other.path
        return False

    def __hash__(self):
        return hash((self.path))
