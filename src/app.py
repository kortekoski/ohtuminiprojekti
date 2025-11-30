"""main application defining routes and reference logic"""
from flask import Response, redirect, render_template, request, jsonify, flash, g
from db_helper import reset_db
from entities.reference import Reference
from config import app, test_env
from services.bibtex_service import BibtexService
from services.reference_service import ReferenceService
from services.validation_service import ValidationService
from util import RefField


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
def new_type_selection():
    """Renders the new reference creation form."""
    return render_template("new_reference.html")

@app.route("/new_reference/<reftype>")
def new(reftype):
    """renders the addition form for the selected type"""
    return render_template(f"add_{reftype}.html")

@app.route("/create_reference", methods=["POST"])
def reference_creation():
    """Handles the creation of a new reference."""
    citation_key = request.form.get(RefField.CITATION_KEY.value)
    year = int(request.form.get(RefField.YEAR.value))
    author = request.form.get(RefField.AUTHOR.value)
    title = request.form.get(RefField.TITLE.value)
    reftype = request.form.get(RefField.REFTYPE.value)

    extra = {}
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

        flash(f"Reference {citation_key} created successfully!", "success")
        return redirect("/")
    except Exception as error:  # pylint: disable=broad-exception-caught
        flash(str(error), "error")
        return redirect("/new_reference")


@app.route("/delete_reference/<citation_key>", methods=["POST"])
def delete_reference(citation_key):
    """
    Handles the deletion of a reference by citation key.
    The citation key is chosen as the parameter due to it being unique between all references.
    """
    service = get_reference_service()
    try:
        if not service.citation_key_exists(citation_key):
            flash(f"Reference {citation_key} not found.", "error")
            return redirect("/")
        service.delete_reference(citation_key)
        flash(f"Reference {citation_key} deleted successfully!", "success")
    except Exception as error:  # pylint: disable=broad-exception-caught
        flash(str(error), "error")
    return redirect("/")


@app.route("/update_reference/<int:ref_id>", methods=["POST"])
def update_reference(ref_id):
    """Handles the updating of an existing reference."""

    reference_service = get_reference_service()
    old_ref = reference_service.get_reference_by_id(ref_id)

    citation_key = request.form.get(RefField.CITATION_KEY.value)
    year = request.form.get(RefField.YEAR.value)
    author = request.form.get(RefField.AUTHOR.value)
    title = request.form.get(RefField.TITLE.value)
    reftype = request.form.get(RefField.REFTYPE.value)

    extra = {}
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
        updated_reference = Reference(
            ref_id,
            citation_key,
            int(year) if year else None,
            author,
            title,
            reftype,
            extra,
        )

        ValidationService.validate_reference(updated_reference, existing_citation_keys)
        reference_service.update_reference_by_id(
            ref_id,
            citation_key,
            int(year) if year else None,
            author,
            title,
            reftype,
            extra,
        )

        flash(f"Reference {old_ref.citation_key} updated successfully!", "success")
        return redirect("/")
    except Exception as error:  # pylint: disable=broad-exception-caught
        flash(str(error), "error")
        return redirect("/")


@app.route("/download_bibtex")
def download_bibtex():
    """generates and gives the BibTex file"""
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
    except Exception as error:  # pylint: disable=broad-exception-caught
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
