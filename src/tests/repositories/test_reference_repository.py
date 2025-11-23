"""Unit tests for the Reference Repository."""

import unittest
from sqlalchemy import text
from config import app, db
from db_helper import setup_db

from repositories.reference_repository import (
    get_references,
    create_reference
)


class TestReferenceRepository(unittest.TestCase):
    """Tests for the Reference Repository."""

    @classmethod
    def setUpClass(cls):
        """Runs once before all tests."""
        app.config["TESTING"] = True

        with app.app_context():
            setup_db()  # recreate the test database

    def setUp(self):
        """Runs before each individual test."""
        self.app_context = app.app_context()
        self.app_context.push()

        # Clear table before each test
        db.session.execute(text("DELETE FROM reference_values"))
        # reset the sequence counter to start from 1
        db.session.execute(
            text("ALTER SEQUENCE reference_values_id_seq RESTART WITH 1")
        )
        db.session.commit()

    def tearDown(self):
        """Runs after each test."""
        self.app_context.pop()

    def test_create_and_get_reference(self):
        """Tests creating and retrieving a reference."""
        create_reference(2024, "Test Author", "Test Title", "book")

        refs = get_references()
        self.assertEqual(len(refs), 1)

        ref = refs[0]
        self.assertEqual(ref.year, 2024)
        self.assertEqual(ref.author, "Test Author")
        self.assertEqual(ref.title, "Test Title")


if __name__ == "__main__":
    unittest.main()
