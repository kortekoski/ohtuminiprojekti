"""Database helper functions for setting up and managing the database."""

import os
from sqlalchemy import text
from config import db, app


def reset_db():
    """ "Clears all contents from the database tables for testing purposes"""
    print("Clearing contents from tables")
    # Delete in correct order due to foreign key constraints
    sql1 = text("DELETE FROM reference_authors")
    sql2 = text("DELETE FROM reference_values")
    sql3 = text("DELETE FROM authors")
    db.session.execute(sql1)
    db.session.execute(sql2)
    db.session.execute(sql3)
    db.session.commit()


def tables():
    """Returns all table names from the database except those ending with _id_seq"""
    sql = text(
        "SELECT table_name "
        "FROM information_schema.tables "
        "WHERE table_schema = 'public' "
        "AND table_type = 'BASE TABLE' "
        "AND table_name NOT LIKE '%_id_seq'"
    )

    result = db.session.execute(sql)
    return [row[0] for row in result.fetchall()]


def views():
    """Returns all view names from the database"""
    sql = text(
        "SELECT table_name "
        "FROM information_schema.views "
        "WHERE table_schema = 'public'"
    )

    result = db.session.execute(sql)
    return [row[0] for row in result.fetchall()]


def setup_db():
    """
    Creating the database
    If database tables already exist, those are dropped before the creation
    """
    # Drop views first
    views_in_db = views()
    if len(views_in_db) > 0:
        print(f"Views exist, dropping: {', '.join(views_in_db)}")
        for view in views_in_db:
            sql = text(f"DROP VIEW IF EXISTS {view} CASCADE")
            db.session.execute(sql)
        db.session.commit()

    # Then drop tables
    tables_in_db = tables()
    if len(tables_in_db) > 0:
        print(f"Tables exist, dropping: {', '.join(tables_in_db)}")
        # Drop tables with CASCADE to handle foreign key dependencies
        for table in tables_in_db:
            sql = text(f"DROP TABLE {table} CASCADE")
            db.session.execute(sql)
        db.session.commit()

    print("Creating database")

    base_path = os.path.dirname(os.path.dirname(__file__))
    schema_path = os.path.join(base_path, "migrations", "01-schema.sql")
    with open(schema_path, "r") as f:
        schema_sql = f.read().strip()

    sql = text(schema_sql)
    db.session.execute(sql)
    db.session.commit()

    # ----------------------------------------------------------------------
    # Reset all sequences (like AUTO_INCREMENT reset to 1)
    # ----------------------------------------------------------------------
    sequences = [
        "reference_values_id_seq",
        # If you add more tables with SERIAL fields, add them here:
        # "some_other_table_id_seq",
    ]

    for seq in sequences:
        try:
            print(f"Resetting sequence {seq}")
            db.session.execute(text(f"ALTER SEQUENCE {seq} RESTART WITH 1"))
        except Exception as e:
            print(f"Could not reset sequence {seq}: {e}")


if __name__ == "__main__":
    with app.app_context():
        setup_db()
