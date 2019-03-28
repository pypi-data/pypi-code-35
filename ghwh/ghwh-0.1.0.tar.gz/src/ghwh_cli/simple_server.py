from ghwh import init_app
from ghwh import init_celery
from ghwh import register


app = init_app()
celery = init_celery(app)


@celery.task()
def handler(headers, payload):
    print(headers)
    print(payload)


def main():
    register("push", handler)
    app.run()
