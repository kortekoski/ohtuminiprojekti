from flask import Response, redirect, render_template, request, jsonify, flash
from db_helper import reset_db
from entities.reference import Reference
from repositories.reference_repository import (
    get_citation_keys,
    get_references,
    create_reference,
)
from config import app, test_env
from services.reference_service import ReferenceService
from services.validation_service import ValidationService
from util import RefField
from api import routes


@app.route("/")
def index():
    """Renders the index page with all references."""
    references: list[Reference] = get_references()
    return render_template("index.html", references=references)


@app.route("/new_reference")
def new():
    """Renders the new reference creation form."""
    return render_template("new_reference.html")


@app.route("/create_reference", methods=["POST"])
def reference_creation():
    """Handles the creation of a new reference."""
    citation_key = request.form.get(RefField.CITATION_KEY.value)
    year = int(request.form.get(RefField.YEAR.value))
    author = request.form.get(RefField.AUTHOR.value)
    title = request.form.get(RefField.TITLE.value)
    reftype = request.form.get(RefField.REFTYPE.value)

    existing_citation_keys = get_citation_keys()

    try:
        new_reference = Reference(None, citation_key, year, author, title, reftype)
        ValidationService.validate_reference(new_reference, existing_citation_keys)
        create_reference(citation_key, year, author, title, reftype)
        flash("Reference created successfully!")
        return redirect("/")
    except Exception as error:
        flash(str(error))
        return redirect("/new_reference")


# TODO csrf, use url for safety, xss protection frontend, rate limit, DoS
@app.route("/download_bibtex")
def download_bibtex():
    refs = get_references()
    bibtex_content = ReferenceService.generate_bibtex(refs)

    flash(str("BibTeX file generated successfully!"))
    return Response(
        bibtex_content,
        mimetype="text/plain",
        headers={"Content-Disposition": "attachment; filename=references.bib"},
    )


# testausta varten oleva reitti
if test_env:

    @app.route("/reset_db")
    def reset_database():
        """Resets the database to an empty state."""
        reset_db()
        return jsonify({"message": "db reset"})


# testausta varten oleva reitti
if test_env:

    @app.route("/add_test_reference", methods=["POST"])
    def add_test_reference():
        """Adds a reference for testing purposes."""
        citation_key = request.form.get(RefField.CITATION_KEY.value)
        year = int(request.form.get(RefField.YEAR.value))
        author = request.form.get(RefField.AUTHOR.value)
        title = request.form.get(RefField.TITLE.value)
        reftype = request.form.get(RefField.REFTYPE.value)

        create_reference(citation_key, year, author, title, reftype)
        return jsonify({"message": "reference registered"})
