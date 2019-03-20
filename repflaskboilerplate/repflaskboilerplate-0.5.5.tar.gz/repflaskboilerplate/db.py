from flask_sqlalchemy import SQLAlchemy
from hashlib import sha256
import time
import os
from repflaskboilerplate.app_global import app, db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    advertiser = db.Column(db.Boolean, default=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    credentials = db.Column(db.String(256), nullable=False)
    rating = db.Column(db.Float, default=1)

    def __repr__(self):
        return '<User %r>' % self.username


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('posts', lazy=True))
    campain_id = db.Column(
        db.Integer, db.ForeignKey('campain.id'), nullable=True)
    campain = db.relationship(
        'Campain', backref=db.backref('posts', lazy=False))
    tags_id = db.Column(db.Integer, nullable=True)
    likes = db.Column(db.Integer, default=0)
    active = db.Column(db.Boolean, default=False)
    nsfw = db.Column(db.Boolean, default=False)
    platform = db.Column(db.Integer, default=0)
    caption = db.relationship('Comment')

    def __repr__(self):
        return '<Post %r>' % self.id


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    post = db.relationship('Post', backref=db.backref('comments', lazy=True))
    content = db.Column(db.String(512), nullable=False)

    def __repr__(self):
        return '<Comment %r>' % self.id


class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account_type = db.Column(db.Integer, nullable=False)
    access_token = db.Column(db.String(256), nullable=False)
    refresh_token = db.Column(db.String(256), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('accounts', lazy=False))

    def __repr__(self):
        return '<Account {}:{}>'.format(self.account_type, self.id)


class Session(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(256), default=sha256(
        (str(time.time()) + "sessSalt").encode("utf-8")).hexdigest())
    expires = db.Column(db.Float, default=(time.time() + 7200))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('session', lazy=False))

    def __repr__(self):
        return '<Session {}:{}>'.format(self.id, self.expires)


class CampainRule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    campain_id = db.Column(db.ForeignKey('campain.id'), nullable=False)
    campain = db.relationship(
        'Campain', backref=db.backref('campain_rules', lazy=True))
    tag = db.Column(db.String(50), nullable=True)
    description = db.Column(db.String(280), nullable=False)
    required = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<CampainRule {}:{}>'.format(self.id, self.campain_id)


class Campain(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    platforms = db.Column(db.Integer, default=0)
    hashtag = db.Column(db.String(50), nullable=False)
    budget = db.Column(db.Float, nullable=False)
    pay_rate = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('campains', lazy=False))

    def __repr__(self):
        return '<Campain %r>' % self.hashtag


db.create_all()
db.session.commit()


def new_user(username, password):
    user = User.query.filter_by(username=username).first()
    if user == None:
        newUser = User(username=username, credentials=sha256(
            (username + password + "super secret salt").encode('utf-8')).hexdigest())
        db.session.add(newUser)
        db.session.commit()
        return newUser


def new_session(user_name, credentials):
    user = User.query.filter_by(username=user_name).first()
    if user.credentials == credentials:
        Session.query.filter_by(user_id=user.id).delete()
        newSession = Session(user=user)
        db.session.add(newSession)
        db.session.commit()
        return newSession
    else:
        return False


def new_post(user):
    newPost = Post(user=user)
    db.session.add(newPost)
    db.session.commit()
    return newPost


def link_post_to_campain(post_id, campain_id):
    post = Post.query.filter_by(post_id=post_id).first()
    campain = Campain.query.filter_by(campain_id=campain_id).first()
    post.campain = campain
    db.session.commit()


def set_post_to_active(post_id, caption):
    post = Post.query.filter_by(post_id=post_id).first()
    post.active = True
    post.caption = Comment(post=post, content=caption)
    db.session.commit()


def get_caption(post_id):
    post = Post.query.filter_by(post_id=post_id).first()
    return post.caption


def get_posts_by_user(user_id):
    user = User.query.filter_by(user_id=user_id).first()
    return user.posts


def get_posts_by_campain(campain_id):
    campain = Campain.query.filter_by(campain_id=campain_id).first()
    return campain.posts


def get_user_by_session(token):
    session = Session.query.filter_by(token=token).first()
    return session.user


def check_session(session_token):
    session = Session.query.filter_by(token=session_token).first()
    print(session)
    if not session:
        print("session not found")
        return -1
    elif session.expires < time.time():
        print("session expired")
        return 0
    else:
        return 1

# dev helper DELETE LATER!!!


def flashDB():
    db.delete_all()
    db.create_all()
    db.session.commit()
