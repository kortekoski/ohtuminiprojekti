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
        authors = ["John Smith"]
        with self.assertRaises(UserInputError):
            ValidationService._validate_empty_entries(ref, authors)

    # ---------- correct types ----------
    def test_validate_value_types_invalid_year(self):
        ref = MockReference("Key", "2020", "John Smith", "Valid Title", "article")
        authors = ["John Smith"]
        with self.assertRaises(ValueError):
            ValidationService._validate_value_types(ref, authors)

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

    def test_title_exactly_2_characters(self):
        self.assertTrue(ValidationService._validate_title("Ok"))

    # ---------- citation key ----------
    def test_citation_key_invalid(self):
        self.assertFalse(ValidationService._validate_citation_key("Invalid Key!"))

    # ---------- bibtex type ----------
    def test_bibtex_reftype_invalid(self):
        self.assertFalse(ValidationService._validate_bibtex_reftype("notatype"))

    # ---------- authors uniqueness ----------
    def test_authors_unique_valid(self):
        authors = ["John Smith", "Jane Doe", "Bob Johnson"]
        self.assertTrue(ValidationService._validate_authors_unique(authors))

    def test_authors_unique_with_duplicates(self):
        authors = ["John Smith", "Jane Doe", "John Smith"]
        self.assertFalse(ValidationService._validate_authors_unique(authors))

    def test_authors_unique_case_insensitive(self):
        authors = ["John Smith", "jane doe", "JOHN SMITH"]
        self.assertFalse(ValidationService._validate_authors_unique(authors))

    def test_authors_unique_with_whitespace(self):
        authors = ["John Smith", "  John Smith  "]
        self.assertFalse(ValidationService._validate_authors_unique(authors))

    def test_authors_unique_empty_list(self):
        authors = []
        self.assertTrue(ValidationService._validate_authors_unique(authors))

    def test_authors_unique_single_author(self):
        authors = ["John Smith"]
        self.assertTrue(ValidationService._validate_authors_unique(authors))

    def test_validate_reference_with_duplicate_authors(self):
        ref = MockReference(
            "Key2024", 2024, "John Smith and John Smith", "Valid Title", RefType.ARTICLE
        )
        authors = ["John Smith", "John Smith"]
        with self.assertRaises(UserInputError) as context:
            ValidationService.validate_input_reference(
                ref, existing_keys=[], authors=authors
            )
        self.assertIn("duplicate", str(context.exception).lower())
