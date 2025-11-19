from entities.reference import Reference
from flask.json.provider import DefaultJSONProvider


def _default(item):
    if isinstance(item, Reference):
        return {
            "id": item.id,
            "year": item.year,
            "author": item.author,
            "title": item.title,
            "type": item.type,
        }
    else:
        return DefaultJSONProvider.default(item)


def _loads(item):
    if isinstance(item, dict):
        try:
            ref = Reference(
                item["id"],
                item["year"],
                item["author"],
                item["title"],
                item["type"]
            )
            return ref
        except:
            return {
                _loads(key): _loads(value)
                for key, value in item.items()
            }

    if isinstance(item, list):
        return [_loads(value) for value in item]

    return item


class CustomJSONProvider(DefaultJSONProvider):
    default = staticmethod(_default)

    def loads(self, s, **kwargs):
        data = super().loads(s, **kwargs)
        parsed_data = _loads(data)
        return parsed_data
