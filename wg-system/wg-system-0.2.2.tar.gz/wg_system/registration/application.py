from starlette.applications import Starlette
from . settings import DEBUG
from . routes import ROUTES

REGISTRATION = Starlette(debug=DEBUG, routes=ROUTES)