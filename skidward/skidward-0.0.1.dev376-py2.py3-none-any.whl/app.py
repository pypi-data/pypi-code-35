import os

from flask import Flask

from skidward.models import db


ROOT_DIR = os.path.dirname(__file__)
TEMPLATE_DIR = os.path.join(ROOT_DIR, "web", "templates")

app = Flask(__name__, template_folder=TEMPLATE_DIR)

app.debug = os.getenv("FLASK_DEBUG")

# Setting any FLASK_ADMIN_SWATCH(Theme Template)
app.config["FLASK_ADMIN_SWATCH"] = os.getenv("FLASK_ADMIN_SWATCH")

# Setting up Postgres Database
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")

# Setting up security keys
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["SECURITY_PASSWORD_SALT"] = os.getenv("SECURITY_PASSWORD_SALT")
app.config["SECURITY_PASSWORD_HASH"] = os.getenv("SECURITY_PASSWORD_HASH")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = os.getenv(
    "SQLALCHEMY_TRACK_MODIFICATIONS"
)


db.init_app(app)

with app.app_context():
    db.create_all()
