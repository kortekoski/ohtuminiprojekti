import unittest
from entities.reference import Reference
from util import RefType


class TestReferenceEntity(unittest.TestCase):

    def test_get_returns_value(self):
        ref = Reference(
            id=1,
            citation_key="Test2024",
            year=2024,
            author="Alice",
            title="My Title",
            reftype=RefType.BOOK.value,
            extra={"publisher": "ACME Press"},
        )

        self.assertEqual(ref.get("publisher"), "ACME Press")

    def test_get_returns_default_when_missing(self):
        ref = Reference(
            id=1,
            citation_key="Test2024",
            year=2024,
            author="Alice",
            title="My Title",
            extra={},
        )

        self.assertEqual(ref.get("missing", "default-value"), "default-value")

    def test_str_contains_all_main_fields(self):
        ref = Reference(
            id=1,
            citation_key="Test2024",
            year=2024,
            author="Alice",
            title="My Title",
            extra={"publisher": "ACME", "pages": "10--20"},
        )

        s = str(ref)

        # Perustarkistukset: __str__ rakentaa nämä mukaan
        self.assertIn("Test2024", s)
        self.assertIn("2024", s)
        self.assertIn("Alice", s)
        self.assertIn("My Title", s)

        # Extra-kentät
        self.assertIn("publisher=ACME", s)
        self.assertIn("pages=10--20", s)


if __name__ == "__main__":
    unittest.main()
