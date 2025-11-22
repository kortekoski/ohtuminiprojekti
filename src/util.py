from datetime import datetime
import re
from collections.abc import Iterator


class UserInputError(Exception):
    pass


class ValueError(Exception):
    pass


def validate_reference(ref):
    """Validates the reference information provided by the user according to the specified rules."""

    # Check first that there are no empty entries
    for entry in [ref.year, ref.author, ref.title, ref.type]:
        if not entry:
            raise UserInputError("All fields must be non-empty")

    # Check variable types
    if not isinstance(ref.year, int):
        raise ValueError("Incorrect value type")
    if not all(isinstance(x, str) for x in [ref.author, ref.title, ref.type]):
        raise ValueError("Incorrect value type")

    # Year must be within a reasonable range
    current_year = datetime.now().year
    if ref.year < 1000 or ref.year > current_year:
        raise UserInputError(f"Year must be between 1000 and {current_year}")

    # Author must be in format First Last or Last, First
    if not author_validator(ref.author):
        raise UserInputError(
            "Author must be in format John Smith or Smith, John (or multiple authors separated by ' and ')"
        )

    # Title should be at least 10 characters long?
    if len(ref.title) < 10:
        raise UserInputError("Title must be at least 10 characters long")

    # Type validation, must be one of the valid bibtex types
    bibtex_types = [
        "article",
        "book",
        "booklet",
        "conference",
        "inbook",
        "incollection",
        "inproceedings",
        "manual",
        "mastersthesis",
        "misc",
        "phdthesis",
        "proceedings",
        "techreport",
        "unpublished",
    ]

    if ref.type not in bibtex_types:
        raise UserInputError("Incorrect bibtex reference type")

    return True


def author_validator(author):
    """Validates that the name is in an acceptable format (e.g. John O'Smith; Smith, John)."""
    pattern = r"([A-Z][a-zA-Z'-]*(\s+[A-Z][a-zA-Z'-]*)*)|([A-Z][a-zA-Z'-]*(\s+[A-Z][a-zA-Z'-]*)*,\s+[A-Z][a-zA-Z'-]*(\s+[A-Z][a-zA-Z'-]*)*)"
    authors = [a.strip() for a in author.split(" and ")]
    return all(bool(re.fullmatch(pattern, author)) for author in authors)


def is_valid_reference(maybe_reference: dict[str : list[str] | str | int]) -> bool:
    required_keys = ["year", "author", "title", "type"]

    validator_iter: Iterator[bool] = map(
        lambda x: _is_valid_reference_helper(maybe_reference, x), required_keys
    )
    return all(validator_iter)


def _is_valid_reference_helper(
    maybe_reference: dict[str : list[str]], key: str
) -> bool:
    if key in maybe_reference.keys() and maybe_reference[key] is not []:
        return True
    else:
        return False
