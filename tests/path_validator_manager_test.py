import unittest

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


class TestPathValidatorManager(unittest.TestCase):
    def setUp(self):
        invalid_characters_provider = LinuxInvalidCharactersForPathProvider()
        validators = [
            NonePathValidator(),
            LinuxInvalidCharactersPathValidator(invalid_characters_provider),
            NotExistingPathValidator(),
            NotDirectoryValidator(),
        ]
        self.validator_manager = PathValidatorManager(validators)

    def test_validate(self):
        path = "directory/for/tests"

        self.validator_manager.validate(path)
