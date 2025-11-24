from repositories.reference_repository import create_reference, get_references
from util import RefField, RefType
from entities.reference import Reference


class ReferenceService:
    """Business logic for reading and formatting references."""

    @staticmethod
    def generate_bibtex(refs: list[Reference]) -> str:

        entries = []
        for ref in refs:
            entry = (
                f"@{ref.reftype.value}{{{ref.citation_key},\n"
                f"  {RefField.AUTHOR.value} = {{{ref.author}}},\n"
                f"  {RefField.TITLE.value} = {{{ref.title}}},\n"
                f"  {RefField.YEAR.value} = {{{ref.year}}}\n"
                f"}}\n"
            )

            entries.append(entry)

        bibtex_content = "\n".join(entries)
        return bibtex_content
