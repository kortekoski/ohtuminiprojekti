import unittest
import json
from api.routes import ALL_REFERENCES_LOCATION, NEW_REFERENCE_LOCATION, REFERENCES_LOCATION
from config import app, db
from db_helper import setup_db
from sqlalchemy import text


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

        db.session.execute(text("DELETE FROM reference_values"))
        db.session.execute(
            text("ALTER SEQUENCE reference_values_id_seq RESTART WITH 1")
        )
        db.session.commit()

    def tearDown(self):
        self.app_context.pop()

    def test_create_and_get_reference(self):
        ref = {
            "author": "cool author",
            "year": 2025,
            "title": "title fit for a cool author",
            "type": "book",
        }
        response = self.client.get(
            NEW_REFERENCE_LOCATION,
            query_string=ref,
            headers={"Content-Type": "application/json"},
        )
        self.assertTrue(response.status_code == 200)
        self.assertTrue(response.get_data(as_text=True) != "")

        response = self.client.get(
            REFERENCES_LOCATION + "/1", headers={"Content-Type": "application/json"}
        )
        self.assertTrue(response.status_code == 200)
        response_ref = json.loads(response.get_data(as_text=True))
        response_ref.pop("id")
        self.assertTrue(response_ref == ref)

    def test_create_multiple_and_get_all(self):
        refs = [
            {
                "author": "cool author 1",
                "year": 2025,
                "title": "title fit for a cool author 1",
                "type": "book",
            },
            {
                "author": "cool author 2",
                "year": 2024,
                "title": "title fit for a cool author 2",
                "type": "book",
            },
            {
                "author": "cool author 3",
                "year": 2023,
                "title": "title fit for a cool author 3",
                "type": "book",
            },
        ]

        for ref in refs:
            res = self.client.get(
                NEW_REFERENCE_LOCATION,
                query_string=ref,
                headers={"Content-Type": "application/json"},
            )
            self.assertTrue(res.status_code == 200)

        res = self.client.get(ALL_REFERENCES_LOCATION)
        self.assertTrue(res.status_code == 200)
        res_loaded = json.loads(res.get_data(as_text=True))
        for item in res_loaded:
            item.pop("id")

        self.assertTrue(all([res_item in refs for res_item in res_loaded]))

    def test_get_nonexistent_reference(self):
        res = self.client.get(REFERENCES_LOCATION + "/255")
        self.assertTrue(res.status_code == 404)
        self.assertTrue(res.get_data(as_text=True) != "")
