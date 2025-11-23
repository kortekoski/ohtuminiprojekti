from entities.reference import Reference
from util import RefField, RefType


class TestData:
    """Common reusable reference test data."""

    @staticmethod
    def valid_reference_list():
        return {
            RefField.YEAR.value: [2004],
            RefField.TITLE.value: ["really cool title"],
            RefField.AUTHOR.value: ["big name author"],
            RefField.REFTYPE.value: ["book"],
        }

    @staticmethod
    def valid_reference_json():
        return {
            RefField.YEAR.value: "2001",
            RefField.AUTHOR.value: "Bad Dude",
            RefField.TITLE.value: "all out of gum",
            RefField.REFTYPE.value: "book",
        }

    @staticmethod
    def valid_reference():
        return Reference(None, 2001, "Bad Dude", "all out of gum", "book")

    @staticmethod
    def valid_multiple_authors_reference():
        return Reference(
            None,
            2001,
            "Bad Dude and Duke Nukem and Max, Pepsi",
            "all out of gum",
            "book",
        )

    @staticmethod
    def valid_multiple_references_json():
        return [
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

    @staticmethod
    def incomplete_references():
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

        return [test_ref1, test_ref2, test_ref3, test_ref4]

    @staticmethod
    def invalid_bibtex_type():
        return Reference(None, 2001, "Bad Dude", "all out of gum", "value")

    @staticmethod
    def empty_reference():
        return Reference(None, "", "", "", "")

    @staticmethod
    def wrong_year():
        return Reference(None, "string", "Bad Dude", "all out of gum", "book")

    @staticmethod
    def wrong_author():
        return Reference(None, 2001, 1, "all out of gum", "book")

    @staticmethod
    def wrong_title():
        return Reference(None, 2001, "Bad Dude", 1, "book")

    @staticmethod
    def wrong_type():
        return Reference(None, 2001, "Bad Dude", "all out of gum", 1)

    @staticmethod
    def too_short_title():
        return Reference(None, 2001, "Bad Dude", "gum", "book")

    @staticmethod
    def invalid_year_references():
        return [
            Reference(None, 1, "Bad Dude", "all out of gum", "book"),
            Reference(None, 2077, "Bad Dude", "all out of gum", "book"),
        ]

    @staticmethod
    def invalid_author_references():
        return [
            Reference(None, 2001, "bad dude", "all out of gum", "book"),
            Reference(None, 2001, "baddude", "all out of gum", "book"),
            Reference(None, 2001, "dude, bad", "all out of gum", "book"),
            Reference(None, 2001, "Bad Dude1", "all out of gum", "book"),
        ]
