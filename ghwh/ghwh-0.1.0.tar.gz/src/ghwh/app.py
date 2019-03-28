from flask import Flask

from .api.webhook import webhook


def init_app():
    app = Flask(__name__.split(".", 1)[0])
    app.register_blueprint(webhook)
    return app
