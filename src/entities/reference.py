from dataclasses import dataclass
from util import RefType


@dataclass
class Reference:
    """Reference entity representing a bibliographic reference."""

    id: int
    citation_key: str
    year: int
    author: str
    title: str
    reftype: RefType = RefType.BOOK

    def __str__(self):
        return f"{self.year}, {self.author}, {self.title}"
