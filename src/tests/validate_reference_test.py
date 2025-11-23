import unittest
from util import is_valid_reference, RefField


class TestReferenceValidation(unittest.TestCase):
    def setUp(self):
        """Set up before each test."""
        pass

    def test_valid_reference_is_valid(self):
        """Tests that a complete and valid reference is recognized as valid."""
        test_ref = {
            RefField.YEAR.value: [2004],
            RefField.TITLE.value: ["really cool title"],
            RefField.AUTHOR.value: ["big name author"],
            RefField.REFTYPE.value: ["book"],
        }
        self.assertTrue(is_valid_reference(test_ref))

    def test_incomplete_reference_is_invalid(self):
        """Tests that references missing fields are invalid."""
        test_ref1 = {
            RefField.TITLE.value: "really cool title",
            RefField.AUTHOR.value: "big name author",
            RefField.REFTYPE.value: "book",
        }
        test_ref2 = {
            RefField.YEAR.value: 2004,
            RefField.AUTHOR.value: "big name author",
            RefField.REFTYPE.value: "book",
        }
        test_ref3 = {
            RefField.YEAR.value: 2004,
            RefField.TITLE.value: "really cool title",
            RefField.REFTYPE.value: "book",
        }
        test_ref4 = {
            "year": 2004,
            "title": "really cool title",
            "author": "big name author",
        }

        for ref in [test_ref1, test_ref2, test_ref3, test_ref4]:
            self.assertFalse(is_valid_reference(ref))
