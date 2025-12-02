from urllib.parse import urlparse
import requests as re
from util import UserInputError
import re
from entities.reference import Reference, RefType


class ApiService:
    def __init__(self, api_proxy: type | None = None):
        if api_proxy:
            self.api = api_proxy
        else:
            self.api = CrossrefApi()

    @staticmethod
    def _validate_doi(maybe_doi: str) -> bool:
        parts = maybe_doi.split("/")
        try:
            int_parts = list(map(int, parts))
        except ValueError:
            return False

        if len(int_parts) != 2:
            return False

        if int_parts[0] != 10:
            return False

        return True

    @staticmethod
    def _grab_doi_from_url(maybe_valid: str) -> str | None:
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
        doi = maybe_doiable
        if url_validator(maybe_doiable):
            doi = ApiService._grab_doi_from_url(maybe_doiable)
            if doi is None:
                return None

        if ApiService._validate_doi(doi):
            return doi

        return None

    @staticmethod
    def _make_reference(content: dict[str, dict[str, dict]]) -> Reference | None:
        status = content.get("status")
        if status != "ok":
            return None

        message_type = content.get("message_type")
        if message_type != "work":
            raise UserInputError("The content the DOI points to is not for a work.")

        message = content.get("message")
        if message is None:
            return None

        work_type = RefType.ARTICLE
        content_type = message.get("type")
        if content_type != "journal_article":
            raise UserInputError(
                "Only works of type or 'Article' are supported by DOI."
            )

        # The field `published` looks something like
        # 'published': {'date-parts':[[2020, 8, 17]]}
        work_date = message["published"]["date-parts"][0]
        work_year = work_date[0]
        work_month = work_date[1]

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

        work_publisher = message["publisher"][0]

        work_journal = message["container-title"][0]

        work_volume = message["volume"]

        work_issue = message["issue"]

        work_language = message["language"]
        if work_language == "en":
            work_language = "English"

        extra = {
            "month": work_month,
            "issn": work_issn,
            "publisher": work_publisher,
            "journal": work_journal,
            "volume": work_volume,
            "issue": work_issue,
        }


class CrossrefApi:
    def __init__(self):
        self.base_url = "https://api.crossref.org/works"
        self.cache: dict[str, dict] = dict()

    def get_doi_metadata(self, doi: str) -> dict | None:
        url = self.base_url + "/doi/"
        response = re.get(url + doi, allow_redirects=True)
        if response.status_code == 403:
            return None

        if response.status_code == 404:
            raise UserInputError(f"DOI doi:{doi} does not exist.")

        return response.json()


def url_validator(url: str) -> bool:
    try:
        parsed_url = urlparse(url)
        return all([parsed_url.scheme, parsed_url.netloc, parsed_url.path])
    except:
        return False
