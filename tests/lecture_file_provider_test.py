from entry.entry import File
from entry.entry_factory import FileFactory
from entry.entry_validator import (
    EntryAdapterForPathValidator,
)
from file.file_filter import FileFilter
from file.file_provider import FileProvider
from tests.fake_entry_name_provider import (
    FakeCustomEntryNamesStrategy,
)
from tests.fake_path_validator import (
    FakeNonFilePathValidator,
)


class TestLectureFileProvider(unittest.TestCase):
    def setUp(self):
        file_provider = FakeFileProvider()

        self.lecture_file_provider = LectureFileProvider(file_provider=file_provider)

    def test_get(self):
        lecture_files = self.lecture_file_provider.get()

        expected_files = {
            LectureFileMp4(
                file=File(
                    "video1.mp4",
                    "directory/for/tests/",
                    "directory/for/tests/video1.mp4",
                )
            )
        }
        self.assertEqual(lecture_files, expected_files)
