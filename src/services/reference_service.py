"""Service layer for reference management."""

from util import RefField
from entities.reference import Reference
from repositories.reference_repository import (
    ReferenceRepository,
)


class ReferenceService:
    """Business logic for reading and formatting references."""

    def __init__(self, repo=None):
        self._repo = repo or ReferenceRepository()

    def get_all_references(
        self, order_by: RefField = RefField.CITATION_KEY
    ) -> list[Reference]:
        """Fetches all references from the repository."""
        return self._repo.get_references(order_by)

    def get_reference_by_id(self, id: int) -> Reference:
        """Fetches a single reference by its ID from the repository."""
        return self._repo.get_reference_by_id(id)

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

    def update_reference_by_id(
        self,
        id: int,
        citation_key: str,
        year: int = None,
        author: str = None,
        title: str = None,
        reftype: str = None,
        extra: dict[str, str] = None,
    ):
        """Updates an existing reference in the repository.
        If citation_key is changed, ensures the new key does not already exist.
        Otherwise we might end up with duplicate citation keys.
        """
        if self.citation_key_exists(citation_key):
            raise ValueError(f"Citation key '{citation_key}' already exists.")
        self._repo.update_reference(
            id, citation_key, year, author, title, reftype, extra
        )

    def get_citation_keys(self) -> list[str]:
        """Fetches all citation keys from the repository."""
        references = self._repo.get_references()
        return [ref.citation_key for ref in references]

    def citation_key_exists(self, citation_key: str) -> bool:
        """Checks if a citation key exists in the repository."""
        return citation_key in self.get_citation_keys()

    def id_exists(self, id: int) -> bool:
        """Checks if an ID exists in the repository."""
        references = self._repo.get_references()
        return any(ref.id == id for ref in references)
