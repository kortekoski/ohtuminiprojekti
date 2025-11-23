import unittest
from tests.test_data import TestData
from util import is_valid_reference, RefField


class TestReferenceValidation(unittest.TestCase):
    def setUp(self):
        """Set up before each test."""
        pass

    def test_valid_reference_is_valid(self):
        """Tests that a complete and valid reference is recognized as valid."""
        test_ref = TestData.valid_reference_list()
        self.assertTrue(is_valid_reference(test_ref))

    def test_incomplete_reference_is_invalid(self):
        """Tests that references missing fields are invalid."""
        for ref in TestData.incomplete_references():
            self.assertFalse(is_valid_reference(ref))
