# from logging import debug, info, warn, error
from config import app, API_ROOT
from .actions import get_all_references, get_reference_by_id, create_new_reference

ALL_REFERENCES_LOCATION = API_ROOT + "/all_references"
NEW_REFERENCE_LOCATION = API_ROOT + "/new_reference"
REFERENCES_LOCATION = API_ROOT + "/references"


app.route(ALL_REFERENCES_LOCATION, methods=["GET"])(get_all_references)

app.route(NEW_REFERENCE_LOCATION, methods=["GET"])(create_new_reference)

app.route(REFERENCES_LOCATION + "/<int:reference_id>", methods=["GET"])(
    get_reference_by_id
)
