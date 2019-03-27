from pymongo import MongoClient


def connect(url='localhost', db_name='links', port=27017):
    client = MongoClient('mongodb://{0}:{1}'.format(url, port))
    db = client[db_name]

    return db
