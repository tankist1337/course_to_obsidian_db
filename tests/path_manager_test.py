import unittest

from base.validator import ValidatorManager
from path.path_manager import PathManager
from path.provider.path_provider import IPathProvider
from path.validator.path_validator import (
    NonePathValidator,
    NonDirectoryPathValidator,
    NotExistingPathValidator,
)


class TestPathManager(unittest.TestCase):
    def test_get_path(self):
        path_provider = FakeCliPathProvider()
        validators = [
            NonePathValidator(),
            NotExistingPathValidator(),
            NonDirectoryPathValidator(),
        ]
        path_validator_manager = ValidatorManager[str](validators)
        path_manager = PathManager(path_provider, path_validator_manager)

        path = path_manager.get()

        self.assertEqual(path, "directory/for/tests/")


class FakeCliPathProvider(IPathProvider):
    def get(self) -> str:
        return "directory/for/tests/"
