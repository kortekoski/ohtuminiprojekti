"""API actions for managing references."""

from flask import jsonify, request
from entities.reference import Reference
from repositories import reference_repository as repo
from services.validation_service import ValidationService
from util import RefField

HTTP_200_SUCCESS = 200
HTTP_400_BAD_REQUEST = 400
HTTP_404_NOT_FOUND = 404
HTTP_500_INTERNAL_SERVER_ERROR = 500


def get_all_references():
    references: list[Reference] = repo.get_references()
    return jsonify(references)


def create_new_reference():
    # We don't flatten the arguments since a reference
    # can have multiple authors.
    args = request.args.to_dict(flat=False)
    if not ValidationService.is_valid_reference(args):
        # debug(f"Failed to parse reference: \"{args}\"")
        return jsonify({"error": "invalid reference"}), HTTP_400_BAD_REQUEST

    try:
        repo.create_reference(
            args[RefField.CITATION_KEY][0],
            int(args[RefField.YEAR][0]),
            args[RefField.AUTHOR][0],
            args[RefField.TITLE][0],
            args[RefField.REFTYPE][0],
        )
        return jsonify({"message": "reference created succesfully"})
    except Exception as err:
        # error(f"Failed to add reference:\n{err}")
        return (
            jsonify({"error": "internal server error"}),
            HTTP_500_INTERNAL_SERVER_ERROR,
        )
