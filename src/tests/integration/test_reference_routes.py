import unittest
import sys
import os

# Add src directory to path - go up two levels from integration folder
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from app import app
from db_helper import setup_db, reset_db
from services.validation_service import ValidationService
from util import UserInputError, ValueError
from tests.test_data import TestData


class TestReferenceRoutes(unittest.TestCase):
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
