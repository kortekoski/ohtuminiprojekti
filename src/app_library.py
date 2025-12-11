import requests
from util import RefField


class app_library:
    def __init__(self):
        """Initialize the AppLibrary with the base URL of the application."""
        self._base_url = "http://localhost:5001"

    def add_test_reference(
        self,
        citation_key="Test2025",
        year=2025,
        authors=["Threeplog, Guybroom"],
        title="Different types of clover in Melee island",
        reftype="book",
        extra={
            "editor": "",
            "volume": "",
            "number": "",
            "series": "",
            "address": "Boston, MA",
            "edition": "1",
            "month": "08",
            "note": "A classic adventure game reference",
            "isbn": "978-0132350884",
            "publisher": "LocusArts",
            "url": "",
            "doi": "",
        },
    ):
        # Send each author as a separate 'author' field
        data = {
            RefField.CITATION_KEY.value: citation_key,
            RefField.YEAR.value: year,
            RefField.TITLE.value: title,
            RefField.REFTYPE.value: reftype,
        }

        # Add multiple author fields (Flask will receive as list via getlist)
        data_with_authors = []
        for key, value in data.items():
            data_with_authors.append((key, value))
        for author in authors:
            data_with_authors.append(("author", author))
        # Add extra fields individually
        for key, value in extra.items():
            if value:  # Only add non-empty values
                data_with_authors.append((key, value))

        requests.post(f"{self._base_url}/add_test_reference", data=data_with_authors)

    def add_multiple_test_references(self, count=3):
        """Add multiple test references with different citation keys."""
        references = [
            {
                "citation_key": "Smith2020",
                "year": 2020,
                "authors": ["Smith, John", "Doe, Jane"],
                "title": "Introduction to Software Testing",
                "reftype": "book",
                "extra": {
                    "publisher": "Tech Press",
                    "address": "New York, NY",
                    "edition": "2",
                    "isbn": "978-0123456789",
                },
            },
            {
                "citation_key": "Johnson2021",
                "year": 2021,
                "authors": ["Johnson, Alice"],
                "title": "Advanced Database Systems",
                "reftype": "article",
                "extra": {
                    "journal": "Journal of Database Research",
                    "volume": "15",
                    "number": "3",
                    "pages": "123-145",
                },
            },
            {
                "citation_key": "Brown2022",
                "year": 2022,
                "authors": ["Brown, Robert", "Wilson, Emily"],
                "title": "Machine Learning in Practice",
                "reftype": "article",
                "extra": {
                    "booktitle": "Proceedings of ML Conference 2022",
                    "pages": "45-52",
                    "address": "San Francisco, CA",
                },
            },
            {
                "citation_key": "Davis2023",
                "year": 2023,
                "authors": ["Davis, Michael"],
                "title": "Cloud Computing Architecture",
                "reftype": "book",
                "extra": {
                    "publisher": "Cloud Press",
                    "edition": "1",
                    "isbn": "978-9876543210",
                },
            },
            {
                "citation_key": "Taylor2024",
                "year": 2024,
                "authors": ["Taylor, Sarah", "Anderson, Chris"],
                "title": "Web Development Best Practices",
                "reftype": "article",
                "extra": {
                    "journal": "Web Engineering Journal",
                    "volume": "8",
                    "number": "2",
                },
            },
        ]

        for i in range(min(count, len(references))):
            ref = references[i]
            self.add_test_reference(**ref)
