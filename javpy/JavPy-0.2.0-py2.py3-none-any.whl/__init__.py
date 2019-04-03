from JavPy.app.webserver import app


def serve(port=8081):
    app.app.run('0.0.0.0', port)


if __name__ == '__main__':
    serve()
