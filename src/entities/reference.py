from dataclasses import dataclass, field
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
    extra: dict[str, str] = field(default_factory=dict)

    def get(self, attribute: str, default: Optional[str] = None) -> Optional[str]:
        return self.extra.get(attribute, default)

    def __str__(self) -> str:
        string = f"{self.citation_key}: {self.year}, {self.author}, {self.title}"

        for key, item in self.extra.items():
            string += f" {key}={item}"

        return string


@dataclass
class InputReference:
    """Input reference entity for creating/updating references with list of authors."""

    citation_key: str
    year: int
    authors: list[str]
    title: str
    reftype: str = RefType.BOOK.value
    extra: dict[str, str] = field(default_factory=dict)
    id: Optional[int] = None
