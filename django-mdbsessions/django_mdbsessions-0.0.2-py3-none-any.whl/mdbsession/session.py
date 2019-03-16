from datetime import timedelta
from django.utils import timezone
from django.conf import settings
from django.contrib.sessions.backends.base import SessionBase, CreateError


def _store():
    return settings.MONGO_DB['session_store']


class SessionStore(SessionBase):
    '''
    MongoDB backend for Django sessions.
    '''

    def get_expiration_date(self):
        s = settings.SESSION_COOKIE_AGE
        return timezone.now() - timedelta(seconds=s)

    def load(self):
        mongo_session = _store().find_one({
            'session_key': self._get_or_create_session_key(),
            'creation_date': {
                '$gt': self.get_expiration_date()
            }
        })

        if mongo_session is None:
            # we just created a new session
            # self._session_key = None
            return {}
        else:
            return mongo_session['session_data']

    def exists(self, session_key):
        session = _store().find_one({
            'session_key': session_key,
        })

        if session is None:
            return False
        else:
            # mongodb ttl invalidation runs only once per minute, delete manually
            if session['creation_date'] <= self.get_expiration_date():
                self.delete(session_key)
                return self.exists(session_key)
            return True

    def create(self):
        while True:
            self._session_key = self._get_new_session_key()
            # ensure that session key is unique
            try:
                self.save(must_create=True)
            except CreateError:
                continue
            self.modified = True
            return

    def save(self, must_create=False):
        if self.session_key is None:
            return self.create()
        if must_create and self.exists(self.session_key):
            raise CreateError

        session = {
            'session_key': self.session_key,
            'session_data': self.encode(
                self._get_session(no_load=must_create)
            ),
            'creation_date': timezone.now()
        }

        _store().update_one(
            {'session_key': self.session_key},
            {'$set': session},
            upsert=True
        )

    def delete(self, session_key=None):
        if session_key is None:
            session_key = self._session_key
        if session_key is None:
            return
        _store().delete_one({'session_key': session_key})
        self._session_key = None

    def encode(self, session_dict):
        return session_dict

    def decode(self, session_data):
        return session_data

    def set_expiry(self, value):
        raise NotImplementedError
