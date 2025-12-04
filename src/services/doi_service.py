"""Service for handling DOI input."""

from urllib.parse import urlparse
import requests
from util import UserInputError
import re
from entities.reference import Reference, RefType


class DoiService:
    """Container for methods for getting and handling DOIs."""

    def __init__(self, api_proxy=None):
        if api_proxy:
            self.api = api_proxy
        else:
            self.api = CrossrefApi()

    def get_doi(self, input_string: str) -> Reference | None:
        """
        Get a DOI from an input string with either a URL
        that contains a DOI or a DOI.
        """
        if doi := DoiService._validate_input(input_string):
            if content := self.api.get_doi_metadata(doi):
                return DoiService._make_reference(content)

    @staticmethod
    def _validate_doi(maybe_doi: str) -> bool:
        """
        Validate that the input string is a DOI and that it
        has a prefix that we support.
        """
        parts = maybe_doi.split("/")
        if len(parts) != 2:
            return False
        prefix = parts[0]

        try:
            prefix_start = prefix.split(".")[0]
            prefix_start = int(prefix_start)
            if prefix_start != 10:
                raise UserInputError(
                    f"The prefix of DOI doi:{maybe_doi} is unsupported."
                )
        except ValueError:
            return False

        return True

    @staticmethod
    def _grab_doi_from_url(maybe_valid: str) -> str | None:
        """
        Grab and return a DOI from an input string:
        _grab_doi_from_url("https://example.com/doi/10.221/test") -> "10.221/test"
        """
        url_parts = iter(maybe_valid.split("/"))
        doi = None

        for part in url_parts:
            if part == "doi":
                doi_prefix = next(url_parts, "")
                doi_suffix = next(url_parts, "")
                doi = doi_prefix + "/" + doi_suffix
                break

        return doi

    @staticmethod
    def _validate_input(maybe_doiable: str) -> str | None:
        """
        Validates input and returns the DOI contained within.
        """
        doi = maybe_doiable
        if url_validator(maybe_doiable):
            doi = DoiService._grab_doi_from_url(maybe_doiable)
            if doi is None:
                raise UserInputError(
                    "Input seems to be a URL that does not contain a DOI."
                )

        if DoiService._validate_doi(doi):
            return doi

        raise UserInputError("Input must be a DOI or a URL that contains a DOI.")

    @staticmethod
    def _make_reference(content: dict) -> Reference | None:
        """
        Make a Reference object from a crossref response python object
        """
        status = content.get("status")
        if status != "ok":
            raise UserInputError("Can't find DOI.")

        message_type = content.get("message-type")
        if message_type != "work":
            raise UserInputError("The content the DOI points to is not for a work.")

        message = content.get("message")
        if message is None:
            return

        # work_type = RefType.ARTICLE
        content_type = message.get("type")
        if content_type != "journal-article":
            raise UserInputError("Only works of type or 'Article' are supported.")

        # The field `published` looks something like
        # 'published': {'date-parts':[[2020, 8, 17]]}
        work_date = message["published"]["date-parts"][0]
        work_year = int(work_date[0])
        work_month = work_date[1]
        extra = {"month": work_month}

        work_title = message["title"][0]

        # This never happens but shuts up the LSP.
        work_title = work_title if isinstance(work_title, str) else ""

        # Titles sometimes have html formatting tags...
        work_title = re.sub("<[^<]+?>", "", work_title)

        # ... and newlines...
        work_title = work_title.replace("\n", "")

        # ... and extra spaces.
        work_title = re.sub(" +", " ", work_title)
        if work_issn := message["ISSN"][0]:
            extra["issn"] = work_issn

        if work_publisher := message.get("publisher"):
            extra["publisher"] = work_publisher

        if work_journal := message.get("container-title")[0]:
            extra["journal"] = work_journal

        if work_volume := message.get("volume"):
            extra["volume"] = work_volume

        if work_issue := message.get("issue"):
            extra["issue"] = work_issue

        if work_doi := message.get("DOI"):
            extra["doi"] = work_doi

        if work_language := message.get("language"):
            if work_language == "en":
                work_language = "English"
            extra["language"] = work_language

        work_author = " and ".join(
            map(lambda a: f"{a['given']} {a['family']}", message["author"])
        )

        return Reference(
            0,
            "placeholder",
            work_year,
            work_author,
            work_title,
            RefType.ARTICLE.value,
            extra,
        )


class CrossrefApi:
    """Crossref API wrapper."""

    def __init__(self):
        self.base_url = "https://api.crossref.org/works"

    def get_doi_metadata(self, doi: str) -> dict | None:
        """Get metadata for a DOI string."""
        url = self.base_url + "/doi/"
        response = requests.get(url + doi, allow_redirects=True, timeout=5)
        if response.status_code == 403:
            raise UserInputError("Too many requests. Try again in a moment.")

        if response.status_code == 404:
            raise UserInputError(f"DOI doi:{doi} does not exist.")

        return response.json()


def url_validator(url: str) -> bool:
    """Return True iff url is a proper url."""
    try:
        parsed_url = urlparse(url)
        return all([parsed_url.scheme, parsed_url.netloc, parsed_url.path])
    except:
        return False


class TestApi:
    """Mock API for testing."""

    def __init__(self):
        self.real_api = CrossrefApi()

    def get_doi_metadata(self, doi: str) -> dict | None:
        """Return test metadata if request fails."""
        try:
            result = self.real_api.get_doi_metadata(doi)
            if result:
                return result
        except Exception:
            print(
                f"Warning: failed to get metadata from api.crossref.org. Falling back to test data."
            )
            result = {
                "status": "ok",
                "message-type": "work",
                "message": {
                    "type": "journal-article",
                    "published": {"date-parts": [["2020", "1", "1"]]},
                    "title": ["Test title"],
                    "ISSN": ["issn00000000"],
                    "container-title": ["Journal title"],
                    "volume": "1",
                    "issue": "1",
                    "DOI": "10.221/test",
                    "language": "en",
                    "author": [
                        {"given": "Jane", "family": "Doe"},
                        {"given": "Jane", "family": "Doe"},
                    ],
                    "publisher": "AAA",
                },
            }

            return result
