import os
from . import PGPString
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Sequence
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
base = declarative_base()


class User(db.Model):
    __tablename__ = 'user'

    sq_user_id = Sequence('sq_user_id', metadata=base.metadata)
    num_user_id = db.Column(db.Numeric, sq_user_id, server_default=sq_user_id.next_value(),
                            primary_key=True)
    str_user_name = db.Column(db.Text)
    str_user_password = db.Column(PGPString(os.environ.get('DBARTEMISKEY'), length=1000))
    chr_status = db.Column(db.Text)
    num_person_id = db.Column(db.Numeric)
    str_createdby = db.Column(db.Text)
    dte_createddate = db.Column(db.DateTime)
    str_modifiedby = db.Column(db.Text)
    dte_modifieddate = db.Column(db.DateTime)


class Application(db.Model):
    __tablename__ = 'application'

    num_application_id = db.Column(db.Numeric, primary_key=True)
    str_application_name = db.Column(db.Text)
    str_createdby = db.Column(db.Text)
    dte_createddate = db.Column(db.DateTime)
    str_modifiedby = db.Column(db.Text)
    dte_modifieddate = db.Column(db.DateTime)
    chr_status = db.Column(db.Text)


class Module(db.Model):
    __tablename__ = 'module'

    str_module_id = db.Column(db.Text, primary_key=True)
    str_module_name = db.Column(db.Text)
    str_module_des = db.Column(db.Text)
    num_order = db.Column(db.Numeric)
    chr_status = db.Column(db.Text)
    str_createdby = db.Column(db.Text)
    dte_createddate = db.Column(db.DateTime)
    str_modifiedby = db.Column(db.Text)
    dte_modifieddate = db.Column(db.DateTime)
    num_application_id = db.Column(db.Numeric)
    str_icon = db.Column(db.Text)


class SubModule(db.Model):
    __tablename__ = 'submodule'

    str_submodule_id = db.Column(db.Text, primary_key=True)
    str_submodule_name = db.Column(db.Text)
    str_submodule_des = db.Column(db.Text)
    str_module_id = db.Column(db.Text, db.ForeignKey('module.str_module_id'), nullable=False)
    str_submodule_title = db.Column(db.Text)
    num_order = db.Column(db.Numeric)
    chr_status = db.Column(db.Text)
    str_createdby = db.Column(db.Text)
    dte_createddate = db.Column(db.DateTime)
    str_modifiedby = db.Column(db.Text)
    dte_modifieddate = db.Column(db.DateTime)
    str_action = db.Column(db.Text)


class OauthCredentials(db.Model):
    __tablename__ = 'oauth_credentials'

    num_oauth_cred_id = db.Column(db.Numeric, primary_key=True)

    str_oauth_cred_user = db.Column(db.Text)
    str_oauth_cred_password = db.Column(db.Text)

    str_createdby = db.Column(db.Text)
    dte_createddate = db.Column(db.DateTime)
    str_modifiedby = db.Column(db.Text)
    dte_modifieddate = db.Column(db.DateTime)


class Role(db.Model):
    __tablename__ = 'role'

    str_role_id = db.Column(db.Text, primary_key=True)
    str_role_name = db.Column(db.Text)
    str_rol_des = db.Column(db.Text)
    chr_status = db.Column(db.Text)
    str_createdby = db.Column(db.Text)
    dte_createddate = db.Column(db.DateTime)
    str_modifiedby = db.Column(db.Text)
    dte_modifieddate = db.Column(db.DateTime)


class RoleSubModule(db.Model):
    __tablename__ = 'role_submodule'

    str_submodule_id = db.Column(db.Text, db.ForeignKey('submodule.str_submodule_id'), nullable=False, primary_key=True)
    str_role_id = db.Column(db.Text, db.ForeignKey('role.str_role_id'), nullable=False)
    chr_status = db.Column(db.Text)
    str_createdby = db.Column(db.Text)
    dte_createddate = db.Column(db.DateTime)
    str_modifiedby = db.Column(db.Text)
    dte_modifieddate = db.Column(db.DateTime)


class UserRole(db.Model):
    __tablename__ = 'user_role'

    str_role_id = db.Column(db.Text, db.ForeignKey('role.str_role_id'), nullable=False, primary_key=True)
    chr_status = db.Column(db.Text)
    str_createdby = db.Column(db.Text)
    dte_createddate = db.Column(db.DateTime)
    str_modifiedby = db.Column(db.Text)
    dte_modifieddate = db.Column(db.DateTime)
    num_user_id = db.Column(db.Numeric, db.ForeignKey('user.num_user_id'), nullable=False)


class Session(db.Model):
    __tablename__ = 'session'
    sq_session_id = db.Column('sq_session_id',
                              metadata=base.metadata)

    num_session_id = db.Column(db.Numeric,
                               sq_session_id,
                               server_default=sq_session_id.next_value(),
                               primary_key=True)

    num_user_id = db.Column(db.Numeric, db.ForeignKey('user.num_user_id'), nullable=False)
    str_createdby = db.Column(db.Text)
    dte_createddate = db.Column(db.DateTime)
    str_modifiedby = db.Column(db.Text)
    dte_modifieddate = db.Column(db.DateTime)
    chr_state = db.Column(db.Text)


class FirebaseTokens(db.Model):
    __tablename__ = 'firebase_tokens'
    num_token_user_id = db.Column(db.Numeric, db.ForeignKey('user.num_user_id'), primary_key=True)
    str_token_android = db.Column(db.Text)
    str_token_ios = db.Column(db.Text)
    str_token_web = db.Column(db.Text)
    str_createdby = db.Column(db.Text)
    dte_createddate = db.Column(db.TIMESTAMP)
    str_modifiedby = db.Column(db.Text)
    dte_modifieddate = db.Column(db.TIMESTAMP)


class Token(db.Model):
    __tablename__ = 'token'
    sq_token_id = db.Column('sq_token_id',
                            metadata=base.metadata)
    num_token_id = db.Column(db.Numeric,
                             sq_token_id,
                             server_default=sq_token_id.next_value(),
                             primary_key=True)
    str_token_format = db.Column(db.Text)
    dte_token_date = db.Column(db.TIMESTAMP)
    num_session_id = db.Column(db.Numeric, db.ForeignKey('session.num_session_id'))
    str_createdby = db.Column(db.Text)
    dte_createddate = db.Column(db.TIMESTAMP)
    str_modifiedbye = db.Column(db.Text)
    dte_modifieddate = db.Column(db.TIMESTAMP)
