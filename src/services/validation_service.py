"""Service for validating references."""

from datetime import datetime
import re
from entities.reference import Reference
from util import RefField, RefType, UserInputError, ValueError


class ValidationService:
    """Business logic for validating references."""

    @staticmethod
    def _validate_empty_entries(ref) -> bool:
        """Checks if a field is empty."""
        for entry in [ref.citation_key, ref.year, ref.author, ref.title, ref.reftype]:
            if not entry:
                raise UserInputError("All fields must be non-empty")

        return True

    @staticmethod
    def _validate_value_types(ref):
        """Checks that the fields have correct value types."""
        if not isinstance(ref.year, int):
            raise ValueError("Incorrect value reftype")
        if not all(
            isinstance(x, str)
            for x in [ref.citation_key, ref.author, ref.title, ref.reftype]
        ):
            raise ValueError("Incorrect value reftype")

        return True

    @staticmethod
    def _validate_year_range(current_year, ref):
        """Checks that the year is within a reasonable range."""
        return ref.year >= 1000 and ref.year <= current_year

    @staticmethod
    def _validate_author(author):
        """Validates that the name is in an acceptable format
        (e.g. John O'Smith; Smith, John)."""
        pattern = r"([A-Z][a-zA-Z'-]*(\s+[A-Z][a-zA-Z'-]*)*)|([A-Z][a-zA-Z'-]*(\s+[A-Z][a-zA-Z'-]*)*,\s+[A-Z][a-zA-Z'-]*(\s+[A-Z][a-zA-Z'-]*)*)"
        authors = [a.strip() for a in author.split(" and ")]
        return all(bool(re.fullmatch(pattern, author)) for author in authors)

    @staticmethod
    def _validate_title(title):
        """Validates that the title is at least 2 characters long."""
        return len(title) >= 2

    @staticmethod
    def _validate_citation_key(citation_key):
        """Validates that the citation key contains only allowed characters."""
        return bool(re.fullmatch(r"[a-zA-Z0-9_:-]+", citation_key))

    @staticmethod
    def _validate_citation_key_starts_with_letter(citation_key):
        """Validates that the citation key starts with a letter."""
        return bool(re.fullmatch(r"[a-zA-Z][a-zA-Z0-9_:-]*", citation_key))

    @staticmethod
    def _validate_citation_key_unique(citation_key, existing_keys):
        """Validates that the citation key is unique."""
        return citation_key not in existing_keys

    @staticmethod
    def _validate_bibtex_reftype(reftype):
        """Validates that the reftype is one of the valid BibTeX reference types."""

        valid_types = {
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
        }

        return reftype in valid_types

    @staticmethod
    def validate_reference(ref: Reference, existing_keys=[]) -> bool:
        """Validates the reference information provided by the user according to the specified rules."""

        # Check first that there are no empty entries
        ValidationService._validate_empty_entries(ref)

        # Check variable reftypes
        ValidationService._validate_value_types(ref)

        # Year must be within a reasonable range
        current_year = datetime.now().year
        if not ValidationService._validate_year_range(current_year, ref):
            raise UserInputError(f"Year must be between 1000 and {current_year}")

        # Author must be in format First Last or Last, First
        if not ValidationService._validate_author(ref.author):
            raise UserInputError(
                """Author must be in format John Smith or Smith, 
                John (or multiple authors separated by ' and ')"""
            )

        # Title should be at least 2 characters long
        if not ValidationService._validate_title(ref.title):
            raise UserInputError("Title must be at least 2 characters long")

        # validate citation key
        if not ValidationService._validate_citation_key(ref.citation_key):
            raise UserInputError("Citation key contains invalid characters")

        if not ValidationService._validate_citation_key_starts_with_letter(
            ref.citation_key
        ):
            raise UserInputError("Citation key must start with a letter")

        if not ValidationService._validate_citation_key_unique(
            ref.citation_key, existing_keys
        ):
            raise UserInputError("Citation key must be unique")

        # Type validation, must be one of the valid bibtex reftypes
        if not ValidationService._validate_bibtex_reftype(ref.reftype):
            raise UserInputError("Incorrect bibtex reference reftype")

        return True
