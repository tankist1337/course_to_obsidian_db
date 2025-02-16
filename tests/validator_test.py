import unittest

from base.validator import ValidatorManager
from tests.fake_validator import FakeException, FakeValidator


class TestValidatorManager(unittest.TestCase):
    def test_validate(self):
        validators = [
            FakeValidator(True),
            FakeValidator(True),
            FakeValidator(True),
            FakeValidator(True),
            FakeValidator(True),
        ]
        manager = ValidatorManager(validators)

        manager.validate("_")

        for validator in validators:
            self.assertEqual(validator.is_passed, True)

    def test_validate_with_fail_at_the_start(self):
        validators = [
            FakeValidator(False),
            FakeValidator(True),
            FakeValidator(True),
            FakeValidator(True),
            FakeValidator(True),
        ]
        manager = ValidatorManager(validators)

        with self.assertRaises(FakeException):
            manager.validate("_")

        for validator in validators:
            self.assertEqual(validator.is_passed, False)

    def test_validate_with_fail_at_the_middle(self):
        validators = [
            FakeValidator(True),
            FakeValidator(True),
            FakeValidator(False),
            FakeValidator(True),
            FakeValidator(True),
        ]
        manager = ValidatorManager(validators)

        with self.assertRaises(FakeException):
            manager.validate("_")

        self.assertEqual(validators[0].is_passed, True)
        self.assertEqual(validators[1].is_passed, True)
        self.assertEqual(validators[2].is_passed, False)
        self.assertEqual(validators[3].is_passed, False)
        self.assertEqual(validators[4].is_passed, False)

    def test_validate_with_fail_at_the_end(self):
        validators = [
            FakeValidator(True),
            FakeValidator(True),
            FakeValidator(True),
            FakeValidator(True),
            FakeValidator(False),
        ]
        manager = ValidatorManager(validators)

        with self.assertRaises(FakeException):
            manager.validate("_")

        self.assertEqual(validators[0].is_passed, True)
        self.assertEqual(validators[1].is_passed, True)
        self.assertEqual(validators[2].is_passed, True)
        self.assertEqual(validators[3].is_passed, True)
        self.assertEqual(validators[4].is_passed, False)

    def test_validate_without_validators(self):
        validators = []
        manager = ValidatorManager(validators)

        manager.validate("_")

        passed_validators_number = sum(validator.is_passed for validator in validators)
        self.assertEqual(passed_validators_number, 0)
