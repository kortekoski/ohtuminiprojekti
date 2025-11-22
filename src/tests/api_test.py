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
from util import RefField, RefType


class TestAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        app.config["TESTING"] = True
        with app.app_context():
            setup_db()

    def setUp(self):
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

    def test_create_and_get_reference(self):
        ref = {
            RefField.AUTHOR.value: "cool author",
            RefField.YEAR.value: 2025,
            RefField.TITLE.value: "title fit for a cool author",
            RefField.REFTYPE.value: RefType.BOOK.value,
        }

        # Create reference
        self._create_reference(ref)

        # Fetch from DB
        loaded = self._get_reference(1)

        # Remove DB-assigned ID for comparison
        loaded.pop("id", None)

        self.assertEqual(
            loaded,
            ref,
            f"Returned reference does not match expected.\nExpected: {ref}\nActual:   {loaded}",
        )

    def test_create_multiple_and_get_all(self):
        refs = [
            {
                RefField.AUTHOR.value: "cool author 1",
                RefField.YEAR.value: 2025,
                RefField.TITLE.value: "title fit for a cool author 1",
                RefField.REFTYPE.value: RefType.BOOK.value,
            },
            {
                RefField.AUTHOR.value: "cool author 2",
                RefField.YEAR.value: 2024,
                RefField.TITLE.value: "title fit for a cool author 2",
                RefField.REFTYPE.value: RefType.BOOK.value,
            },
            {
                RefField.AUTHOR.value: "cool author 3",
                RefField.YEAR.value: 2023,
                RefField.TITLE.value: "title fit for a cool author 3",
                RefField.REFTYPE.value: RefType.BOOK.value,
            },
        ]

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

    def test_get_nonexistent_reference(self):
        url = f"{REFERENCES_LOCATION}/255"
        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            404,
            f"Expected 404 for nonexistent reference; got {response.status_code}",
        )
        self.assertNotEqual(
            response.get_data(as_text=True),
            "",
            "404 response should contain an error message.",
        )
