"""Google Firestore API client."""

from bits.google.services.base import Base
from google.cloud import firestore


class Firestore(Base):
    """Firestore class."""

    def __init__(self, project, credentials=None):
        """Initialize a class instance."""
        # uses application default credentials.
        self.db = firestore.Client(project, credentials=credentials)
        self.firestore = firestore

    def get_docs(self, collection):
        """Return a list of docs in a collection."""
        ref = self.db.collection(collection)
        return list(ref.get())

    def get_docs_dict(self, collection):
        """Return a dict of docs in a collection."""
        docs = {}
        for doc in self.get_docs(collection):
            docs[doc.id] = doc
        return docs

    def update_collection(self, collection, data, docs=None, delete_docs=False):
        """Update docs in a Firestore collection."""
        if not docs:
            docs = self.get_docs_dict(collection)

        # create lists
        add = {}
        delete = {}
        update = {}

        # find docs to add
        for key in data:
            if key not in docs:
                add[key] = data[key]
                print('Add: %s' % (key))
                self.db.collection(collection).document(key).set(data[key])

        # find docs to delete
        for key in docs:
            if key not in data:
                delete[key] = docs[key]

                # delete doc
                print('Delete: %s' % (key))
                self.db.collection(collection).document(key).delete()

        # find docs to update
        for key in docs:
            if key not in data:
                continue

            # get new and old doc
            new = data[key]
            old = docs[key].to_dict()

            # check for diff
            if new != old:
                update[key] = new

                # update doc
                print('Update: %s' % (key))
                self.db.collection(collection).document(key).set(new)

        output = 'Add: %s, delete: %s, update: %s\n' % (
            len(add),
            len(delete),
            len(update),
        )
        print(output)

        return output