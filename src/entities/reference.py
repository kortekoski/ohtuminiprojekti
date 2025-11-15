class Reference:
    def __init__(self, id, year, author, title, type="book"):
        self.id = id
        self.year = year
        self.author = author
        self.title = title
        self.type = type

    def __str__(self):
        return f"{self.year}, {self.author}, {self.title}"
