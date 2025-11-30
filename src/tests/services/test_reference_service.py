import unittest
from unittest.mock import Mock
from services.reference_service import ReferenceService
from entities.reference import Reference


class TestReferenceService(unittest.TestCase):

    def test_service_returns_references_from_repository(self):
        """Service should use repository.get_references() and return its result."""

        # Arrange – mock repository
        mock_repo = Mock()
        mock_repo.get_references.return_value = [
            Reference(1, "Key2024", 2024, "Author", "Title", "book")
        ]

        service = ReferenceService(repo=mock_repo)

        # Act
        result = service.get_all_references()

        # Assert
        mock_repo.get_references.assert_called_once()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].citation_key, "Key2024")

    def test_delete_reference(self):
        """Service should call repository.delete_reference() with correct citation key."""

        # Arrange
        mock_repo = Mock()
        service = ReferenceService(repo=mock_repo)
        citation_key_to_delete = "Key2024"

        # Act
        service.delete_reference(citation_key_to_delete)

        # Assert – ensure correct repository interaction
        mock_repo.delete_reference.assert_called_once_with(citation_key_to_delete)
