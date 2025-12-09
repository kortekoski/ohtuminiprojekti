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
