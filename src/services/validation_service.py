"""Service for validating references."""

from datetime import datetime
import re
from entities.reference import InputReference, Reference
from util import RefField, RefType, UserInputError, ValueError


class ValidationService:
    """Business logic for validating references."""

    @staticmethod
    def _validate_empty_entries(ref, authors: list[str]) -> bool:
        """Checks if a field is empty."""
        for entry in [ref.citation_key, ref.year, ref.title, ref.reftype]:
            if not entry:
                raise UserInputError("All fields must be non-empty")

        # Check that authors list exists and has at least one non-empty author
        if not authors or not any(author.strip() for author in authors):
            raise UserInputError("All fields must be non-empty")

        return True

    @staticmethod
    def _validate_value_types(ref, authors: list[str]):
        """Checks that the fields have correct value types."""
        if not isinstance(ref.year, int):
            raise ValueError("Incorrect value reftype")
        if not all(
            isinstance(x, str) for x in [ref.citation_key, ref.title, ref.reftype]
        ):
            raise ValueError("Incorrect value reftype")

        # Validate authors is a list of strings
        if not isinstance(authors, list) or not all(
            isinstance(a, str) for a in authors
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
        (e.g. John O'Smith; Smith, John; Järvinen, Päivi; John X. Smith)."""
        # Pattern that accepts Unicode letters, apostrophes, hyphens, and middle initials
        pattern = (
            r"([A-ZÀ-ÖØ-Þ][a-zA-ZÀ-ÖØ-öø-ÿ'-]*(\s+[A-ZÀ-ÖØ-Þ]\.?|\s+[a-zA-ZÀ-ÖØ-öø-ÿ'-]+)*)|"
            r"([A-ZÀ-ÖØ-Þ][a-zA-ZÀ-ÖØ-öø-ÿ'-]*(\s+[a-zA-ZÀ-ÖØ-öø-ÿ'-]+)*,\s+[A-ZÀ-ÖØ-Þ]\.?(\s+[a-zA-ZÀ-ÖØ-öø-ÿ'-]+)*)"
        )
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
    def _validate_authors_unique(authors: list[str]):
        """Validates that there are no duplicate author names in the list."""
        # Normalize author names (strip whitespace and compare case-insensitively)
        normalized_authors = [
            author.strip().lower() for author in authors if author.strip()
        ]
        return len(normalized_authors) == len(set(normalized_authors))

    @staticmethod
    def _validate_authors_not_empty_strings(authors: list[str]):
        """Validates that no author in the list is an empty or whitespace-only string."""
        return all(author.strip() for author in authors)

    @staticmethod
    def _validate_author_names_format(authors: list[str]):
        """Validates that each author name is in an acceptable format."""
        # Pattern that accepts Unicode letters, apostrophes, hyphens, and middle initials
        pattern = (
            r"([A-ZÀ-ÖØ-Þ][a-zA-ZÀ-ÖØ-öø-ÿ'-]*(\s+[A-ZÀ-ÖØ-Þ]\.?|\s+[a-zA-ZÀ-ÖØ-öø-ÿ'-]+)*)|"
            r"([A-ZÀ-ÖØ-Þ][a-zA-ZÀ-ÖØ-öø-ÿ'-]*(\s+[a-zA-ZÀ-ÖØ-öø-ÿ'-]+)*,\s+[A-ZÀ-ÖØ-Þ]\.?(\s+[a-zA-ZÀ-ÖØ-öø-ÿ'-]+)*)"
        )
        return all(
            bool(re.fullmatch(pattern, author.strip()))
            for author in authors
            if author.strip()
        )

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
    def validate_input_reference(
        ref: InputReference,
        existing_keys=[],
        same_citation_key=False,
        authors: list[str] = None,
    ) -> bool:
        """
        Validates the reference information provided by the user
        according to the specified rules.

        Args:
            ref: The reference to validate
            existing_keys: List of existing citation keys
            same_citation_key: Whether to skip citation key uniqueness check
            authors: Optional list of author names to validate for duplicates
        """

        # Check first that there are no empty entries
        ValidationService._validate_empty_entries(ref, authors)

        # Check variable reftypes
        ValidationService._validate_value_types(ref, authors)

        # Year must be within a reasonable range
        current_year = datetime.now().year
        if not ValidationService._validate_year_range(current_year, ref):
            raise UserInputError(f"Year must be between 1000 and {current_year}")

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

        # Skips the uniqueness check if the citation key is unchanged in an update
        if not same_citation_key:
            if not ValidationService._validate_citation_key_unique(
                ref.citation_key, existing_keys
            ):
                raise UserInputError("Citation key must be unique")

        # Type validation, must be one of the valid bibtex reftypes
        if not ValidationService._validate_bibtex_reftype(ref.reftype):
            raise UserInputError("Incorrect bibtex reference reftype")

        # Validate authors list if provided
        if authors is not None:
            if not ValidationService._validate_authors_not_empty_strings(authors):
                raise UserInputError("Author names cannot be empty")

            if not ValidationService._validate_author_names_format(authors):
                raise UserInputError("Author names must be in correct format")

            if not ValidationService._validate_authors_unique(authors):
                raise UserInputError(
                    "Author names must be unique - duplicate authors found"
                )

        return True
