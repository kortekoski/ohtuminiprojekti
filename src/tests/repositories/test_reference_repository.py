import unittest
from sqlalchemy import text

from config import app, db
from db_helper import setup_db
from repositories.reference_repository import ReferenceRepository
from tests.test_data import TestData


class TestReferenceRepository(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Runs once before all tests (creates test DB schema)."""
        app.config["TESTING"] = True
        with app.app_context():
            setup_db()

    def setUp(self):
        """Runs before each test — clears table and resets sequence."""
        self.app_context = app.app_context()
        self.app_context.push()

        db.session.execute(text("DELETE FROM reference_values"))
        db.session.execute(
            text("ALTER SEQUENCE reference_values_id_seq RESTART WITH 1")
        )
        db.session.commit()

        self.repo = ReferenceRepository()

    def tearDown(self):
        """Cleanup after each test."""
        self.app_context.pop()

    def test_get_references_returns_inserted_testdata(self):
        """Repository should return the data inserted using TestData."""

        # Get test reference object
        ref = TestData.valid_reference()

        # Insert into test database using existing create_reference()
        self.repo.create_reference(
            ref.citation_key,
            ref.year,
            [ref.author],
            ref.title,
            ref.reftype,
        )

        # Fetch from repository
        result = self.repo.get_references()

        self.assertEqual(len(result), 1)
        db_ref = result[0]

        # Assert all fields match TestData
        self.assertEqual(db_ref.citation_key, ref.citation_key)
        self.assertEqual(db_ref.year, ref.year)
        self.assertEqual(db_ref.author, ref.author)
        self.assertEqual(db_ref.title, ref.title)
        self.assertEqual(db_ref.reftype, ref.reftype)

    def test_delete_reference_removes_row_from_db(self):
        """Repository.delete_reference should remove the correct row from the database."""

        ref = TestData.valid_reference()

        self.repo.create_reference(
            ref.citation_key,
            ref.year,
            [ref.author],
            ref.title,
            ref.reftype,
        )

        inserted = self.repo.get_references()
        self.assertEqual(len(inserted), 1)

        # Act
        self.repo.delete_reference(ref.citation_key)

        remaining = self.repo.get_references()
        self.assertEqual(len(remaining), 0)

    def test_update_reference_modifies_existing_row(self):
        """Repository.update_reference should modify the correct row in the database."""

        ref = TestData.valid_reference()

        id = self.repo.create_reference(
            ref.citation_key, ref.year, [ref.author], ref.title, ref.reftype, {}
        )

        # Act
        new_authors = ["New Author"]
        new_title = "New Title"
        new_reftype = "book"
        self.repo.update_reference(
            id, ref.citation_key, ref.year, new_authors, new_title, new_reftype, {}
        )

        updated = self.repo.get_references()
        self.assertEqual(len(updated), 1)
        updated_ref = updated[0]

        self.assertEqual(updated_ref.author, new_authors[0])
        self.assertEqual(updated_ref.title, new_title)
        self.assertEqual(updated_ref.reftype, new_reftype)


if __name__ == "__main__":
    unittest.main()
