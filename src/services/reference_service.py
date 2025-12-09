"""Service layer for reference management."""

from util import RefField
from entities.reference import Reference, InputReference
from repositories.reference_repository import (
    ReferenceRepository,
)


class ReferenceService:
    """Business logic for reading and formatting references."""

    def __init__(self, repo=None):
        self._repo = repo or ReferenceRepository()

    def get_all_references(
        self,
        bibtex: bool = False,
        order_by: RefField = RefField.CITATION_KEY,
        author_filter: str = None,
        year_filter: str = None,
    ) -> list[Reference]:
        """Fetches all references from the repository."""
        ref_list = self._repo.get_references(order_by)

        if author_filter:
            author_filter = author_filter.lower()
            ref_list = [
                ref
                for ref in ref_list
                if ref.author and author_filter in ref.author.lower()
            ]

        if year_filter:
            ref_list = [ref for ref in ref_list if str(ref.year) == str(year_filter)]

        if bibtex:
            return ref_list
        parsed_ref_list = self.parse_authors(ref_list)
        return parsed_ref_list

    def parse_authors(self, ref_list: list[Reference]) -> list[str]:
        """Parses a string of authors separated by ' and ' into a list."""
        for ref in ref_list:
            ref.author = self.parse_author_string(ref.author)
        return ref_list

    def parse_author_string(self, author_string: str) -> str:
        """Parses a string of authors separated by ' and ' into abbreviated format."""

        authors = [self.parse_name(a.strip()) for a in author_string.split(" and ")]

        if len(authors) > 3:
            return f"{authors[0]} et al."
        return " and ".join(authors)

    def parse_name(self, name: str) -> str:
        """Parses a single author's name into 'Last, F.' format."""
        if "," in name:
            parts = name.split(",", 1)
            lastname = parts[0].strip()
            firstname = parts[1].strip() if len(parts) > 1 else ""
            if firstname:
                # Split firstname by spaces to handle middle names
                first_names = firstname.split()
                # Take first letter of each name part and add periods
                initials = ". ".join([n[0] for n in first_names if n]) + "."
                return f"{lastname}, {initials}"
            return lastname
        else:
            return name.strip()

    def get_reference_by_id(self, id: int) -> Reference:
        """Fetches a single reference by its ID from the repository."""
        return self._repo.get_reference_by_id(id)

    def create_reference(self, input_ref: InputReference):
        """Creates a new reference in the repository."""

        if self._repo.citation_key_exists(input_ref.citation_key):
            raise ValueError(f"Citation key '{input_ref.citation_key}' already exists.")

        return self._repo.create_reference(input_ref)

    def delete_reference(self, citation_key: str):
        """Deletes a reference from the repository."""
        self._repo.delete_reference(citation_key)

    def update_reference_by_id(
        self, input_ref: InputReference, same_citation_key: bool = False
    ):
        """Updates an existing reference in the repository.
        If citation_key is changed, ensures the new key does not already exist.
        Otherwise we might end up with duplicate citation keys.
        This check is skipped if the updated ref keeps the same citation key.
        """
        if self.citation_key_exists(input_ref.citation_key) and not same_citation_key:
            raise ValueError(f"Citation key '{input_ref.citation_key}' already exists.")

        self._repo.update_reference(input_ref)

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
