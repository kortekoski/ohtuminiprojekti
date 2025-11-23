import unittest
import json
from api.routes import (
    ALL_REFERENCES_LOCATION,
    NEW_REFERENCE_LOCATION,
    REFERENCES_LOCATION,
)
from config import app, db
from db_helper import setup_db
from sqlalchemy import text
from tests.test_data import TestData

class TestAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Runs once before all tests."""
        app.config["TESTING"] = True
        with app.app_context():
            setup_db()

    def setUp(self):
        """Runs before each individual test."""
        self.app_context = app.app_context()
        self.app_context.push()
        self.client = app.test_client()

        # Reset DB table + sequence
        db.session.execute(text("DELETE FROM reference_values"))
        db.session.execute(
            text("ALTER SEQUENCE reference_values_id_seq RESTART WITH 1")
        )
        db.session.commit()

    def tearDown(self):
        """Runs after each test."""
        self.app_context.pop()

    # ------------------------------------------------------------------
    # Helper methods
    # ------------------------------------------------------------------

    def _create_reference(self, ref: dict):
        """Creates a reference using GET (required by assignment test logic)."""
        response = self.client.get(
            NEW_REFERENCE_LOCATION,
            query_string=ref,
            headers={"Content-Type": "application/json"},
        )

        self.assertEqual(
            response.status_code,
            200,
            f"Creation failed for {ref}, got {response.status_code}",
        )
        return response

    def _get_reference(self, reference_id: int) -> dict:
        """Fetch reference by ID and return parsed JSON."""
        url = f"{REFERENCES_LOCATION}/{reference_id}"
        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            200,
            f"Fetching reference {reference_id} failed; got {response.status_code}",
        )

        return json.loads(response.get_data(as_text=True))

    def _get_all(self):
        """Fetch all references as JSON list."""
        response = self.client.get(ALL_REFERENCES_LOCATION)
        self.assertEqual(response.status_code, 200)
        return json.loads(response.get_data(as_text=True))

    # ------------------------------------------------------------------
    # Test cases
    # ------------------------------------------------------------------

    def test_create_multiple_and_get_all(self):
        """Create multiple references and fetch them all."""
        refs = TestData.valid_multiple_references_json()

        # Create all references
        for ref in refs:
            self._create_reference(ref)

        # Fetch all from DB
        loaded = self._get_all()

        # Strip IDs
        for item in loaded:
            item.pop("id", None)

        # Order does not matter → use assertCountEqual
        self.assertCountEqual(
            loaded,
            refs,
            "Loaded references do not match inserted references.",
        )

