"""Service layer for reference management."""

from util import RefField
from entities.reference import Reference
from repositories.reference_repository import (
    ReferenceRepository,
)

from typing import Optional


class ReferenceService:
    """Business logic for reading and formatting references."""

    def __init__(self, repo=None):
        self._repo = repo or ReferenceRepository()

    def get_all_references(
        self, order_by: RefField = RefField.CITATION_KEY
    ) -> list[Reference]:
        """Fetches all references from the repository."""
        return self._repo.get_references(order_by)

    def create_reference(
        self,
        citation_key: str,
        year: int,
        author: str,
        title: str,
        reftype: str,
        extra: dict[str, str] = {},
    ):
        """Creates a new reference in the repository."""

        if self._repo.citation_key_exists(citation_key):
            raise ValueError(f"Citation key '{citation_key}' already exists.")

        return self._repo.create_reference(
            citation_key, year, author, title, reftype, extra
        )

    def delete_reference(self, citation_key: str):
        """Deletes a reference from the repository."""
        self._repo.delete_reference(citation_key)

    def get_citation_keys(self) -> list[str]:
        """Fetches all citation keys from the repository."""
        references = self._repo.get_references()
        return [ref.citation_key for ref in references]

    def citation_key_exists(self, citation_key: str) -> bool:
        """Checks if a citation key exists in the repository."""
        return citation_key in self.get_citation_keys()
