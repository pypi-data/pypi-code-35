from flask_admin.form import JSONField
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email
from wtforms.fields.html5 import EmailField
from flask_wtf import FlaskForm
from flask_security.forms import LoginForm
from wtforms.compat import string_types


class KeyValueValidator(DataRequired):
    def __call__(self, form, field):
        if (
            not field.data
            or isinstance(field.data, string_types)
            and not field.data.strip()
        ):
            field.errors[:] = []


class TaskContextForm(FlaskForm):
    key = StringField("Key", [KeyValueValidator()])
    value = StringField("Value", [KeyValueValidator()])
    context = JSONField("Context")


class SkidwardLoginForm(LoginForm):
    email = EmailField("Email ID", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
