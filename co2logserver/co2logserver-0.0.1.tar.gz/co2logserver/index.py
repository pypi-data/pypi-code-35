# system modules
import datetime

# internal modules
from co2logserver import app
from co2logserver.config import config, database

# external modules
from flask import render_template


@app.route("/")
@app.route("/index", methods=["GET"])
def index():
    return render_template(
        "index.html",
        server={"name": config("NAME")},
        config=app.config,
        database=database(),
        date=datetime.datetime.utcnow()
        .replace(tzinfo=datetime.timezone.utc)
        .strftime("%F %T %Z"),
    )
