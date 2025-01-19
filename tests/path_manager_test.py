import unittest

from path.path_manager import PathManager
from path.provider.path_provider import IPathProvider
from path.validator.path_validator import (
    LinuxInvalidCharactersPathValidator,
    NonePathValidator,
    NotDirectoryValidator,
    NotExistingPathValidator,
)
from path.validator.path_validator_manager import PathValidatorManager
from path.validator.invalid_characters_for_path_provider import (
    LinuxInvalidCharactersForPathProvider,
)


class TestPathManager(unittest.TestCase):
    def test_get_path(self):
        path_provider = FakeCliPathProvider()
        invalid_characters_provider = LinuxInvalidCharactersForPathProvider()
        validators = [
            NonePathValidator(),
            LinuxInvalidCharactersPathValidator(invalid_characters_provider),
            NotExistingPathValidator(),
            NotDirectoryValidator(),
        ]
        path_validator_manager = PathValidatorManager(validators)
        path_manager = PathManager(path_provider, path_validator_manager)

        path = path_manager.get_path()

        self.assertEqual(path, "directory/for/tests/")


class FakeCliPathProvider(IPathProvider):
    def get_path(self) -> str:
        return "directory/for/tests/"
