"""Repository module for managing reference data in the database."""

from config import db
from sqlalchemy import text

from entities.reference import Reference, InputReference
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

    def create_reference(self, input_ref: InputReference):
        """Creates a new reference in the database."""

        author_ids = self.get_author_ids(input_ref)

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
                RefField.CITATION_KEY.value: input_ref.citation_key,
                RefField.YEAR.value: input_ref.year,
                RefField.TITLE.value: input_ref.title,
                RefField.REFTYPE.value: input_ref.reftype,
                RefField.EXTRA.value: json.dumps(input_ref.extra),
            },
        )
        reference_id = result.fetchone()[0]

        self.insert_into_authors(author_ids, reference_id)

        db.session.commit()
        return reference_id

    def insert_into_authors(self, author_ids: list[int], reference_id: int) -> int:
        for order, author_id in enumerate(author_ids):
            insert_mapping_sql = self.get_insert_mapping_sql()
            db.session.execute(
                insert_mapping_sql,
                {
                    "reference_id": reference_id,
                    "author_id": author_id,
                    "author_order": order,
                },
            )

    def get_insert_mapping_sql(self):
        return text(
            """
                INSERT INTO reference_authors (reference_id, author_id, author_order)
                VALUES (:reference_id, :author_id, :author_order)
                """
        )

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

    def delete_authors(self, id):
        delete_mappings_sql = text(
            """
                DELETE FROM reference_authors
                WHERE reference_id = :reference_id
                """
        )
        db.session.execute(delete_mappings_sql, {"reference_id": id})

    def update_reference(self, input_ref: InputReference):
        """Updates a reference using InputReference entity."""

        updates = {}
        if input_ref.citation_key is not None:
            updates["citation_key"] = input_ref.citation_key
        if input_ref.year is not None:
            updates["year"] = input_ref.year
        if input_ref.title is not None:
            updates["title"] = input_ref.title
        if input_ref.reftype is not None:
            updates["reftype"] = input_ref.reftype
        if input_ref.extra is not None:
            updates["extra"] = json.dumps(input_ref.extra)

        if updates:

            self.update_reference_by_citation_key(input_ref, updates)
            self.handle_authors_update(input_ref)

        db.session.commit()

    def update_reference_by_citation_key(
        self, input_ref: InputReference, updates: dict[str, str]
    ):
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

        updates["id"] = input_ref.id
        db.session.execute(sql, updates)

    def handle_authors_update(self, input_ref: InputReference):
        if input_ref.authors is not None:
            self.delete_authors(input_ref.id)
            author_ids = self.get_author_ids(input_ref)
            # Step 3: Insert new mappings into reference_authors
            self.insert_into_authors(author_ids, input_ref.id)

    def get_author_ids(self, input_ref: InputReference) -> list[int]:
        author_ids = []
        for author in input_ref.authors:
            author_name = author.strip()
            if not author_name:
                continue

            # Try to insert author, or get existing ID
            author_id = self.insert_into_author(author_name)
            author_ids.append(author_id)

        return author_ids

    def insert_into_author(self, author_name: str) -> int:
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
        return author_id
