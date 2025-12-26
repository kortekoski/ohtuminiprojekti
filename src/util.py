"""Utility helper functions."""

from enum import Enum, auto


class RefField(str, Enum):
    """Enumeration for reference fields."""

    CITATION_KEY = "citation_key"
    YEAR = "year"
    AUTHOR = "author"
    TITLE = "title"
    REFTYPE = "reftype"
    EXTRA = "extra"


class RefType(str, Enum):
    """Enumeration for reference types."""

    ARTICLE = "article"
    BOOK = "book"
    BOOKLET = "booklet"
    CONFERENCE = "conference"
    INBOOK = "inbook"
    INCOLLECTION = "incollection"
    INPROCEEDINGS = "inproceedings"
    MANUAL = "manual"
    MASTERSTHESIS = "mastersthesis"
    MISC = "misc"
    PHDTHESIS = "phdthesis"
    PROCEEDINGS = "proceedings"
    TECHREPORT = "techreport"
    UNPUBLISHED = "unpublished"


class FieldKind(Enum):
    NAME_LIST = "name_list"
    LITERAL = "literal"
    RANGE = "range"
    INTEGER = "integer"
    DATEPART = "datepart"
    DATE = "date"
    VERBATIM = "verbatim"
    URI = "uri"
    SEPARATED_VALUE = "separated_value"
    PATTERN = "pattern"
    KEY = "key"
    CODE = "code"
    IDENTIFIER = "identifier"


class RefAttribute(Enum):
    # ------------------------------
    # Name list fields
    # ------------------------------
    AUTHOR = ("author", "Author(s)", FieldKind.NAME_LIST)
    EDITOR = ("editor", "Editor(s)", FieldKind.NAME_LIST)
    EDITORA = ("editora", "Editor A", FieldKind.NAME_LIST)
    EDITORB = ("editorb", "Editor B", FieldKind.NAME_LIST)
    EDITORC = ("editorc", "Editor C", FieldKind.NAME_LIST)
    TRANSLATOR = ("translator", "Translator(s)", FieldKind.NAME_LIST)
    ANNOTATOR = ("annotator", "Annotator(s)", FieldKind.NAME_LIST)
    COMMENTATOR = ("commentator", "Commentator(s)", FieldKind.NAME_LIST)
    INTRODUCER = ("introducer", "Introducer(s)", FieldKind.NAME_LIST)
    AFTERWORD = ("afterword", "Afterword by", FieldKind.NAME_LIST)
    FOREWORD = ("foreword", "Foreword by", FieldKind.NAME_LIST)
    HOLDER = ("holder", "Holder(s)", FieldKind.NAME_LIST)
    SHORTAUTHOR = ("shortauthor", "Short Author", FieldKind.NAME_LIST)
    SHORTEDITOR = ("shorteditor", "Short Editor", FieldKind.NAME_LIST)
    ENTITLED = ("entitled", "Entitled by", FieldKind.NAME_LIST)
    NAMEA = ("namea", "Name A", FieldKind.NAME_LIST)
    NAMEB = ("nameb", "Name B", FieldKind.NAME_LIST)
    NAMEC = ("namec", "Name C", FieldKind.NAME_LIST)

    # ------------------------------
    # Literal/string fields
    # ------------------------------
    TITLE = ("title", "Title", FieldKind.LITERAL)
    SUBTITLE = ("subtitle", "Subtitle", FieldKind.LITERAL)
    TITLEADDON = ("titleaddon", "Title Addon", FieldKind.LITERAL)
    SHORTTITLE = ("shorttitle", "Short Title", FieldKind.LITERAL)
    SORTTITLE = ("sorttitle", "Sort Title", FieldKind.LITERAL)

    BOOKTITLE = ("booktitle", "Book Title", FieldKind.LITERAL)
    BOOKSUBTITLE = ("booksubtitle", "Book Subtitle", FieldKind.LITERAL)
    BOOKTITLEADDON = ("booktitleaddon", "Book Title Addon", FieldKind.LITERAL)
    MAINTITLE = ("maintitle", "Main Title", FieldKind.LITERAL)
    MAINSUBTITLE = ("mainsubtitle", "Main Subtitle", FieldKind.LITERAL)
    MAINTITLEADDON = ("maintitleaddon", "Main Title Addon", FieldKind.LITERAL)

    EVENTTITLE = ("eventtitle", "Event Title", FieldKind.LITERAL)
    EVENTSUBTITLE = ("eventsubtitle", "Event Subtitle", FieldKind.LITERAL)

    JOURNALTITLE = ("journaltitle", "Journal Title", FieldKind.LITERAL)
    JOURNALSUBTITLE = ("journalsubtitle", "Journal Subtitle", FieldKind.LITERAL)
    JOURNALTITLEADDON = ("journaltitleaddon", "Journal Title Addon", FieldKind.LITERAL)

    ISSUETITLE = ("issuetitle", "Issue Title", FieldKind.LITERAL)
    ISSUESUBTITLE = ("issuesubtitle", "Issue Subtitle", FieldKind.LITERAL)
    ISSUETITLEADDON = ("issuetitleaddon", "Issue Title Addon", FieldKind.LITERAL)

    SERIES = ("series", "Series", FieldKind.LITERAL)
    NUMBER = ("number", "Number", FieldKind.INTEGER)

    ORGANIZATION = ("organization", "Organization", FieldKind.LITERAL)
    INSTITUTION = ("institution", "Institution", FieldKind.LITERAL)
    SCHOOL = ("school", "School", FieldKind.LITERAL)
    PUBLISHER = ("publisher", "Publisher", FieldKind.LITERAL)
    LOCATION = ("location", "Location", FieldKind.LITERAL)
    ADDRESS = ("address", "Address", FieldKind.LITERAL)

    HOWPUBLISHED = ("howpublished", "How Published", FieldKind.LITERAL)
    TYPE = ("type", "Type", FieldKind.LITERAL)
    VERSION = ("version", "Version", FieldKind.LITERAL)

    NOTE = ("note", "Note", FieldKind.LITERAL)
    ADDENDUM = ("addendum", "Addendum", FieldKind.LITERAL)
    ABSTRACT = ("abstract", "Abstract", FieldKind.LITERAL)

    LANGUAGE = ("language", "Language", FieldKind.LITERAL)
    ORIGLANGUAGE = ("origlanguage", "Original Language", FieldKind.LITERAL)

    VENUE = ("venue", "Venue", FieldKind.LITERAL)

    # ------------------------------
    # Integer / numeric fields
    # ------------------------------
    VOLUME = ("volume", "Volume", FieldKind.INTEGER)
    VOLUMES = ("volumes", "Volumes", FieldKind.INTEGER)
    PART = ("part", "Part", FieldKind.INTEGER)
    EDITION = ("edition", "Edition", FieldKind.INTEGER)
    CHAPTER = ("chapter", "Chapter", FieldKind.INTEGER)
    ISSUE = ("issue", "Issue", FieldKind.INTEGER)

    # ------------------------------
    # Ranges
    # ------------------------------
    PAGES = ("pages", "Pages", FieldKind.RANGE)
    PAGETOTAL = ("pagetotal", "Total Pages", FieldKind.INTEGER)

    # ------------------------------
    # Date fields
    # ------------------------------
    DATE = ("date", "Date", FieldKind.DATE)
    YEAR = ("year", "Year", FieldKind.INTEGER)
    MONTH = ("month", "Month", FieldKind.INTEGER)
    EVENTDATE = ("eventdate", "Event Date", FieldKind.DATE)
    ORIGDATE = ("origdate", "Original Date", FieldKind.DATE)
    URLDATE = ("urldate", "Accessed Date", FieldKind.DATE)
    PUBSTATE = ("pubstate", "Publication State", FieldKind.LITERAL)

    # ------------------------------
    # Identifiers
    # ------------------------------
    DOI = ("doi", "DOI", FieldKind.IDENTIFIER)
    EPRINT = ("eprint", "E-Print", FieldKind.IDENTIFIER)
    EPRINTTYPE = ("eprinttype", "E-Print Type", FieldKind.LITERAL)
    EPRINTCLASS = ("eprintclass", "E-Print Class", FieldKind.LITERAL)
    ISBN = ("isbn", "ISBN", FieldKind.IDENTIFIER)
    ISSN = ("issn", "ISSN", FieldKind.IDENTIFIER)
    ISMN = ("ismn", "ISMN", FieldKind.IDENTIFIER)

    # ------------------------------
    # URL fields
    # ------------------------------
    URL = ("url", "URL", FieldKind.URI)
    FILE = ("file", "File", FieldKind.VERBATIM)

    # ------------------------------
    # Misc fields
    # ------------------------------
    KEYWORDS = ("keywords", "Keywords", FieldKind.VERBATIM)
    SORTKEY = ("sortkey", "Sort Key", FieldKind.VERBATIM)
    CROSSREF = ("crossref", "Cross-Reference", FieldKind.LITERAL)
    XREF = ("xref", "Cross-Reference 2", FieldKind.LITERAL)
    ENTRYSET = ("entryset", "Entry Set", FieldKind.LITERAL)
    ENTRYSUBTYPE = ("entrysubtype", "Entry Subtype", FieldKind.LITERAL)


class UserInputError(Exception):
    """Exception raised for errors in the user input."""

    pass


class ValueError(Exception):
    """Exception raised for errors in the value type."""

    pass
