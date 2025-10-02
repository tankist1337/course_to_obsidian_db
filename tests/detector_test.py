import unittest
from unittest.mock import MagicMock

from detector.detector import (
    DetectorChain,
    FallbackDetector,
    IDetector,
)
from detector.detector_exception import (
    NoAnyDetectorException,
    NoFallbackDetectorException,
)
from entry.entry import File
from entry.typed_file import UnknownFile, TypedFile


def wrap_file_as_unknown(file: File) -> TypedFile:
    return UnknownFile(file.name, file.directory_path, file.path)


class TestDetectorChain(unittest.TestCase):
    def setUp(self):
        self.file1 = File(
            "logo.jpeg", "/directory/for/tests/", "/directory/for/tests/logo.jpeg"
        )
        self.file2 = File(
            "video.mp4", "/directory/for/tests/", "/directory/for/tests/video.mp4"
        )

    def _assert_is_typed_file(self, file):
        self.assertIsInstance(
            file, TypedFile, "Manager returns variable that's not instance of TypedFile"
        )

    def test_detect_hit_positions(self):
        positions = (
            (
                "start",
                [wrap_file_as_unknown(self.file1) for _ in range(3)],
                [1, 0, 0],
            ),
            (
                "middle",
                [None, *(wrap_file_as_unknown(self.file1) for _ in range(2))],
                [1, 1, 0],
            ),
            ("end", [None, None, wrap_file_as_unknown(self.file1)], [1, 1, 1]),
        )

        for name, returns, expected_calls in positions:
            with self.subTest(position=name):
                detectors = [
                    MagicMock(spec=IDetector),
                    MagicMock(spec=IDetector),
                    MagicMock(spec=IDetector),
                ]
                for mock, ret in zip(detectors, returns):
                    mock.detect.return_value = ret

                detector_chain = DetectorChain(detectors)
                detector_chain.detect = MagicMock(wraps=detector_chain.detect)

                typed_file = detector_chain.detect(self.file1)

                self._assert_is_typed_file(typed_file)
                detector_chain.detect.assert_called_once_with(self.file1)
                for i, mock in enumerate(detectors):
                    if expected_calls[i]:
                        mock.detect.assert_called_once_with(self.file1)
                    else:
                        mock.detect.assert_not_called()

    def test_detect_no_matches(self):
        detectors = [
            MagicMock(spec=IDetector),
            MagicMock(spec=IDetector),
            MagicMock(spec=IDetector),
        ]
        detectors[0].detect.return_value = None
        detectors[1].detect.return_value = None
        detectors[2].detect.return_value = None
        detector_chain = DetectorChain(detectors)
        detector_chain.detect = MagicMock(wraps=detector_chain.detect)

        with self.assertRaises(NoFallbackDetectorException):
            detector_chain.detect(self.file1)

        detector_chain.detect.assert_called_once_with(self.file1)
        detectors[0].detect.assert_called_once_with(self.file1)
        detectors[1].detect.assert_called_once_with(self.file1)
        detectors[2].detect.assert_called_once_with(self.file1)

    def test_detect_with_fallback(self):
        detectors = [
            MagicMock(spec=IDetector),
            MagicMock(spec=IDetector),
        ]
        detectors[0].detect.return_value = None
        detectors[1].detect.return_value = None

        detector_chain = DetectorChain([*detectors, FallbackDetector()])
        detector_chain.detect = MagicMock(wraps=detector_chain.detect)

        typed_file = detector_chain.detect(self.file1)

        self._assert_is_typed_file(typed_file)
        detector_chain.detect.assert_called_once_with(self.file1)
        detectors[0].detect.assert_called_once_with(self.file1)
        detectors[1].detect.assert_called_once_with(self.file1)

    def test_detect_without_detectors(self):
        detectors = []
        detector_chain = DetectorChain(detectors)
        detector_chain.detect = MagicMock(wraps=detector_chain.detect)

        with self.assertRaises(NoAnyDetectorException):
            detector_chain.detect(self.file1)

        detector_chain.detect.assert_called_once_with(self.file1)

    def test_detect_all(self):
        files = [self.file2, self.file1]
        file_amount = len(files)
        detector = MagicMock(spec=IDetector)
        detector.detect.side_effect = wrap_file_as_unknown
        detectors = [detector]
        detector_chain = DetectorChain(detectors)
        detector_chain.detect_all = MagicMock(wraps=detector_chain.detect_all)
        detector_chain.detect = MagicMock(wraps=detector_chain.detect)

        typed_files = detector_chain.detect_all(files)

        detector_chain.detect.assert_any_call(self.file2)
        detector_chain.detect.assert_any_call(self.file1)
        detector_chain.detect_all.assert_called_once_with([self.file2, self.file1])
        self.assertEqual(detector_chain.detect.call_count, file_amount)
        self.assertEqual(len(typed_files), file_amount)
        for file in typed_files:
            self._assert_is_typed_file(file)

    def test_detect_all_no_files(self):
        files = []
        detector = MagicMock(spec=IDetector)
        detectors = [detector]
        detector_chain = DetectorChain(detectors)
        detector_chain.detect = MagicMock(wraps=detector_chain.detect)
        detector_chain.detect_all = MagicMock(wraps=detector_chain.detect_all)

        typed_files = detector_chain.detect_all(files)

        detector_chain.detect.assert_not_called()
        detector_chain.detect_all.assert_called_once_with(files)
        detector.detect.assert_not_called()
        self.assertEqual(detector_chain.detect.call_count, 0)
        self.assertEqual(len(typed_files), 0)
