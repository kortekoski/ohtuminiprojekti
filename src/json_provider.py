from entities.reference import Reference
from flask.json.provider import DefaultJSONProvider


def _default(item):
    if isinstance(item, Reference):
        """Converts a Reference object to a dictionary for JSON serialization."""
        return {
            "id": item.id,
            "citation_key": item.citation_key,
            "year": item.year,
            "author": item.author,
            "title": item.title,
            "reftype": item.reftype,
        }
    else:
        return DefaultJSONProvider.default(item)


def _loads(item):
    if isinstance(item, dict):
        """Attempts to reconstruct a Reference object from a dictionary."""
        try:
            ref = Reference(
                item["id"],
                item["citation_key"],
                item["year"],
                item["author"],
                item["title"],
                item["reftype"],
            )
            return ref
        except:
            return {_loads(key): _loads(value) for key, value in item.items()}

    if isinstance(item, list):
        return [_loads(value) for value in item]

    return item


class CustomJSONProvider(DefaultJSONProvider):
    """Custom JSON provider to handle Reference objects."""

    default = staticmethod(_default)

    def loads(self, s, **kwargs):
        data = super().loads(s, **kwargs)
        parsed_data = _loads(data)
        return parsed_data
