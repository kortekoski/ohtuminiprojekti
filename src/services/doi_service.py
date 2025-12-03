"""Service for handling DOI input."""

from urllib.parse import urlparse
import requests
from util import UserInputError
import re
from entities.reference import Reference, RefType


class DoiService:
    """Container for methods for getting and handling DOIs."""

    def __init__(self, api_proxy: type | None = None):
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
        work_month = int(work_date[1])

        work_title = message["title"]

        # This never happens but shuts up the LSP.
        work_title = work_title if isinstance(work_title, str) else ""

        # Titles sometimes have html formatting tags...
        work_title = re.sub("<[^<]+?>", "", work_title)

        # ... and newlines...
        work_title = work_title.replace("\n", "")

        # ... and extra spaces.
        work_title = re.sub(" +", " ", work_title)

        work_issn = message["ISSN"][0]

        work_publisher = message["publisher"]

        work_journal = message["container-title"][0]

        work_volume = message["volume"]

        work_issue = message["issue"]

        work_doi = message["DOI"]

        work_language = message["language"]
        if work_language == "en":
            work_language = "English"

        work_author = " and ".join(
            map(lambda a: f"{a['given']} {a['family']}", message["author"])
        )

        extra = {
            "month": work_month,
            "issn": work_issn,
            "publisher": work_publisher,
            "journal": work_journal,
            "volume": work_volume,
            "issue": work_issue,
            "doi": work_doi,
        }

        return Reference(
            0, "placeholder", work_year, work_author, work_title, RefType.ARTICLE, extra
        )


class CrossrefApi:
    """Crossref API wrapper."""

    def __init__(self):
        self.base_url = "https://api.crossref.org/works"

    def get_doi_metadata(self, doi: str) -> dict | None:
        """Get metadata for a DOI string."""
        url = self.base_url + "/doi/"
        response = requests.get(url + doi, allow_redirects=True)
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
