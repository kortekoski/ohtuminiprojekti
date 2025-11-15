from config import db
from sqlalchemy import text

from entities.reference import Reference

def get_references():
    sql = text("SELECT id, year, author, title FROM reference_values")
    result = db.session.execute(sql)
    rows = result.fetchall()
    return [Reference(row[0], row[1], row[2], row[3]) for row in rows]

def create_reference(year, author, title):
    sql = text("""
        INSERT INTO reference_values (year, author, title)
        VALUES (:year, :author, :title)
    """)
    db.session.execute(sql, {
        "year": year,
        "author": author,
        "title": title
    })
    db.session.commit()

def get_reference_by_id(reference_id):
    sql = text("""
        SELECT id, year, author, title
        FROM reference_values
        WHERE id = :id
    """)
    row = db.session.execute(sql, {"id": reference_id}).fetchone()

    if row:
        return Reference(row[0], row[1], row[2], row[3])

    return None
