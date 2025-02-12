import unittest

from entry.entry import Directory
from subdirectories.subdirectories_exception import NoSubdirectoriesException
from subdirectories.validator.subdirectories_validator import NoSubdirectoriesValidator


class TestNoSubdirectoriesValidator(unittest.TestCase):
    def test_validate_with_subdirectories(self):
        subdirectories = {
            Directory(
                name="subdirectory1",
                directory_path="directory/for/tests",
                path="directory/for/tests/subdirectory1",
            )
        }
        validator = NoSubdirectoriesValidator()

        validator.validate(subdirectories)

    def test_validate_with_no_subdirectories(self):
        subdirectories = set[Directory]()
        validator = NoSubdirectoriesValidator()

        with self.assertRaises(NoSubdirectoriesException):
            validator.validate(subdirectories)
