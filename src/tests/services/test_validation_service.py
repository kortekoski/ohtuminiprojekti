import unittest
from datetime import datetime
from util import RefType, UserInputError, ValueError
from services.validation_service import ValidationService


class MockReference:
    def __init__(self, citation_key, year, author, title, reftype):
        self.citation_key = citation_key
        self.year = year
        self.author = author
        self.title = title
        self.reftype = reftype


class TestValidationServiceUnit(unittest.TestCase):

    # -------- basic required fields ----------
    def test_empty_entries_invalid(self):
        ref = MockReference("", 2020, "John Smith", "Valid Title", RefType.ARTICLE)
        with self.assertRaises(UserInputError):
            ValidationService._validate_empty_entries(ref)

    # ---------- correct types ----------
    def test_validate_value_types_invalid_year(self):
        ref = MockReference("Key", "2020", "John Smith", "Valid Title", "article")
        with self.assertRaises(ValueError):
            ValidationService._validate_value_types(ref)

    # ---------- year range ----------
    def test_year_range_invalid(self):
        ref = MockReference("Key", 999, "John Smith", "Valid Title", "article")
        self.assertFalse(
            ValidationService._validate_year_range(datetime.now().year, ref)
        )

    # ---------- author ----------
    def test_author_invalid(self):
        self.assertFalse(ValidationService._validate_author("john smith"))

    # ---------- title ----------
    def test_title_too_short(self):
        self.assertFalse(ValidationService._validate_title("T"))

    # ---------- citation key ----------
    def test_citation_key_invalid(self):
        self.assertFalse(ValidationService._validate_citation_key("Invalid Key!"))

    # ---------- bibtex type ----------
    def test_bibtex_reftype_invalid(self):
        self.assertFalse(ValidationService._validate_bibtex_reftype("notatype"))
