from entities.reference import Reference
from flask.json.provider import DefaultJSONProvider

class CustomJSONProvider(DefaultJSONProvider):
    def default(self, item):
        if isinstance(item, Reference):
            return {
                "id":     item.id,
                "year":   item.year,
                "author": item.author,
                "title":  item.title,
                "type":   item.type
            }
        else:
            return super().default(item)
