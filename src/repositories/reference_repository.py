from config import db
from sqlalchemy import text

from entities.reference import Reference
from util import RefField


def get_references():
    """Fetches all references from the database."""
    sql = text(
        f"""
               SELECT id, 
               {RefField.YEAR.value},
               {RefField.AUTHOR.value},
               {RefField.TITLE.value},
               {RefField.REFTYPE.value}
               FROM reference_values
               """
    )
    result = db.session.execute(sql)
    rows = result.fetchall()
    return [Reference(row[0], row[1], row[2], row[3], row[4]) for row in rows]


def create_reference(year, author, title, reftype):
    """Creates a new reference in the database."""
    sql = text(
        f"""
        INSERT INTO reference_values ( 
        {RefField.YEAR.value},
        {RefField.AUTHOR.value},
        {RefField.TITLE.value},
        {RefField.REFTYPE.value})
        VALUES (:year, :author, :title, :reftype)
        """
    )
    db.session.execute(
        sql,
        {
            RefField.YEAR.value: year,
            RefField.AUTHOR.value: author,
            RefField.TITLE.value: title,
            RefField.REFTYPE.value: reftype,
        },
    )
    db.session.commit()


def get_reference_by_id(reference_id):
    """Fetches a reference by its ID."""
    sql = text(
        f"""
        SELECT id, 
        {RefField.YEAR.value}, 
        {RefField.AUTHOR.value}, 
        {RefField.TITLE.value}, 
        {RefField.REFTYPE.value}
        FROM reference_values
        WHERE id = :id
    """
    )
    row = db.session.execute(sql, {"id": reference_id}).fetchone()

    if row:
        return Reference(row[0], row[1], row[2], row[3], row[4])

    return None
