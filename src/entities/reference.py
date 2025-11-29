"""Reference entity module."""

from dataclasses import dataclass
from util import RefType

from typing import Optional


@dataclass
class Reference:
    """Reference entity representing a bibliographic reference."""

    id: int
    citation_key: str
    year: int
    author: str
    title: str
    reftype: str = RefType.BOOK.value
    attributes: dict[str, str] = dict()

    def get(self, attribute: str, default: Optional[str] = None) -> Optional[str]:
        self.attributes.get(attribute, default)

    def __str__(self):
        string = f"{self.citation_key}: {self.year}, {self.author}, {self.title}"

        for key, item in self.attributes:
            string += f" {key}={item}"

        return string
