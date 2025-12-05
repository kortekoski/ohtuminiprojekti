import unittest
from unittest.mock import Mock
from services.reference_service import ReferenceService
from entities.reference import Reference, InputReference
from tests.test_data import TestData
from util import RefField


class TestReferenceService(unittest.TestCase):

    def test_service_returns_references_from_repository(self):
        """Service should use repository.get_references() and return its result."""

        # Arrange – mock repository
        mock_repo = Mock()
        mock_repo.get_references.return_value = [TestData.valid_reference_object()]

        service = ReferenceService(repo=mock_repo)

        # Act
        result = service.get_all_references()

        # Assert
        mock_repo.get_references.assert_called_once()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].citation_key, "Test2024")

    def test_delete_reference(self):
        """Service should call repository.delete_reference() with correct citation key."""

        # Arrange
        mock_repo = Mock()
        service = ReferenceService(repo=mock_repo)
        citation_key_to_delete = "Test2024"

        # Act
        service.delete_reference(citation_key_to_delete)

        # Assert – ensure correct repository interaction
        mock_repo.delete_reference.assert_called_once_with(citation_key_to_delete)

    def test_create_reference_raises_error_if_citation_key_exists(self):
        # Arrange
        mock_repo = Mock()
        mock_repo.get_references.return_value = [TestData.valid_reference_object()]
        mock_repo.citation_key_exists.return_value = True  # KEY ALREADY EXISTS

        service = ReferenceService(repo=mock_repo)

        # Act + Assert
        with self.assertRaises(Exception):
            service.create_reference(TestData.valid_input_reference())

        # The repository's create_reference MUST NOT be called
        mock_repo.create_reference.assert_not_called()

    def test_update_reference_fails_if_citation_key_already_exists(self):
        """Updating should fail if the new citation_key is already in use."""

        # Arrange
        mock_repo = Mock()

        # Database already contains ref with key "Test2024"
        mock_repo.get_references.return_value = [TestData.valid_reference()]
        mock_repo.citation_key_exists.return_value = True  # key exists

        service = ReferenceService(repo=mock_repo)

        # Act + Assert
        with self.assertRaises(ValueError) as ctx:
            service.update_reference_by_id(
                id=1,
                citation_key="Test2024",  # duplicate key
                year=2001,
                authors=["Bad Dude"],
                title="all out of gum",
                reftype="book",
                extra={},
            )

        # Ensure the correct error was raised
        self.assertIn("already exists", str(ctx.exception))

        # Repository must NOT be called
        mock_repo.update_reference.assert_not_called()

    def test_update_reference_succeeds_if_citation_key_is_unique(self):
        """Updating should succeed when the citation_key is new."""

        # Arrange
        mock_repo = Mock()

        # Old reference exists
        existing = TestData.valid_reference()
        mock_repo.get_references.return_value = [existing]

        # New key is unique -> citation_key_exists returns False
        mock_repo.citation_key_exists.return_value = False

        service = ReferenceService(repo=mock_repo)

        data = TestData.updated_reference_json()
        # Act
        service.update_reference_by_id(
            id=data["id"],
            citation_key=data[RefField.CITATION_KEY.value],
            year=data[RefField.YEAR.value],
            authors=[data[RefField.AUTHOR.value]],
            title=data[RefField.TITLE.value],
            reftype=data[RefField.REFTYPE.value],
            extra=data[RefField.EXTRA.value],
        )

        # Assert – repository update must be called with correct params
        mock_repo.update_reference.assert_called_once_with(
            data["id"],
            data[RefField.CITATION_KEY.value],
            data[RefField.YEAR.value],
            [data[RefField.AUTHOR.value]],
            data[RefField.TITLE.value],
            data[RefField.REFTYPE.value],
            data[RefField.EXTRA.value],
        )

    def test_update_fails_if_citation_key_belongs_to_another_reference(self):
        """Updating should fail ONLY when changing to a citation_key
        that belongs to a different reference."""

        # Arrange
        mock_repo = Mock()

        # Two existing references in database
        refs = TestData.valid_multiple_reference_objects()
        old = refs[0]  # id=1, citation_key="Test2024"
        other = refs[1]  # id=2, citation_key="Test2025"

        # Repository returns both references
        mock_repo.get_references.return_value = refs

        # Mock: citation_key_exists("Test2025") → True
        # This simulates trying to change key to another reference's key
        mock_repo.citation_key_exists.side_effect = (
            lambda key: key == other.citation_key
        )

        service = ReferenceService(repo=mock_repo)

        # ACT + ASSERT — Trying to update old.id to use other's key
        with self.assertRaises(ValueError) as ctx:
            service.update_reference_by_id(
                id=old.id,
                citation_key=other.citation_key,  # <-- belongs to ID 2
                year=old.year,
                authors=[old.author],
                title=old.title,
                reftype=old.reftype,
                extra=old.extra,
            )

        # Ensure error explains the situation
        self.assertIn("already exists", str(ctx.exception))

        # Repository update must NEVER be called
        mock_repo.update_reference.assert_not_called()
