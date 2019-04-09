from celery import Celery

app = Celery('tasks', broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')


@app.task
def suma(x):
    suma = 0
    for i in range(x):
        suma += i
    return pp
