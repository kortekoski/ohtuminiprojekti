from flask import redirect, render_template, request, jsonify, flash
from db_helper import reset_db
from entities.reference import Reference
from repositories.reference_repository import get_references, create_reference
from config import app, test_env
from util import validate_reference
from api import api

@app.route("/")
def index():
    references: list[Reference] = get_references()
    return render_template("index.html", references=references)

@app.route("/new_reference")
def new():
    return render_template("new_reference.html")

@app.route("/create_reference", methods=["POST"])
def reference_creation():
    year = int(request.form.get("year"))
    author = request.form.get("author")
    title = request.form.get("title")
    reftype = request.form.get("reftype")

    try:
        new_reference = Reference(None, year, author, title, reftype)
        validate_reference(new_reference)
        # Pitäisikö muuttaa käyttämään referenceä?
        create_reference(year, author, title, reftype)
        flash("Reference created successfully!")
        return redirect("/")
    except Exception as error:
        flash(str(error))
        return  redirect("/new_reference")

# Jätetään esimerkeiksi tulevaa käyttöä varten kommentoituina
# @app.route("/new_todo")
# def new():
#     return render_template("new_todo.html")

# @app.route("/create_todo", methods=["POST"])
# def todo_creation():
#     content = request.form.get("content")

#     try:
#         validate_todo(content)
#         create_todo(content)
#         return redirect("/")
#     except Exception as error:
#         flash(str(error))
#         return  redirect("/new_todo")

# @app.route("/toggle_todo/<todo_id>", methods=["POST"])
# def toggle_todo(todo_id):
#     set_done(todo_id)
#     return redirect("/")

# testausta varten oleva reitti
if test_env:
    @app.route("/reset_db")
    def reset_database():
        reset_db()
        return jsonify({ 'message': "db reset" })
    
# testausta varten oleva reitti
if test_env:
    @app.route("/add_test_reference", methods=["POST"])
    def add_test_reference():
        year = int(request.form.get("year"))
        author = request.form.get("author")
        title = request.form.get("title")
        reftype = request.form.get("reftype")

        create_reference(year, author, title, reftype)
        return jsonify({ 'message': "reference registered" })
