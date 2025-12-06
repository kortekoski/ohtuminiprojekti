from entities.reference import Reference, InputReference
from util import RefField, RefType


class TestData:
    """Common reusable reference test data."""

    @staticmethod
    def valid_reference_object():
        return Reference(1, "Test2024", 2001, "Bad Dude", "all out of gum", "book", {})

    @staticmethod
    def valid_input_reference():
        return InputReference(
            citation_key="Test2024",
            year=2001,
            authors=["Bad Dude"],
            title="all out of gum",
            reftype="book",
            extra={},
            id=1,
        )

    @staticmethod
    def valid_multiple_reference_objects():
        return [
            Reference(1, "Test2024", 2001, "Bad Dude", "all out of gum", "book", {}),
            Reference(2, "Test2025", 2002, "Good Dude", "all out of gum", "book", {}),
        ]

    @staticmethod
    def valid_reference_list():
        return {
            RefField.CITATION_KEY.value: ["Test2024"],
            RefField.YEAR.value: [2004],
            RefField.TITLE.value: ["really cool title"],
            RefField.AUTHOR.value: ["big name author"],
            RefField.REFTYPE.value: ["book"],
        }

    @staticmethod
    def valid_reference_json():
        return {
            RefField.CITATION_KEY.value: "Test2024",
            RefField.YEAR.value: "2001",
            RefField.AUTHOR.value: "Bad Dude",
            RefField.TITLE.value: "all out of gum",
            RefField.REFTYPE.value: "book",
            RefField.EXTRA.value: {},
        }

    @staticmethod
    def updated_reference_json():
        return {
            "id": "1",
            RefField.CITATION_KEY.value: "Test2025",
            RefField.YEAR.value: "2001",
            RefField.AUTHOR.value: "Good Dude",
            RefField.TITLE.value: "all out of gum",
            RefField.REFTYPE.value: "book",
            RefField.EXTRA.value: {},
        }

    @staticmethod
    def valid_reference():
        return Reference(
            None, "Test2024", 2001, "Bad Dude", "all out of gum", "book", {}
        )

    @staticmethod
    def valid_multiple_authors_reference():
        return Reference(
            None,
            "Test2024",
            2001,
            "Bad Dude and Duke Nukem and Max, Pepsi",
            "all out of gum",
            "book",
            {},
        )

    @staticmethod
    def valid_multiple_references_json():
        return [
            {
                RefField.CITATION_KEY.value: "coolauthor1",
                RefField.AUTHOR.value: "cool author 1",
                RefField.YEAR.value: 2025,
                RefField.TITLE.value: "title fit for a cool author 1",
                RefField.REFTYPE.value: RefType.BOOK.value,
                RefField.EXTRA.value: {},
            },
            {
                RefField.CITATION_KEY.value: "coolauthor2",
                RefField.AUTHOR.value: "cool author 2",
                RefField.YEAR.value: 2024,
                RefField.TITLE.value: "title fit for a cool author 2",
                RefField.REFTYPE.value: RefType.BOOK.value,
                RefField.EXTRA.value: {},
            },
            {
                RefField.CITATION_KEY.value: "coolauthor3",
                RefField.AUTHOR.value: "cool author 3",
                RefField.YEAR.value: 2023,
                RefField.TITLE.value: "title fit for a cool author 3",
                RefField.REFTYPE.value: RefType.BOOK.value,
                RefField.EXTRA.value: {},
            },
        ]

    @staticmethod
    def incomplete_references():
        test_ref1 = {
            RefField.CITATION_KEY.value: "Test2024",
            RefField.TITLE.value: "really cool title",
            RefField.AUTHOR.value: "big name author",
            RefField.REFTYPE.value: "book",
            RefField.EXTRA.value: {},
        }
        test_ref2 = {
            RefField.CITATION_KEY.value: "Test2024",
            RefField.YEAR.value: 2004,
            RefField.AUTHOR.value: "big name author",
            RefField.REFTYPE.value: "book",
            RefField.EXTRA.value: {},
        }
        test_ref3 = {
            RefField.CITATION_KEY.value: "Test2024",
            RefField.YEAR.value: 2004,
            RefField.TITLE.value: "really cool title",
            RefField.REFTYPE.value: "book",
            RefField.EXTRA.value: {},
        }
        test_ref4 = {
            RefField.CITATION_KEY.value: "Test2024",
            RefField.YEAR.value: 2004,
            RefField.TITLE.value: "really cool title",
            RefField.AUTHOR.value: "big name author",
            RefField.EXTRA.value: {},
        }

        return [test_ref1, test_ref2, test_ref3, test_ref4]

    @staticmethod
    def invalid_bibtex_type():
        return Reference(
            None, "Test2024", 2001, "Bad Dude", "all out of gum", "value", {}
        )

    @staticmethod
    def empty_reference():
        return Reference(None, "", "", "", "", "", {})

    @staticmethod
    def wrong_year():
        return Reference(
            None, "Test2024", "string", "Bad Dude", "all out of gum", "book", {}
        )

    @staticmethod
    def wrong_author():
        return Reference(None, "Test2024", 2001, 1, "all out of gum", "book", {})

    @staticmethod
    def wrong_title():
        return Reference(None, "Test2024", 2001, "Bad Dude", 1, "book", {})

    @staticmethod
    def wrong_type():
        return Reference(None, "Test2024", 2001, "Bad Dude", "all out of gum", 1, {})

    @staticmethod
    def too_short_title():
        return Reference(None, "Test2024", 2001, "Bad Dude", "gum", "book", {})

    @staticmethod
    def invalid_year_references():
        return [
            Reference(None, "Test2024", 1, "Bad Dude", "all out of gum", "book", {}),
            Reference(None, "Test2025", 2077, "Bad Dude", "all out of gum", "book", {}),
        ]

    @staticmethod
    def invalid_author_references():
        return [
            Reference(None, "Test2024", 2001, "bad dude", "all out of gum", "book", {}),
            Reference(None, "Test2025", 2001, "baddude", "all out of gum", "book", {}),
            Reference(
                None, "Test2026", 2001, "dude, bad", "all out of gum", "book", {}
            ),
            Reference(
                None, "Test2027", 2001, "Bad Dude1", "all out of gum", "book", {}
            ),
        ]
