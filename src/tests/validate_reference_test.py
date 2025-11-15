import unittest
from util import is_valid_reference


class TestReferenceValidation(unittest.TestCase):
    def setUp(self):
        pass

    def test_valid_reference_is_valid(self):
        test_ref = {
                "year": [2004],
                "title": ["really cool title"],
                "author": ["big name author"],
                "type": ["book"]
        }
        self.assertTrue(is_valid_reference(test_ref))

    def test_incomplete_reference_is_invalid(self):
        test_ref1 = {
                "title": "really cool title",
                "author": "big name author",
                "type": "book"
        }
        test_ref2 = {
                "year": 2004,
                "author": "big name author",
                "type": "book"
        }
        test_ref3 = {
                "year": 2004,
                "title": "really cool title",
                "type": "book"
        }
        test_ref4 = {
                "year": 2004,
                "title": "really cool title",
                "author": "big name author"
        }

        for ref in [test_ref1,test_ref2,test_ref3,test_ref4]:
            self.assertFalse(is_valid_reference(ref))
