from datetime import datetime
import re

class UserInputError(Exception):
    pass

def validate_reference(year, author, title, reftype):
    # Check first that there are no empty entries
    for entry in [year, author, title, reftype]:
        if not entry:
            raise UserInputError(f"All fields must be non-empty")
        
    # Check variable types
    if type(year) != int:
        raise ValueError("Incorrect value type")
    if type(author) != str or type(title) != str or type(reftype) != str:
        raise ValueError("Incorrect value type")
        
    # Year must be within a reasonable range
    current_year = datetime.now().year
    if year < 1000 or year > current_year:
        raise UserInputError(f"Year must be between 1000 and {current_year}")

    # Author must be in format First Last or Last, First
    if not author_validator(author):
        raise UserInputError(f"Author must be in format John Smith or Smith, John")
    
    # Title should be at least 10 characters long?
    if len(title) < 10:
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
    "unpublished"
    ]   

    if reftype not in bibtex_types:
        raise UserInputError("Incorrect bibtex reference type")
    
    return True

def author_validator(author):
    # Should accept formats like:
    # - John Smith (First Last)
    # - Maria-Elena O'Brien (with hyphens and apostrophes)
    # - John Middle Smith (with middle names/initials)
    # - Smith, John (Last, First)
    # - O'Brien, Maria-Elena (Last, First with special characters)
    pattern = r"([A-Z][a-zA-Z'-]*(\s+[A-Z][a-zA-Z'-]*)*)|([A-Z][a-zA-Z'-]*(\s+[A-Z][a-zA-Z'-]*)*,\s+[A-Z][a-zA-Z'-]*(\s+[A-Z][a-zA-Z'-]*)*)"
    return bool(re.fullmatch(pattern, author))

def is_valid_reference(
        maybe_reference: dict[str: list[str]|str|int]
) -> bool:
    required_keys = [
        "year",
        "author",
        "title",
        "type"
    ]

    validator_iter: Iterator[bool] = map(
        lambda x: _is_valid_reference_helper(
            maybe_reference, x
        ),
        required_keys
    )
    return all(validator_iter)

def _is_valid_reference_helper(
        maybe_reference: dict[str: list[str]],
        key: str
) -> bool:
    if key in maybe_reference.keys()\
       and maybe_reference[key] is not []:
        return True
    else:
        return False
