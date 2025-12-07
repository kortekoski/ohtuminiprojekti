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

    def test_get_all_references_with_bibtex_true_skips_parsing(self):
        """When bibtex=True, should return references without parsing authors."""

        # Arrange
        mock_repo = Mock()
        # Create a reference with unparsed author format
        ref = Reference(
            1, "Test2024", 2001, "Smith, John and Doe, Jane", "Title", "book", {}
        )
        mock_repo.get_references.return_value = [ref]

        service = ReferenceService(repo=mock_repo)

        # Act
        result = service.get_all_references(bibtex=True)

        # Assert
        mock_repo.get_references.assert_called_once()
        self.assertEqual(len(result), 1)
        # Author field should remain unparsed (no abbreviation)
        self.assertEqual(result[0].author, "Smith, John and Doe, Jane")

    def test_get_all_references_with_bibtex_false_parses_authors(self):
        """When bibtex=False (default), should parse author names."""

        # Arrange
        mock_repo = Mock()
        # Create a reference with unparsed author format
        ref = Reference(
            1, "Test2024", 2001, "Smith, John and Doe, Jane", "Title", "book", {}
        )
        mock_repo.get_references.return_value = [ref]

        service = ReferenceService(repo=mock_repo)

        # Act
        result = service.get_all_references(bibtex=False)

        # Assert
        mock_repo.get_references.assert_called_once()
        self.assertEqual(len(result), 1)
        # Author field should be parsed to abbreviated format
        self.assertEqual(result[0].author, "Smith, J. and Doe, J.")

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
        input_ref = InputReference(
            citation_key="Test2024",  # duplicate key
            year=2001,
            authors=["Bad Dude"],
            title="all out of gum",
            reftype="book",
            extra={},
            id=1,
        )
        with self.assertRaises(ValueError) as ctx:
            service.update_reference_by_id(input_ref)

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
        input_ref = InputReference(
            citation_key=data[RefField.CITATION_KEY.value],
            year=data[RefField.YEAR.value],
            authors=[data[RefField.AUTHOR.value]],
            title=data[RefField.TITLE.value],
            reftype=data[RefField.REFTYPE.value],
            extra=data[RefField.EXTRA.value],
            id=data["id"],
        )
        service.update_reference_by_id(input_ref)

        # Assert – repository update must be called once
        mock_repo.update_reference.assert_called_once()

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
        input_ref = InputReference(
            citation_key=other.citation_key,  # <-- belongs to ID 2
            year=old.year,
            authors=[old.author],
            title=old.title,
            reftype=old.reftype,
            extra=old.extra,
            id=old.id,
        )
        with self.assertRaises(ValueError) as ctx:
            service.update_reference_by_id(input_ref)

        # Ensure error explains the situation
        self.assertIn("already exists", str(ctx.exception))

        # Repository update must NEVER be called
        mock_repo.update_reference.assert_not_called()

    def test_id_exists_returns_true_when_id_found(self):
        """Should return True when ID exists in repository."""
        # Arrange
        mock_repo = Mock()
        refs = TestData.valid_multiple_reference_objects()
        # refs[0] has id=1, refs[1] has id=2
        mock_repo.get_references.return_value = refs

        service = ReferenceService(repo=mock_repo)

        # Act
        result = service.id_exists(1)

        # Assert
        self.assertTrue(result)
        mock_repo.get_references.assert_called_once()

    def test_id_exists_returns_false_when_id_not_found(self):
        """Should return False when ID does not exist in repository."""
        # Arrange
        mock_repo = Mock()
        refs = TestData.valid_multiple_reference_objects()
        # refs[0] has id=1, refs[1] has id=2
        mock_repo.get_references.return_value = refs

        service = ReferenceService(repo=mock_repo)

        # Act
        result = service.id_exists(999)

        # Assert
        self.assertFalse(result)
        mock_repo.get_references.assert_called_once()

    def test_id_exists_with_empty_repository(self):
        """Should return False when repository is empty."""
        # Arrange
        mock_repo = Mock()
        mock_repo.get_references.return_value = []

        service = ReferenceService(repo=mock_repo)

        # Act
        result = service.id_exists(1)

        # Assert
        self.assertFalse(result)
        mock_repo.get_references.assert_called_once()

    def test_parse_author_string_with_one_author(self):
        """Should return original string for single author."""
        service = ReferenceService()
        result = service.parse_author_string("John Doe")
        self.assertEqual(result, "John Doe")

    def test_parse_author_string_with_two_authors(self):
        """Should return original string for two authors."""
        service = ReferenceService()
        result = service.parse_author_string("John Doe and Jane Smith")
        self.assertEqual(result, "John Doe and Jane Smith")

    def test_parse_author_string_with_three_authors(self):
        """Should return original string for three authors."""
        service = ReferenceService()
        result = service.parse_author_string("John Doe and Jane Smith and Bob Brown")
        self.assertEqual(result, "John Doe and Jane Smith and Bob Brown")

    def test_parse_author_string_with_more_than_three_authors(self):
        """Should return first author and 'et al.' for more than three authors."""
        service = ReferenceService()
        result = service.parse_author_string(
            "John Doe and Jane Smith and Bob Brown and Alice Cooper"
        )
        self.assertEqual(result, "John Doe et al.")

    def test_parse_author_string_with_five_authors(self):
        """Should return first author and 'et al.' for five authors."""
        service = ReferenceService()
        result = service.parse_author_string("A and B and C and D and E")
        self.assertEqual(result, "A et al.")

    def test_parse_author_string_strips_whitespace(self):
        """Should strip whitespace around author names."""
        service = ReferenceService()
        result = service.parse_author_string(
            "  John Doe  and  Jane Smith  and  Bob Brown  and  Alice Cooper  "
        )
        self.assertEqual(result, "John Doe et al.")

    def test_parse_authors_modifies_reference_list(self):
        """Should modify author field in all references in the list."""
        service = ReferenceService()
        refs = [
            Reference(1, "key1", 2020, "A and B and C and D", "Title1", "book", {}),
            Reference(2, "key2", 2021, "X and Y", "Title2", "article", {}),
        ]

        result = service.parse_authors(refs)

        self.assertEqual(result[0].author, "A et al.")
        self.assertEqual(result[1].author, "X and Y")

    def test_parse_authors_returns_same_list(self):
        """Should return the same list object that was passed in."""
        service = ReferenceService()
        refs = [
            Reference(1, "key1", 2020, "John Doe", "Title1", "book", {}),
        ]

        result = service.parse_authors(refs)

        self.assertIs(result, refs)

    def test_parse_authors_with_empty_list(self):
        """Should handle empty list without errors."""
        service = ReferenceService()
        result = service.parse_authors([])
        self.assertEqual(result, [])

    def test_parse_name_with_lastname_firstname(self):
        """Should convert 'Lastname, Firstname' to 'Lastname, F.'"""
        service = ReferenceService()
        result = service.parse_name("Smith, John")
        self.assertEqual(result, "Smith, J.")

    def test_parse_name_with_multiple_first_names(self):
        """Should convert 'Lastname, Firstname Middlename' to 'Lastname, F. M.'"""
        service = ReferenceService()
        result = service.parse_name("Smith, John Paul")
        self.assertEqual(result, "Smith, J. P.")

    def test_parse_name_with_three_names(self):
        """Should convert 'Lastname, Firstname Middlename1 Middlename2' to initials"""
        service = ReferenceService()
        result = service.parse_name("Smith, John Paul Robert")
        self.assertEqual(result, "Smith, J. P. R.")

    def test_parse_name_with_only_lastname(self):
        """Should return just the lastname when no firstname is provided"""
        service = ReferenceService()
        result = service.parse_name("Smith,")
        self.assertEqual(result, "Smith")

    def test_parse_name_without_comma(self):
        """Should return name as-is when no comma is present"""
        service = ReferenceService()
        result = service.parse_name("John Smith")
        self.assertEqual(result, "John Smith")

    def test_parse_name_strips_whitespace(self):
        """Should strip whitespace from lastname and firstname"""
        service = ReferenceService()
        result = service.parse_name("  Smith  ,  John  ")
        self.assertEqual(result, "Smith, J.")

    def test_parse_name_with_single_letter_firstname(self):
        """Should handle single letter firstname correctly"""
        service = ReferenceService()
        result = service.parse_name("Smith, J")
        self.assertEqual(result, "Smith, J.")

    def test_parse_name_with_empty_firstname(self):
        """Should return just lastname when firstname is empty string"""
        service = ReferenceService()
        result = service.parse_name("Smith, ")
        self.assertEqual(result, "Smith")
