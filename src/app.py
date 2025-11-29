import re
from flask import Response, redirect, render_template, request, jsonify, flash, g
from db_helper import reset_db
from entities.reference import Reference
from config import app, test_env
from services.bibtex_service import BibtexService
from services.reference_service import ReferenceService
from services.validation_service import ValidationService
from services.template_service import TemplateService
from util import RefField, RefType


# ---------------------------
# Reference Service Dependency Provider, Flask g
# ---------------------------
def get_reference_service() -> ReferenceService:
    """Returns a cached ReferenceService per request."""
    if "reference_service" not in g:
        g.reference_service = ReferenceService()
    return g.reference_service


# ---------------------------
# Routes
# ---------------------------
@app.route("/")
def index():
    """Renders the index page with all references."""
    service = get_reference_service()
    references: list[Reference] = service.get_all_references()
    return render_template("index.html", references=references)


@app.route("/new_reference")
def new():
    """Renders the new reference creation form."""
    return render_template(
        "new_reference.html", schemas=TemplateService.relevant_attributes(RefType.BOOK)
    )


@app.route("/create_reference", methods=["POST"])
def reference_creation():
    """Handles the creation of a new reference."""
    citation_key = request.form.get(RefField.CITATION_KEY.value)
    year = int(request.form.get(RefField.YEAR.value))
    author = request.form.get(RefField.AUTHOR.value)
    title = request.form.get(RefField.TITLE.value)
    reftype = request.form.get(RefField.REFTYPE.value)

    extra = dict()
    for key, value, *_ in request.form.to_dict():
        if key in [
            RefField.CITATION_KEY.value,
            RefField.YEAR.value,
            RefField.AUTHOR.value,
            RefField.TITLE.value,
            RefField.REFTYPE.value,
        ]:
            continue
        extra[key] = value

    reference_service = get_reference_service()
    existing_citation_keys = reference_service.get_citation_keys()

    try:
        new_reference = Reference(
            None, citation_key, year, author, title, reftype, extra
        )

        ValidationService.validate_reference(new_reference, existing_citation_keys)
        reference_service.create_reference(
            citation_key, year, author, title, reftype, extra
        )

        flash("Reference created successfully!", "success")
        return redirect("/")
    except Exception as error:
        flash(str(error), "error")
        return redirect("/new_reference")


@app.route("/download_bibtex")
def download_bibtex():
    reference_service = get_reference_service()
    refs = reference_service.get_all_references()

    if not refs:
        flash("No references available to download", "error")
        return redirect("/")

    try:
        bibtex_content = BibtexService.generate_bibtex(refs)
        return Response(
            bibtex_content,
            mimetype="text/plain",
            headers={
                "Content-Disposition": "attachment; filename=references.bib",
            },
        )
    except Exception as error:
        flash(str(error), "error")
        return redirect("/")


# ---------------------------
# Test Routes
# ---------------------------

if test_env:

    @app.route("/reset_db")
    def reset_database():
        """Resets the database to an empty state."""
        reset_db()
        return jsonify({"message": "db reset"})

    @app.route("/add_test_reference", methods=["POST"])
    def add_test_reference():
        """Adds a reference for testing purposes."""
        citation_key = request.form.get(RefField.CITATION_KEY.value)
        year = int(request.form.get(RefField.YEAR.value))
        author = request.form.get(RefField.AUTHOR.value)
        title = request.form.get(RefField.TITLE.value)
        reftype = request.form.get(RefField.REFTYPE.value)

        service = get_reference_service()
        service.create_reference(citation_key, year, author, title, reftype)

        return jsonify({"message": "reference registered"})
