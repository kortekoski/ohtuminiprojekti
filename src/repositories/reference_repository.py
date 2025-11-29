"""Repository module for managing reference data in the database."""

from config import db
from sqlalchemy import text

from entities.reference import Reference
from util import RefField


class ReferenceRepository:

    def get_references(self, order_by: RefField = None) -> list[Reference]:
        """Fetches all references from the database."""
        sql = text(
            f"""
                SELECT id, 
                {RefField.CITATION_KEY.value},
                {RefField.YEAR.value},
                {RefField.AUTHOR.value},
                {RefField.TITLE.value},
                {RefField.REFTYPE.value}
                FROM reference_values
                ORDER BY {order_by.value
                            if order_by
                            else RefField.CITATION_KEY.value}
                """
        )
        result = db.session.execute(sql)
        rows = result.fetchall()
        return [
            Reference(row[0], row[1], row[2], row[3], row[4], row[5]) for row in rows
        ]

    def create_reference(self, citation_key, year, author, title, reftype):
        """Creates a new reference in the database."""
        sql = text(
            f"""
            INSERT INTO reference_values ( 
            {RefField.CITATION_KEY.value},
            {RefField.YEAR.value},
            {RefField.AUTHOR.value},
            {RefField.TITLE.value},
            {RefField.REFTYPE.value})
            VALUES (:citation_key, :year, :author, :title, :reftype)
            """
        )
        db.session.execute(
            sql,
            {
                RefField.CITATION_KEY.value: citation_key,
                RefField.YEAR.value: year,
                RefField.AUTHOR.value: author,
                RefField.TITLE.value: title,
                RefField.REFTYPE.value: reftype,
            },
        )
        db.session.commit()


def citation_key_exists(citation_key: str) -> bool:
    """Checks if a citation key exists in the database."""
    sql = text(
        f"""
        SELECT 1
        FROM reference_values
        WHERE {RefField.CITATION_KEY.value} = :citation_key
        """
    )
    result = db.session.execute(sql, {RefField.CITATION_KEY.value: citation_key})
    return result.first() is not None


def get_citation_keys() -> list[str]:
    """Fetches all citation keys from the database."""
    sql = text(
        f"""
        SELECT {RefField.CITATION_KEY.value}
        FROM reference_values
        """
    )
    result = db.session.execute(sql)
    rows = result.fetchall()
    return [row[0] for row in rows]
