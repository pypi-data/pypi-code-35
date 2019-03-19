# -*- coding: utf-8 -*-
import colander
import deform

from colanderalchemy import SQLAlchemySchemaNode
from endi.forms.lists import BaseListsSchema
from endi.forms import mail_validator
from endi.forms.widgets import CleanMappingWidget

from endi_oidc_provider.config import SCOPES
from endi_oidc_provider.models import OidcClient


def join_scopes(scope_list):
    """
    Join scope values with spaces (as they are stored in database)
    """
    return " ".join(scope_list)


def get_client_schema():
    """
    Return the colander Schema for OidcClient add/edit
    """
    schema = SQLAlchemySchemaNode(
        OidcClient,
        includes=(
            'id', 'name', 'admin_email', 'scopes', 'logout_uri', 'redirect_uris'
        )
    )
    schema['admin_email'].widget = deform.widget.TextInputWidget(
        input_prepend='@'
    )
    schema['admin_email'].validator = mail_validator()

    schema['scopes'].typ = colander.Set()
    schema['scopes'].widget = deform.widget.CheckboxChoiceWidget(
        values=SCOPES,
    )
    schema['scopes'].preparer = join_scopes

    schema['redirect_uris'].children[0].widget = CleanMappingWidget()
    schema['redirect_uris'].widget = deform.widget.SequenceWidget(min_len=1)
    schema['redirect_uris'].validator = colander.Length(
        1,
        min_err=u"Veuillez saisir au moins une valeur",
    )
    return schema


def get_client_list_schema():
    """
    Build the OidcClient list schema
    """
    schema = BaseListsSchema().clone()
    schema['search'].description = u"Nom ou client ID"
    return schema
