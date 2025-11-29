from repositories.reference_repository import ReferenceRepository
from util import RefType, RefField, RefAttribute
from collections import namedtuple


class TemplateSchemaElem:
    def __init__(self, attribute: RefAttribute, required: bool):
        self.attribute = attribute
        self.required = required


elem = TemplateSchemaElem


class TemplateService:
    @staticmethod
    def relevant_attributes(reftype: RefType) -> list[TemplateSchemaElem]:
        if reftype == RefType.BOOK:
            return [
                elem(RefAttribute.AUTHOR, True),
                elem(RefAttribute.YEAR, True),
                elem(RefAttribute.PUBLISHER, True),
                elem(RefAttribute.EPRINT, False),
                elem(RefAttribute.BOOKTITLE, False),
                elem(RefAttribute.EDITOR, False),
                elem(RefAttribute.TITLE, True),
                elem(RefAttribute.SUBTITLE, False),
                elem(RefAttribute.SERIES, False),
                elem(RefAttribute.LOCATION, False),
                elem(RefAttribute.ADDRESS, False),
                elem(RefAttribute.LANGUAGE, False),
                elem(RefAttribute.ORIGLANGUAGE, False),
                elem(RefAttribute.TRANSLATOR, False),
                elem(RefAttribute.VOLUME, False),
                elem(RefAttribute.PART, False),
                elem(RefAttribute.EDITION, False),
                elem(RefAttribute.CHAPTER, False),
                elem(RefAttribute.PAGES, False),
                elem(RefAttribute.DATE, False),
            ]
        elif reftype == RefType.ARTICLE:
            return [
                elem(RefAttribute.TITLE, True),
                elem(RefAttribute.AUTHOR, True),
                elem(RefAttribute.DOI, False),
                elem(RefAttribute.YEAR, True),
                elem(RefAttribute.JOURNALTITLE, True),
                elem(RefAttribute.ISSUETITLE, True),
                elem(RefAttribute.ABSTRACT, False),
                elem(RefAttribute.SUBTITLE, False),
                elem(RefAttribute.LANGUAGE, False),
                elem(RefAttribute.ORIGLANGUAGE, False),
                elem(RefAttribute.TRANSLATOR, False),
                elem(RefAttribute.PAGES, False),
            ]
        else:
            return [elem(RefAttribute.AUTHOR, True)]
