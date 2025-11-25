"""Utility helper functions."""

from enum import Enum


class RefField(str, Enum):
    """Enumeration for reference fields."""

    CITATION_KEY = "citation_key"
    YEAR = "year"
    AUTHOR = "author"
    TITLE = "title"
    REFTYPE = "reftype"


class RefType(str, Enum):
    """Enumeration for reference types."""

    ARTICLE = "article"
    BOOK = "book"
    BOOKLET = "booklet"
    CONFERENCE = "conference"
    INBOOK = "inbook"
    INCOLLECTION = "incollection"
    INPROCEEDINGS = "inproceedings"
    MANUAL = "manual"
    MASTERSTHESIS = "mastersthesis"
    MISC = "misc"
    PHDTHESIS = "phdthesis"
    PROCEEDINGS = "proceedings"
    TECHREPORT = "techreport"
    UNPUBLISHED = "unpublished"


class UserInputError(Exception):
    """Exception raised for errors in the user input."""

    pass


class ValueError(Exception):
    """Exception raised for errors in the value type."""

    pass