from abc import ABC, abstractmethod

from base.validator import ValidatorManager
from part.part_converter import IPartConverter
from part.part_provider import IPartProvider, PartProvider
from path.validator.path_validator import NonePathValidator
from tests.fake_directory_provider import (
    FakeDefaultDirectoryProvider,
    IFakeDirectoryProvider,
)
from tests.fake_path_provider import FakeCliPathProvider
from tests.fake_path_validator import (
    FakeDirectoryPathValidator,
    FakeExistingPathValidator,
)


class IFakePartProvider(IPartProvider, ABC):
    @abstractmethod
    def build(self):
        pass


class FakeDefaultPartProvider(IFakePartProvider):
    _path_provider: FakeCliPathProvider
    _directory_provider: IFakeDirectoryProvider
    _converter: IPartConverter

    _part_provider: IPartProvider

    def __init__(self):
        self._setup()

        self.build()

    def build(self):
        self._part_provider = PartProvider(
            path_provider=self._path_provider,
            directory_provider=self._directory_provider,
            converter=self._converter,
        )

    def _setup(self):
        # Directory path validator
        none_path_validator = NonePathValidator()
        self.existing_path_validator = FakeExistingPathValidator()
        self.directory_path_validator = FakeDirectoryPathValidator()
        directory_path_validators = [
            none_path_validator,
            self.existing_path_validator,
            self.directory_path_validator,
        ]
        directory_path_validator_manager = ValidatorManager[str](
            directory_path_validators
        )

        # Directory path manager
        path_provider = FakeCliPathProvider(FakeGoodPathStrategy())
        path_manager = PathManager(
            provider=path_provider, validator=directory_path_validator_manager
        )

        # Directory validator
        self.entry_provider = FakeDefaultDirectoryProvider()
        self.entry_provider.set_existing_path_validator(self.existing_path_validator)

        # Directory filter
        directory_filter_validator = EntryAdapterForPathValidator(
            self.directory_path_validator
        )

        directory_factory = DirectoryFactory()
        directory_filter = DirectoryFilter(
            validator=directory_filter_validator,
            directory_factory=directory_factory,
        )

        # directory provider
        directory_provider = DirectoryProvider(
            entry_provider=self.entry_provider,
            directory_filter=directory_filter,
        )

        # Part provider
        part_converter = PartConverter()

        self.part_provider = PartProvider(
            path_provider=path_manager,
            directory_provider=directory_provider,
            converter=part_converter,
        )

    def get(self):
        return self._part_provider.get()
