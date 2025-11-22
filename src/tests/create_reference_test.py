import unittest
import sys
import os

# Import app from app.py to ensure routes are registered
from app import app
from db_helper import setup_db, reset_db
from util import validate_reference, UserInputError, ValueError, RefField
from entities.reference import Reference

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
        ref = Reference(None, 2001, "Bad Dude", "all out of gum", "book")

        self.assertTrue(validate_reference(ref))

    def test_cannot_add_empty_reference(self):
        ref = Reference("", "", "", "")
        with self.assertRaises(UserInputError):
            self.assertRaises(validate_reference(ref))

    def test_cannot_add_wrong_value_types(self):
        ref1 = Reference(None, "string", "Bad Dude", "all out of gum", "book")
        ref2 = Reference(None, 2001, 1, "all out of gum", "book")
        ref3 = Reference(None, 2001, "Bad Dude", 1, "book")
        ref4 = Reference(None, 2001, "Bad Dude", "all out of gum", 1)

        for ref in [ref1, ref2, ref3, ref4]:
            with self.assertRaises(ValueError):
                self.assertRaises(validate_reference(ref))

    def test_year_must_be_in_valid_range(self):
        ref1 = Reference(None, 1, "Bad Dude", "all out of gum", "book")
        ref2 = Reference(None, 2077, "Bad Dude", "all out of gum", "book")

        for ref in [ref1, ref2]:
            with self.assertRaises(UserInputError):
                self.assertRaises(validate_reference(ref))

    def test_author_must_be_in_correct_format(self):
        ref1 = Reference(None, 2001, "bad dude", "all out of gum", "book")
        ref2 = Reference(None, 2001, "baddude", "all out of gum", "book")
        ref3 = Reference(None, 2001, "dude, bad", "all out of gum", "book")
        ref4 = Reference(None, 2001, "Bad Dude1", "all out of gum", "book")

        for ref in [ref1, ref2, ref3, ref4]:
            with self.assertRaises(UserInputError):
                self.assertRaises(validate_reference(ref))

    def test_multiple_authors_accepted(self):
        ref1 = Reference(
            None,
            2001,
            "Bad Dude and Duke Nukem and Max, Pepsi",
            "all out of gum",
            "book",
        )

        self.assertTrue(validate_reference(ref1))

    def test_title_must_be_10_characters_long(self):
        ref = Reference(None, 2001, "Bad Dude", "gum", "book")

        with self.assertRaises(UserInputError):
            self.assertRaises(validate_reference(ref))

    def test_type_must_be_bibtex_type(self):
        ref = Reference(None, 2001, "Bad Dude", "all out of gum", "value")

        with self.assertRaises(UserInputError):
            self.assertRaises(validate_reference(ref))

    def test_create_valid_reference_redirects_to_home(self):
        """Test that creating a valid reference redirects to home"""
        response = self.client.post(
            "/create_reference",
            data={
                RefField.YEAR.value: "2001",
                RefField.AUTHOR.value: "Bad Dude",
                RefField.TITLE.value: "all out of gum",
                RefField.REFTYPE.value: "book",
            },
        )
        # Should redirect to home on success (302 or 303)
        self.assertIn(response.status_code, [302, 303])
        self.assertEqual(response.location, "/")

    def test_create_reference_appears_on_index(self):
        """Test that created reference appears on the index page"""
        self.client.post(
            "/create_reference",
            data={
                RefField.YEAR.value: "2001",
                RefField.AUTHOR.value: "Bad Dude",
                RefField.TITLE.value: "all out of gum",
                RefField.REFTYPE.value: "book",
            },
        )

        response = self.client.get("/")
        self.assertIn(b"Bad Dude", response.data)
        self.assertIn(b"all out of gum", response.data)
        self.assertIn(b"2001", response.data)
