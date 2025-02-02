import unittest

from path.validator.path_validator import (
    NonePathValidator,
    NonDirectoryPathValidator,
    NotExistingPathValidator,
)
from path.validator.path_validator_manager import PathValidatorManager


class TestPathValidatorManager(unittest.TestCase):
    def setUp(self):
        validators = [
            NonePathValidator(),
            NotExistingPathValidator(),
            NonDirectoryPathValidator(),
        ]
        self.validator_manager = PathValidatorManager(validators)

    def test_validate(self):
        path = "directory/for/tests"

        self.validator_manager.validate(path)
