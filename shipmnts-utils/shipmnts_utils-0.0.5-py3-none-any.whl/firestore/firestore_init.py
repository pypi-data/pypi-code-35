import os

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


def initialize_firestore():
    global fs_client
    firestore_path = os.getenv(
        "FIRESTORECRED", None
    )
    cred = credentials.Certificate(firestore_path)
    firebase_admin.initialize_app(cred)
    fs_client = firestore.client()

    return fs_client
