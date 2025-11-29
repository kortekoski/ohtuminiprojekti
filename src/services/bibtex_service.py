from util import RefField, RefType
from entities.reference import Reference


class BibtexService:
    """Business logic for reading and formatting references."""

    @staticmethod
    def generate_bibtex(refs: list[Reference]) -> str:

        entries = []
        for ref in refs:
            reftype = (
                ref.reftype.value if isinstance(ref.reftype, RefType) else ref.reftype
            )

            entry = (
                f"@{reftype}{{{ref.citation_key},\n"
                f"  {RefField.AUTHOR.value} = {{{ref.author}}},\n"
                f"  {RefField.TITLE.value} = {{{ref.title}}},\n"
                f"  {RefField.YEAR.value} = {{{ref.year}}}"
            )

            for key, value in ref.extra:
                entry += f",\n  {key} = {{{value}}}"

            entry += f"\n}}\n"
            entries.append(entry)

        bibtex_content = "\n".join(entries)
        return bibtex_content
