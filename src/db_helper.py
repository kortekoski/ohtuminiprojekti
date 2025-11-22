"""Database helper functions for setting up and managing the database."""
import os
from sqlalchemy import text
from config import db, app


def reset_db():
    """ "Clears all contents from the database table reference_values for testing purposes"""
    print("Clearing contents from table reference_values")
    sql = text("DELETE FROM reference_values")
    db.session.execute(sql)
    db.session.commit()


def tables():
    """Returns all table names from the database except those ending with _id_seq"""
    sql = text(
        "SELECT table_name "
        "FROM information_schema.tables "
        "WHERE table_schema = 'public' "
        "AND table_name NOT LIKE '%_id_seq'"
    )

    result = db.session.execute(sql)
    return [row[0] for row in result.fetchall()]


def setup_db():
    """
    Creating the database
    If database tables already exist, those are dropped before the creation
    """
    tables_in_db = tables()
    if len(tables_in_db) > 0:
        print(f"Tables exist, dropping: {', '.join(tables_in_db)}")
        for table in tables_in_db:
            sql = text(f"DROP TABLE {table}")
            db.session.execute(sql)
        db.session.commit()

    print("Creating database")

    # Read schema from schema.sql file
    base_path = os.path.dirname(os.path.dirname(__file__))
    schema_path = os.path.join(base_path, "migrations", "01-schema.sql")
    with open(schema_path, "r") as f:
        schema_sql = f.read().strip()

    sql = text(schema_sql)
    db.session.execute(sql)
    db.session.commit()


if __name__ == "__main__":
    with app.app_context():
        setup_db()
