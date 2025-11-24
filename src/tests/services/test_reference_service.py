import unittest
from entities.reference import Reference
from util import RefType, RefField
from services.reference_service import ReferenceService


class TestReferenceService(unittest.TestCase):

    def test_generate_bibtex(self):
        refs = [
            Reference(
                id=1,
                citation_key="Zelda1998",
                year=1998,
                author="Zelda",
                title="Tunes for the harp, ocarina and violin",
                reftype=RefType.BOOK,
            ),
            Reference(
                id=2,
                citation_key="Freeman1998",
                year=1998,
                author="Gordon Freeman",
                title="Bending reality - a scientific approach",
                reftype=RefType.ARTICLE,
            ),
        ]

        bibtex = ReferenceService.generate_bibtex(refs)

        expected = (
            "@book{Zelda1998,\n"
            f"  {RefField.AUTHOR.value} = {{Zelda}},\n"
            f"  {RefField.TITLE.value} = {{Tunes for the harp, ocarina and violin}},\n"
            f"  {RefField.YEAR.value} = {{1998}}\n"
            "}\n"
            "\n"
            "@article{Freeman1998,\n"
            f"  {RefField.AUTHOR.value} = {{Gordon Freeman}},\n"
            f"  {RefField.TITLE.value} = {{Bending reality - a scientific approach}},\n"
            f"  {RefField.YEAR.value} = {{1998}}\n"
            "}\n"
        )

        # Assert
        self.assertEqual(bibtex.strip(), expected.strip())


if __name__ == "__main__":
    unittest.main()
