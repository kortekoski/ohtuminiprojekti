import unittest
from unittest.mock import Mock
from services.doi_service import DoiService, CrossrefApi
from entities.reference import InputReference
from util import UserInputError, RefType


class TestDoiService(unittest.TestCase):

    def setUp(self):
        self.mock_api = Mock()
        self.service = DoiService(self.mock_api)

    def test_service_handles_correct_input(self):
        """Service should not fail given correct input."""
        try:
            self.service.get_doi("10.221/test", "testkey")
        except UserInputError:
            pass
        self.mock_api.get_doi_metadata.assert_called_with("10.221/test")

        try:
            self.service.get_doi("https://example.com/doi/10.221/test", "testkey")
        except UserInputError:
            pass
        self.mock_api.get_doi_metadata.assert_called_with("10.221/test")

    def test_service_fails_incorrect_input(self):
        """Service should fail given incorrect input"""
        with self.assertRaises(UserInputError):
            self.service.get_doi("", "testkey")

        with self.assertRaises(UserInputError):
            self.service.get_doi("test", "testkey")

        with self.assertRaises(UserInputError):
            self.service.get_doi("https://test.org/doi/test", "testkey")

        with self.assertRaises(UserInputError):
            self.service.get_doi("https://test.org/test", "testkey")

        with self.assertRaises(UserInputError):
            self.service.get_doi("22.222/test", "testkey")

    def test_service_fails_on_non_ok_message(self):
        mock_api = Mock()
        mock_api.get_doi_metadata.return_value = {"status": "fail"}
        service = DoiService(mock_api)
        with self.assertRaises(UserInputError):
            service.get_doi("10.221/test", "testkey")

    def test_service_fails_on_non_work_message(self):
        self.mock_api.get_doi_metadata.return_value = {
            "status": "ok",
            "message-type": "person",
        }
        with self.assertRaises(UserInputError):
            self.service.get_doi("10.221/test", "testkey")

    def test_service_fails_missing_message(self):
        self.mock_api.get_goi_metadata.return_value = {
            "status": "ok",
            "message-type": "work",
        }
        with self.assertRaises(UserInputError):
            self.service.get_doi("10.221/test", "testkey")

    def test_service_fails_non_journal(self):
        self.mock_api.get_doi_metadata.return_value = {
            "status": "ok",
            "message-type": "work",
            "message": {"type": "book"},
        }
        with self.assertRaises(UserInputError):
            self.service.get_doi("10.221/test", "testkey")

    def test_service_fails_no_message(self):
        self.mock_api.get_doi_metadata.return_value = {
            "status": "ok",
            "message-type": "work",
            "type": "journal-article",
        }
        self.assertIsNone(self.service.get_doi("10.221/test", "testkey"))

    def test_service_constructs_reference(self):
        self.mock_api.get_doi_metadata.return_value = {
            "status": "ok",
            "message-type": "work",
            "message": {
                "type": "journal-article",
                "published": {"date-parts": [["2020", "1", "1"]]},
                "title": ["Test title."],
                "ISSN": ["issn00000000"],
                "container-title": ["Journal title"],
                "volume": "1",
                "issue": "1",
                "DOI": "10.221/test",
                "language": "en",
                "author": [
                    {"given": "Jane", "family": "Doe"},
                    {"given": "Jane2", "family": "Doe2"},
                ],
                "publisher": "AAA",
            },
        }
        ref = self.service.get_doi("10.221/test", "testkey")
        self.assertIsNotNone(ref)
        if ref is None:
            raise Exception
        self.assertEqual(ref.citation_key, "testkey")
        self.assertEqual(ref.authors, ["Doe, Jane", "Doe2, Jane2"])
        self.assertEqual(ref.title, "Test title.")
        self.assertEqual(ref.year, 2020)
        ref.extra["month"]
        ref.extra["issn"]
        ref.extra["publisher"]
        ref.extra["journal"]
        ref.extra["volume"]
        ref.extra["issue"]
        ref.extra["doi"]


class TestCrossrefApi(unittest.TestCase):
    def setUp(self):
        self.api = CrossrefApi()

    def test_existing_doi_is_retrieved(self):
        try:
            self.api.get_doi_metadata("10.1136/jclinpath-2020-206745")
        except UserInputError:
            self.fail()
        except:
            self.skipTest(
                "Can't connect to https://api.crossref.org. Check your internet connection."
            )

    def test_nonexistant_doi_raises_error(self):
        with self.assertRaises(UserInputError):
            self.api.get_doi_metadata("10.432/whatever")
