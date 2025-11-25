import unittest
from datetime import datetime
from util import RefField, RefType, UserInputError, ValueError
from services.validation_service import ValidationService


class MockReference:
    def __init__(self, citation_key, year, author, title, reftype):
        self.citation_key = citation_key
        self.year = year
        self.author = author
        self.title = title
        self.reftype = reftype


class TestValidationService(unittest.TestCase):

    # ---------empty entries----------------------
    def test_empty_entries_valid(self):
        ref = MockReference(
            "Key1", 2020, "John Smith", "A Valid Title", RefType.ARTICLE
        )
        self.assertTrue(ValidationService._validate_empty_entries(ref))

    def test_empty_entries_invalid(self):
        ref = MockReference("", 2020, "John Smith", "A Valid Title", RefType.ARTICLE)
        with self.assertRaises(UserInputError):
            ValidationService._validate_empty_entries(ref)

    # -----------------value types---------------------------------
    def test_validate_value_types_valid(self):
        ref = MockReference("Key1", 2020, "John Smith", "A Valid Title", "article")
        self.assertTrue(ValidationService._validate_value_types(ref))

    def test_validate_value_types_invalid_year(self):
        ref = MockReference("Key1", "2020", "John Smith", "A Valid Title", "article")
        with self.assertRaises(ValueError):
            ValidationService._validate_value_types(ref)

    def test_validate_value_types_invalid_field_type(self):
        ref = MockReference(123, 2020, "John Smith", "A Valid Title", "article")
        with self.assertRaises(ValueError):
            ValidationService._validate_value_types(ref)

    # -------------year ranges------------------------------
    def test_year_range_valid(self):
        ref = MockReference("Key1", 2020, "John Smith", "A Valid Title", "article")
        self.assertTrue(
            ValidationService._validate_year_range(datetime.now().year, ref)
        )

    def test_year_range_too_low(self):
        ref = MockReference("Key1", 999, "John Smith", "A Valid Title", "article")
        self.assertFalse(
            ValidationService._validate_year_range(datetime.now().year, ref)
        )

    def test_year_range_too_high(self):
        next_year = datetime.now().year + 1
        ref = MockReference("Key1", next_year, "John Smith", "A Valid Title", "article")
        self.assertFalse(
            ValidationService._validate_year_range(datetime.now().year, ref)
        )

    # ----------------author-------------------------------
    def test_author_valid(self):
        self.assertTrue(ValidationService._validate_author("John Smith"))

    def test_author_valid_last_first(self):
        self.assertTrue(ValidationService._validate_author("Smith, John"))

    def test_author_multiple_valid(self):
        self.assertTrue(ValidationService._validate_author("John Smith and Jane Doe"))

    def test_author_invalid(self):
        self.assertFalse(ValidationService._validate_author("john smith"))

    # -----------------title--------------------------------
    def test_title_valid(self):
        self.assertTrue(ValidationService._validate_title("A Valid Title"))

    def test_title_too_short(self):
        self.assertFalse(ValidationService._validate_title("Too short"))

    # -------------------citation key----------------------------
    def test_citation_key_valid(self):
        self.assertTrue(ValidationService._validate_citation_key("Key_2024"))

    def test_citation_key_invalid(self):
        self.assertFalse(ValidationService._validate_citation_key("Invalid Key!"))

    def test_citation_key_starts_with_letter_valid(self):
        self.assertTrue(
            ValidationService._validate_citation_key_starts_with_letter("A123")
        )

    def test_citation_key_starts_with_letter_invalid(self):
        self.assertFalse(
            ValidationService._validate_citation_key_starts_with_letter("1ABC")
        )

    def test_citation_key_unique_valid(self):
        self.assertTrue(
            ValidationService._validate_citation_key_unique("Key3", ["Key1", "Key2"])
        )

    def test_citation_key_unique_invalid(self):
        self.assertFalse(
            ValidationService._validate_citation_key_unique("Key1", ["Key1", "Key2"])
        )

    # ----------------bibtex reftype---------------------------
    def test_bibtex_reftype_valid(self):
        self.assertTrue(ValidationService._validate_bibtex_reftype(RefType.ARTICLE))

    def test_bibtex_reftype_invalid(self):
        self.assertFalse(ValidationService._validate_bibtex_reftype("notatype"))

    # -------------validate_reference full IT -tests----------------------------

    def test_validate_reference_valid(self):
        ref = MockReference(
            "Key1", 2020, "John Smith", "A Valid Title", RefType.ARTICLE
        )
        self.assertTrue(ValidationService.validate_reference(ref, []))

    def test_validate_reference_invalid_author(self):
        ref = MockReference(
            "Key1", 2020, "john smith", "A Valid Title", RefType.ARTICLE
        )
        with self.assertRaises(UserInputError):
            ValidationService.validate_reference(ref, [])

    def test_validate_reference_invalid_year(self):
        ref = MockReference("Key1", 999, "John Smith", "A Valid Title", RefType.ARTICLE)
        with self.assertRaises(UserInputError):
            ValidationService.validate_reference(ref, [])

    def test_validate_reference_duplicate_key(self):
        ref = MockReference(
            "Key1", 2020, "John Smith", "A Valid Title", RefType.ARTICLE
        )
        with self.assertRaises(UserInputError):
            ValidationService.validate_reference(ref, ["Key1"])


if __name__ == "__main__":
    unittest.main()
