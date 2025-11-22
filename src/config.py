from os import getenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from json_provider import CustomJSONProvider

API_ROOT = "/api"

load_dotenv()

test_env = getenv("TEST_ENV") == "true"
print(f"Test environment: {test_env}")

if location := getenv("API_ROOT"):
    API_ROOT = location

app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
app.json = CustomJSONProvider(app)
db = SQLAlchemy(app)
