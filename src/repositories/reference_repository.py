from config import db
from sqlalchemy import text

from entities.reference import Reference


def get_references():
    sql = text("SELECT id, year, author, title, reftype FROM reference_values")
    result = db.session.execute(sql)
    rows = result.fetchall()
    return [Reference(row[0], row[1], row[2], row[3], row[4]) for row in rows]


def create_reference(year, author, title, reftype):
    sql = text(
        """
        INSERT INTO reference_values (year, author, title, reftype)
        VALUES (:year, :author, :title, :reftype)
    """
    )
    db.session.execute(
        sql, {"year": year, "author": author, "title": title, "reftype": reftype}
    )
    db.session.commit()


def get_reference_by_id(reference_id):
    sql = text(
        """
        SELECT id, year, author, title, reftype
        FROM reference_values
        WHERE id = :id
    """
    )
    row = db.session.execute(sql, {"id": reference_id}).fetchone()

    if row:
        return Reference(row[0], row[1], row[2], row[3], row[4])

    return None
