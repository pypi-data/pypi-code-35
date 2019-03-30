from .app.webserver import app


def serve():
    app.app.run('0.0.0.0', 8081)
