
from flask import Flask, jsonify, session, redirect
from authlib.flask.client import OAuth
from loginpass import create_flask_blueprint
from sqlalchemy import or_, and_

from pabu.auth import backends
from pabu.config import Config
from pabu.db import Database
from pabu.models import User

class Cache(object):
    def __init__(self):
        self._data = {}

    def get(self, k):
        return self._data.get(k)

    def set(self, k, v, timeout=None):
        self._data[k] = v

    def delete(self, k):
        if k in self._data:
            del self._data[k]



def add_auth_controllers(app: Flask, config: Config, db: Database):

    oauth = OAuth(app, Cache())

    def handle_authorize(remote, token, user_info):
        sub = user_info['sub']
        email = user_info['email']
        user_info['providerName'] = remote.name
        session['user_info'] = user_info
        with db.session_scope() as conn:
            user = conn.query(User).filter(or_(User.sub == sub, and_(User.email == email, User.email != None))).first()
            if not user:
                user = User(sub = sub, email = email)
                conn.add(user)
            user.email = email
            user.name = user_info['name']
            user.avatar = user_info['picture']
            conn.flush()
            session['user_id'] = user.id

        return redirect('/')

    for backend in backends:
        bp = create_flask_blueprint(backend, oauth, handle_authorize)
        app.register_blueprint(bp, url_prefix='/{}'.format(backend.OAUTH_NAME))


    @app.route('/logout')
    def logout(): # pylint: disable=unused-variable
        del session['user_info']
        del session['user_id']
        return redirect('/')
