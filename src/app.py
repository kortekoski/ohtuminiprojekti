"""
main application defining routes and reference logic
"""

from flask import (
    Request,
    Response,
    redirect,
    render_template,
    request,
    jsonify,
    flash,
    g,
    session,
)
from db_helper import reset_db
from entities.reference import Reference, InputReference
from config import app, test_env
from services.bibtex_service import BibtexService
from services.reference_service import ReferenceService
from services.validation_service import ValidationService
from services.doi_service import DoiService
from util import RefField, UserInputError


# ---------------------------
# Reference Service Dependency Provider, Flask g
# ---------------------------
def get_reference_service() -> ReferenceService:
    """Returns a cached ReferenceService per request."""
    if "reference_service" not in g:
        g.reference_service = ReferenceService()
    return g.reference_service


def get_doi_service() -> DoiService:
    if "doi_service" not in g:
        g.doi_service = DoiService()
    return g.doi_service


def create_extra_dict(request: Request) -> dict[str, str]:
    extra = {}
    for key, value in request.form.to_dict().items():
        if key in [
            RefField.CITATION_KEY.value,
            RefField.YEAR.value,
            RefField.AUTHOR.value,
            RefField.TITLE.value,
            RefField.REFTYPE.value,
        ]:
            continue
        extra[key] = value
    return extra


def capitalize_name(name: str) -> str:
    """Capitalize first letter of each word and lowercase the rest."""
    if not name:
        return name
    # Split by spaces and capitalize each word
    words = name.split()
    return " ".join(
        word[0].upper() + word[1:] if len(word) > 1 else word.upper() for word in words
    )


def create_input_reference(
    request: Request, reference_id: int | None = None
) -> InputReference:
    citation_key = request.form.get(RefField.CITATION_KEY.value)
    year = int(request.form.get(RefField.YEAR.value))
    authors = request.form.getlist(RefField.AUTHOR.value)
    title = request.form.get(RefField.TITLE.value)
    reftype = request.form.get(RefField.REFTYPE.value)

    extra = create_extra_dict(request)

    capitalized_authors = []
    for author in authors:
        if "," in author:
            parts = author.split(",", 1)
            lastname = capitalize_name(parts[0].strip())
            firstname = capitalize_name(parts[1].strip()) if len(parts) > 1 else ""
            capitalized_authors.append(f"{lastname}, {firstname}")
        else:
            capitalized_authors.append(capitalize_name(author.strip()))

    return InputReference(
        citation_key=citation_key,
        year=year,
        authors=capitalized_authors,
        title=title,
        reftype=reftype,
        extra=extra,
        id=reference_id,
    )


# ---------------------------
# Routes
# ---------------------------
@app.route("/")
def index():
    """Renders the index page with all references."""
    service = get_reference_service()
    references: list[Reference] = service.get_all_references()
    return render_template(
        "index.html",
        references=references,
        generate_bibtex=BibtexService.generate_bibtex,
        get_reference_by_id=service.get_reference_by_id,
    )


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
    input_ref = create_input_reference(request)
    citation_key = input_ref.citation_key
    authors = input_ref.authors

    reference_service = get_reference_service()
    existing_citation_keys = reference_service.get_citation_keys()

    try:
        ValidationService.validate_input_reference(
            input_ref, existing_citation_keys, authors=authors
        )

        reference_service.create_reference(input_ref)

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


@app.route("/update_reference/<int:ref_id>", methods=["GET", "POST"])
def update_reference(ref_id):
    """Handles the updating of an existing reference."""

    reference_service = get_reference_service()
    old_ref = reference_service.get_reference_by_id(ref_id)

    if request.method == "GET":
        return render_template(f"add_{old_ref.reftype}.html", reference=old_ref)
    if request.method == "POST":
        input_ref = create_input_reference(request, ref_id)
        citation_key = input_ref.citation_key
        authors = input_ref.authors

        reference_service = get_reference_service()
        existing_citation_keys = reference_service.get_citation_keys()

        try:
            ValidationService.validate_input_reference(
                input_ref,
                existing_citation_keys,
                same_citation_key=(old_ref.citation_key == citation_key),
                authors=authors,
            )

            reference_service.update_reference_by_id(
                input_ref, same_citation_key=(old_ref.citation_key == citation_key)
            )

            flash(f"Reference {old_ref.citation_key} updated successfully!", "success")
            return redirect("/")
        except Exception as error:  # pylint: disable=broad-exception-caught
            flash(str(error), "error")
            return redirect("/")

    return None


@app.route("/download_bibtex")
def download_bibtex():
    """generates and gives the BibTex file"""
    reference_service = get_reference_service()
    refs = reference_service.get_all_references(bibtex=True)

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


@app.route("/add_from_doi", methods=["POST"])
def add_from_doi():
    doi = request.form.get("doi")
    citation_key = request.form.get("citation_key")
    if doi is None:
        flash("error", "Input needs to have a DOI.")
        return redirect("/new_reference/from_doi")
    if citation_key is None:
        flash("error", "Input needs to have a citation key.")
        return redirect("/new_reference/from_doi")
    citation_key = request.form.get("citation_key")
    try:
        doi_service = get_doi_service()
        ref = doi_service.get_doi(doi)
        if ref is None:
            # This only happens when we somehow fail to
            # contact api.crossref.org.
            flash("Failed to retrieve DOI. Try again later.", "error")
            return redirect("/")

        # DOI service returns author as a string, split it into a list for validation
        authors = [a.strip() for a in ref.author.split(" and ")]
        ValidationService.validate_input_reference(ref, authors=authors)
        reference_service = get_reference_service()

        input_ref = InputReference(
            citation_key=citation_key,
            year=ref.year,
            authors=authors,
            title=ref.title,
            reftype=ref.reftype,
            extra=ref.extra,
        )
        reference_service.create_reference(input_ref)
        flash(f"Reference {citation_key} created succesfully!", "success")
        return redirect("/")
    except UserInputError as err:
        flash(str(err), "error")
        return redirect("/new_reference/from_doi")


@app.before_request
def init_easter_egg():
    """Initializes session["enable-easter-egg"] to False.
    This is run before further handling of all requests."""
    session.setdefault("enable-easter-egg", False)


@app.route("/toggle_easter_egg")
def toggle_easter_egg():
    """Toggle session["enable-easter-egg"] between
    True/False and redirect caller to args["origin"]."""
    session["enable-easter-egg"] = not session.get("enable-easter-egg", False)
    origin = request.args.get("origin", "/")
    return redirect(origin)


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

        input_ref = create_input_reference(request)
        service = get_reference_service()
        service.create_reference(input_ref)

        return jsonify({"message": "reference registered"})
