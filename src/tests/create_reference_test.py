import unittest
import sys
import os

# Import app from app.py to ensure routes are registered
from app import app
from db_helper import setup_db, reset_db
from util import validate_reference, UserInputError, ValueError, RefField
from entities.reference import Reference
from tests.test_data import TestData

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


class TestAddReference(unittest.TestCase):
    def setUp(self):
        """Set up test client and database before each test"""
        app.config["TESTING"] = True
        self.client = app.test_client()

        with app.app_context():
            setup_db()

    def tearDown(self):
        """Clean up after each test"""
        with app.app_context():
            reset_db()

    def test_valid_reference_goes_through(self):
        """Tests that a valid reference passes validation."""
        ref = TestData.valid_reference()

        self.assertTrue(validate_reference(ref))

    def test_cannot_add_empty_reference(self):
        """Tests that reference fields are not empty."""
        ref = TestData.empty_reference()
        with self.assertRaises(UserInputError):
            self.assertRaises(validate_reference(ref))

    def test_cannot_add_wrong_value_types(self):
        """Tests that fields have correct types."""
        ref1 = TestData.wrong_year()
        ref2 = TestData.wrong_author()
        ref3 = TestData.wrong_title()
        ref4 = TestData.wrong_type()

        for ref in [ref1, ref2, ref3, ref4]:
            with self.assertRaises(ValueError):
                self.assertRaises(validate_reference(ref))

    def test_year_must_be_in_valid_range(self):
        """Tests that year is within valid range."""
        for ref in TestData.invalid_year_references():
            with self.assertRaises(UserInputError):
                self.assertRaises(validate_reference(ref))

    def test_author_must_be_in_correct_format(self):
        """Tests that author name is in correct format."""
        for ref in TestData.invalid_author_references():
            with self.assertRaises(UserInputError):
                self.assertRaises(validate_reference(ref))

    def test_multiple_authors_accepted(self):
        """Tests that multiple authors are accepted."""
        ref1 = TestData.valid_multiple_authors_reference()
        self.assertTrue(validate_reference(ref1))

    def test_title_must_be_10_characters_long(self):
        """Tests that title is at least 10 characters long."""
        ref = TestData.too_short_title()

        with self.assertRaises(UserInputError):
            self.assertRaises(validate_reference(ref))

    def test_type_must_be_bibtex_type(self):
        """Tests that reference type is a valid BibTeX type."""
        ref = TestData.invalid_bibtex_type()

        with self.assertRaises(UserInputError):
            self.assertRaises(validate_reference(ref))

    def test_create_valid_reference_redirects_to_home(self):
        """Test that creating a valid reference redirects to home"""
        response = self.client.post(
            "/create_reference",
            data=TestData.valid_reference_json(),
        )
        # Should redirect to home on success (302 or 303)
        self.assertIn(response.status_code, [302, 303])
        self.assertEqual(response.location, "/")

    def test_create_reference_appears_on_index(self):
        """Test that created reference appears on the index page"""
        self.client.post("/create_reference", data=TestData.valid_reference_json())

        response = self.client.get("/")
        self.assertIn(b"Bad Dude", response.data)
        self.assertIn(b"all out of gum", response.data)
        self.assertIn(b"2001", response.data)
