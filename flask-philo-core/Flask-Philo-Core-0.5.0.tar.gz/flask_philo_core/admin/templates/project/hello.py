from flask import current_app


def run():
    app = current_app._get_current_object()
    print('hello')
    print(app)
