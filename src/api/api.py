# from logging import debug, info, warn, error
from config import app, db
from flask import jsonify, request
from entities.reference import Reference
from repositories import reference_repository as repo
from util import is_valid_reference

HTTP_400_BAD_REQUEST = 400
HTTP_404_NOT_FOUND = 404
HTTP_500_INTERNAL_SERVER_ERROR = 500
API_ROOT = "/api"

@app.route(API_ROOT + "/all_references", methods=["GET"])
def get_all_references():
    references: list[Reference] = repo.get_references()
    return jsonify(references)

@app.route(API_ROOT + "/new_reference", methods=["GET"])
def create_new_reference():
    # We don't flatten the arguments since a reference
    # can have multiple authors.
    args = request.args.to_dict(flat=False)
    if not is_valid_reference(args):
        # debug(f"Failed to parse reference: \"{args}\"")
        return jsonify({
            "error": "invalid reference"
        }), HTTP_400_BAD_REQUEST

    try:
        repo.create_reference(
            int(args["year"][0]),
            args["author"][0],
            args["title"][0],
            args["type"][0]
        )
        return jsonify({
            "message": "reference created succesfully"
        })
    except Exception as err:
        # error(f"Failed to add reference:\n{err}")
        return jsonify({
            "error": "internal server error"
        }), HTTP_500_INTERNAL_SERVER_ERROR

@app.route(API_ROOT + "/references/<int:reference_id>", methods=["GET"])
def get_reference_by_id(reference_id: int):
    ref: Reference|None = repo.get_reference_by_id(reference_id)

    if ref is None:
        return jsonify({
            "error": "reference not found"
        }), HTTP_404_NOT_FOUND

    return jsonify(ref)
