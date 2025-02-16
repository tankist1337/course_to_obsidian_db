from base.validator import IValidator


class FakeException(Exception):
    pass


class FakeValidator(IValidator):
    is_passed = False

    def __init__(self, is_valid: bool):
        self.validation = is_valid

    def validate(self, item):
        if not self.validation:
            raise FakeException("Fake exception")

        self.is_passed = True
