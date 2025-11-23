"""Utility functions and classes for reference validation and management."""

from datetime import datetime
from enum import Enum
import re
from collections.abc import Iterator


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


def validate_reference(ref):
    """Validates the reference information provided by the user according to the specified rules."""

    # Check first that there are no empty entries
    for entry in [ref.citation_key, ref.year, ref.author, ref.title, ref.reftype]:
        if not entry:
            raise UserInputError("All fields must be non-empty")

    # Check variable reftypes
    if not isinstance(ref.year, int):
        raise ValueError("Incorrect value reftype")
    if not all(
        isinstance(x, str)
        for x in [ref.citation_key, ref.author, ref.title, ref.reftype]
    ):
        raise ValueError("Incorrect value reftype")

    # Year must be within a reasonable range
    current_year = datetime.now().year
    if ref.year < 1000 or ref.year > current_year:
        raise UserInputError(f"Year must be between 1000 and {current_year}")

    # Author must be in format First Last or Last, First
    if not author_validator(ref.author):
        raise UserInputError(
            """Author must be in format John Smith or Smith, 
            John (or multiple authors separated by ' and ')"""
        )

    # Title should be at least 10 characters long?
    if len(ref.title) < 10:
        raise UserInputError("Title must be at least 10 characters long")

    # Type validation, must be one of the valid bibtex reftypes
    bibtex_reftypes = [
        RefType.ARTICLE,
        RefType.BOOK,
        RefType.BOOKLET,
        RefType.CONFERENCE,
        RefType.INBOOK,
        RefType.INCOLLECTION,
        RefType.INPROCEEDINGS,
        RefType.MANUAL,
        RefType.MASTERSTHESIS,
        RefType.MISC,
        RefType.PHDTHESIS,
        RefType.PROCEEDINGS,
        RefType.TECHREPORT,
        RefType.UNPUBLISHED,
    ]

    if ref.reftype not in bibtex_reftypes:
        raise UserInputError("Incorrect bibtex reference reftype")

    return True


def author_validator(author):
    """Validates that the name is in an acceptable format
    (e.g. John O'Smith; Smith, John)."""
    pattern = r"([A-Z][a-zA-Z'-]*(\s+[A-Z][a-zA-Z'-]*)*)|([A-Z][a-zA-Z'-]*(\s+[A-Z][a-zA-Z'-]*)*,\s+[A-Z][a-zA-Z'-]*(\s+[A-Z][a-zA-Z'-]*)*)"
    authors = [a.strip() for a in author.split(" and ")]
    return all(bool(re.fullmatch(pattern, author)) for author in authors)


def is_valid_reference(maybe_reference: dict[str : list[str] | str | int]) -> bool:
    """Checks that the provided dictionary has all required keys for a reference."""
    required_keys = [
        RefField.CITATION_KEY,
        RefField.YEAR,
        RefField.AUTHOR,
        RefField.TITLE,
        RefField.REFTYPE,
    ]

    validator_iter: Iterator[bool] = map(
        lambda x: _is_valid_reference_helper(maybe_reference, x), required_keys
    )
    return all(validator_iter)


def _is_valid_reference_helper(maybe_reference: dict[str, list[str]], key: str) -> bool:
    return key in maybe_reference and maybe_reference[key] != []
