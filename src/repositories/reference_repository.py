"""Repository module for managing reference data in the database."""

from config import db
from sqlalchemy import text

from entities.reference import Reference
from util import RefField

import json


class ReferenceRepository:

    def get_references(
        self, order_by: RefField = RefField.CITATION_KEY
    ) -> list[Reference]:
        """Fetches all references from the database."""
        sql = text(
            f"""
                SELECT 
                    id, 
                    {RefField.CITATION_KEY.value},
                    {RefField.YEAR.value},
                    {RefField.AUTHOR.value},
                    {RefField.TITLE.value},
                    {RefField.REFTYPE.value},
                    {RefField.EXTRA.value}
                FROM references_view
                ORDER BY {order_by.value}
                """
        )

        result = db.session.execute(sql)
        rows = result.fetchall()

        # jsonb is automagically converted to a python
        # object so we don't have to call json.loads.
        return [
            Reference(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
            for row in rows
        ]

    def get_reference_by_id(self, id: int) -> Reference:
        """Fetches a single reference by its ID."""
        sql = text(
            f"""
                SELECT 
                    id, 
                    {RefField.CITATION_KEY.value},
                    {RefField.YEAR.value},
                    {RefField.AUTHOR.value},
                    {RefField.TITLE.value},
                    {RefField.REFTYPE.value},
                    {RefField.EXTRA.value}
                FROM references_view
                WHERE id = :id
                """
        )

        result = db.session.execute(sql, {"id": id})
        row = result.fetchone()

        if row is None:
            return None

        return Reference(row[0], row[1], row[2], row[3], row[4], row[5], row[6])

    def get_reference_by_citation_key(self, citation_key: str) -> Reference:
        """Fetches a single reference by its citation key."""
        sql = text(
            f"""
                SELECT 
                    id, 
                    {RefField.CITATION_KEY.value},
                    {RefField.YEAR.value},
                    {RefField.AUTHOR.value},
                    {RefField.TITLE.value},
                    {RefField.REFTYPE.value},
                    {RefField.EXTRA.value}
                FROM references_view
                WHERE {RefField.CITATION_KEY.value} = :{RefField.CITATION_KEY.value}
                """
        )

        result = db.session.execute(sql, {RefField.CITATION_KEY.value: citation_key})
        row = result.fetchone()

        if row is None:
            return None

        return Reference(row[0], row[1], row[2], row[3], row[4], row[5], row[6])

    def create_reference(
        self,
        citation_key: str,
        year: int,
        authors: list[str],
        title: str,
        reftype: str,
        extra: dict[str, str] = {},
    ):
        """Creates a new reference in the database."""
        # Step 1: Insert or get author IDs
        author_ids = []
        for author in authors:
            author_name = author.strip()
            if not author_name:
                continue

            # Try to insert author, or get existing ID
            insert_author_sql = text(
                """
                INSERT INTO authors (name)
                VALUES (:name)
                ON CONFLICT (name) DO NOTHING
                """
            )
            db.session.execute(insert_author_sql, {"name": author_name})

            # Get the author ID
            get_author_id_sql = text(
                """
                SELECT id FROM authors WHERE name = :name
                """
            )
            result = db.session.execute(get_author_id_sql, {"name": author_name})
            author_id = result.fetchone()[0]
            author_ids.append(author_id)

        # Step 2: Insert reference into reference_values
        sql = text(
            f"""
            INSERT INTO reference_values ( 
            {RefField.CITATION_KEY.value},
            {RefField.YEAR.value},
            {RefField.TITLE.value},
            {RefField.REFTYPE.value},
            {RefField.EXTRA.value})
            VALUES (:{RefField.CITATION_KEY.value}, :{RefField.YEAR.value}, :{RefField.TITLE.value}, :{RefField.REFTYPE.value}, :{RefField.EXTRA.value})
            RETURNING id
            """
        )
        result = db.session.execute(
            sql,
            {
                RefField.CITATION_KEY.value: citation_key,
                RefField.YEAR.value: year,
                RefField.TITLE.value: title,
                RefField.REFTYPE.value: reftype,
                RefField.EXTRA.value: json.dumps(extra),
            },
        )
        reference_id = result.fetchone()[0]

        # Step 3: Insert mappings into reference_authors
        for order, author_id in enumerate(author_ids):
            insert_mapping_sql = text(
                """
                INSERT INTO reference_authors (reference_id, author_id, author_order)
                VALUES (:reference_id, :author_id, :author_order)
                """
            )
            db.session.execute(
                insert_mapping_sql,
                {
                    "reference_id": reference_id,
                    "author_id": author_id,
                    "author_order": order,
                },
            )

        db.session.commit()
        return reference_id

    def get_citation_keys(self) -> list[str]:
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

    def citation_key_exists(self, citation_key: str) -> bool:
        """Checks if a citation key exists in the database."""
        sql = text(
            f"""
            SELECT 1
            FROM reference_values
            WHERE {RefField.CITATION_KEY.value} = :{RefField.CITATION_KEY.value}
            """
        )
        result = db.session.execute(sql, {RefField.CITATION_KEY.value: citation_key})
        return result.first() is not None

    def delete_reference(self, citation_key: str):
        """Deletes a reference from the database."""
        sql = text(
            f"""
            DELETE FROM reference_values
            WHERE {RefField.CITATION_KEY.value} = :{RefField.CITATION_KEY.value}
            """
        )
        db.session.execute(sql, {RefField.CITATION_KEY.value: citation_key})
        db.session.commit()

    def update_reference(
        self,
        id: int,
        citation_key: str,
        year: int = None,
        authors: list[str] = None,
        title: str = None,
        reftype: str = None,
        extra: dict[str, str] = None,
    ):
        """Updates only fields that are not None."""

        updates = {}
        if citation_key is not None:
            updates["citation_key"] = citation_key
        if year is not None:
            updates["year"] = year
        if title is not None:
            updates["title"] = title
        if reftype is not None:
            updates["reftype"] = reftype
        if extra is not None:
            updates["extra"] = json.dumps(extra)

        # Update reference_values table if there are any updates
        if updates:
            field_mapping = {
                "citation_key": RefField.CITATION_KEY.value,
                "year": RefField.YEAR.value,
                "title": RefField.TITLE.value,
                "reftype": RefField.REFTYPE.value,
                "extra": RefField.EXTRA.value,
            }
            set_clause = ", ".join(
                [
                    f"{field_mapping[field]} = :{field}"
                    for field in updates.keys()
                    if field in field_mapping
                ]
            )

            sql = text(
                f"""
                UPDATE reference_values
                SET {set_clause}
                WHERE id = :id
            """
            )

            updates["id"] = id
            db.session.execute(sql, updates)

        # Handle author updates
        if authors is not None:
            # Step 1: Delete old author mappings
            delete_mappings_sql = text(
                """
                DELETE FROM reference_authors
                WHERE reference_id = :reference_id
                """
            )
            db.session.execute(delete_mappings_sql, {"reference_id": id})

            # Step 2: Insert or get author IDs
            author_ids = []
            for author in authors:
                author_name = author.strip()
                if not author_name:
                    continue

                # Try to insert author, or get existing ID
                insert_author_sql = text(
                    """
                    INSERT INTO authors (name)
                    VALUES (:name)
                    ON CONFLICT (name) DO NOTHING
                    """
                )
                db.session.execute(insert_author_sql, {"name": author_name})

                # Get the author ID
                get_author_id_sql = text(
                    """
                    SELECT id FROM authors WHERE name = :name
                    """
                )
                result = db.session.execute(get_author_id_sql, {"name": author_name})
                author_id = result.fetchone()[0]
                author_ids.append(author_id)

            # Step 3: Insert new mappings into reference_authors
            for order, author_id in enumerate(author_ids):
                insert_mapping_sql = text(
                    """
                    INSERT INTO reference_authors (reference_id, author_id, author_order)
                    VALUES (:reference_id, :author_id, :author_order)
                    """
                )
                db.session.execute(
                    insert_mapping_sql,
                    {
                        "reference_id": id,
                        "author_id": author_id,
                        "author_order": order,
                    },
                )

        db.session.commit()
