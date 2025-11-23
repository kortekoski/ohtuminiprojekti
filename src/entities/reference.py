from util import RefType


class Reference:
    def __init__(self, id, year, author, title, reftype=RefType.BOOK):
        """Reference entity representing a bibliographic reference."""
        self.id = id
        self.year = year
        self.author = author
        self.title = title
        self.reftype = reftype

    def __str__(self):
        return f"{self.year}, {self.author}, {self.title}"
