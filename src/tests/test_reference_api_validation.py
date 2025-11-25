import unittest
from services.validation_service import ValidationService
from tests.test_data import TestData


class TestReferenceApiValidation(unittest.TestCase):
    def setUp(self):
        """Set up before each test."""
        pass

    def test_valid_reference_is_valid(self):
        """Tests that a complete and valid reference is recognized as valid."""
        test_ref = TestData.valid_reference_list()
        self.assertTrue(ValidationService.is_valid_reference(test_ref))

    def test_incomplete_reference_is_invalid(self):
        """Tests that references missing fields are invalid."""
        for ref in TestData.incomplete_references():
            self.assertFalse(ValidationService.is_valid_reference(ref))
