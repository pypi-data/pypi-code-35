# -*- coding: utf-8 -*-
import logging
import deform
import colander
from pyramid.security import NO_PERMISSION_REQUIRED
from pyramid.httpexceptions import HTTPFound, HTTPForbidden

from endi.forms.user.login import (
    get_auth_validator,
    AuthSchema,
)
from endi.views.auth import (
    connect_user,
)

logger = logging.getLogger(__name__)


class OIDCSchema(AuthSchema):
    """
    Schema used for openid connect implementation

    http://openid.net/specs/openid-connect-core-1_0.html#AuthRequest

    Only the field we think usefull are implemented here
    """
    csrf_token = colander.SchemaNode(
        colander.String(),
        widget=deform.widget.HiddenWidget(),
    )
    scope = colander.SchemaNode(
        colander.String(),
        widget=deform.widget.HiddenWidget(),
    )
    response_type = colander.SchemaNode(
        colander.String(),
        widget=deform.widget.HiddenWidget(),
    )
    client_id = colander.SchemaNode(
        colander.String(),
        widget=deform.widget.HiddenWidget(),
    )
    redirect_uri = colander.SchemaNode(
        colander.String(),
        widget=deform.widget.HiddenWidget(),
    )

    state = colander.SchemaNode(
        colander.String(),
        widget=deform.widget.HiddenWidget(),
        missing=colander.drop,
    )
    nonce = colander.SchemaNode(
        colander.String(),
        widget=deform.widget.HiddenWidget(),
        missing=colander.drop,
    )


REQUIRED_FIELDS = (
    "scope",
    "response_type",
    "client_id",
    "redirect_uri",
)
OPTIONNAL_FIELDS = ('state', 'nonce',)


def get_oidc_datas(request_parameters):
    """
    Return a dict for form datas population

    :param dict request_parameters: A dictionnary containing the parameters we
    want to rerturn
    :returns: The param dict
    :rtype: dict
    """
    logger.debug(request_parameters)
    logger.debug("client_id" in request_parameters)
    result = {}
    for key in REQUIRED_FIELDS:
        if key == 'scope' and "openid" not in request_parameters[key]:
            raise KeyError("Invalid scope declaration")
        result[key] = request_parameters[key]
    for key in OPTIONNAL_FIELDS:
        if key in request_parameters:
            result[key] = request_parameters[key]
    return result


def login_view(request):
    """
    View for login handling
    """
    schema = OIDCSchema(title="", validator=get_auth_validator())
    schema = schema.bind(request=request)
    form = deform.Form(
        schema,
        buttons=(deform.Button(title='Connexion'),),
        formid="authentication",
    )

    if 'submit' in request.POST:
        post_params = request.POST.items()
        try:
            form_datas = form.validate(post_params)
            logger.debug("Form datas are valid")
        except deform.ValidationFailure as e:
            logger.exception(e.error)
            logger.exception(e.cstruct)
            return dict(form=e.render())

        logger.debug(u" + '{0}' has been authenticated".format(
            form_datas['login'])
        )
        connect_user(request, form_datas)

        # The user is connected, we return him to the original page with the
        # provided parameters (original page should be /authorize)
        nextpage = form_datas['nextpage']
        request_params = get_oidc_datas(form_datas)
        route = request.route_path(nextpage, _query=request_params)
        logger.debug("Redirecting to %s" % route)
        return HTTPFound(location=route, headers=request.response.headers)

    form_datas = get_oidc_datas(request.params)
    form_datas['nextpage'] = request.GET['nextpage']
    form_datas['csrf_token'] = request.session.get_csrf_token()

    html_form = form.render(form_datas)

    return dict(
        title='enDI',
        html_form=html_form,
    )


def forbidden_view(request):
    """
    403 page
    """
    logger.debug("Forbidden view")
    path = request.matched_route.name
    req_params = request.params.items()
    req_params += (('nextpage', path),)
    loc = request.route_path('/login', _query=req_params)
    return HTTPFound(loc)


def includeme(config):
    """
    Add the views and routes to the current configuration
    """
    config.add_view(
        login_view,
        route_name='/login',
        permission=NO_PERMISSION_REQUIRED,
        require_csrf=True,
        layout='login',
        renderer='endi:templates/login.mako',
    )
    config.add_view(
        forbidden_view,
        context=HTTPForbidden,
        permission=NO_PERMISSION_REQUIRED,
    )
