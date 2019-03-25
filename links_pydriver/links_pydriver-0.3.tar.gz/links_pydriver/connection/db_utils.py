from pymongo import MongoClient

PORT = 27017
DB_NAME = 'links'

def connect():
    client = MongoClient('mongodb://localhost:{0}'.format(PORT))
    db = client[DB_NAME]

    return db
