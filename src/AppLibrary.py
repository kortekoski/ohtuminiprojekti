import requests
from repositories.reference_repository import create_reference

class AppLibrary:

    def __init__(self):
        self._base_url = "http://localhost:5001"

    def add_test_reference(self, year=2025, author="Guybrush Threepwood", title="Different types of clover in Melee island", reftype="book"):
        data = {
            "year": year,
            "author": author,
            "title": title,
            "reftype": reftype
        }
        
        requests.post(f"{self._base_url}/add_test_reference", data=data)