from flask import current_app


def run():
    app = current_app._get_current_object()
    app.run(
        host=app.config['HOST'], port=app.config['PORT'])
