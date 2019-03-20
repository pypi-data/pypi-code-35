from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse

import cas

from . import settings
from .models import TUIDUser
from .util import update_user


def _get_service_url(request):
    if settings.TUID_FORCE_SERVICE_URL:
        if request.GET.get('next'):
            return settings.TUID_FORCE_SERVICE_URL + "?next=" + request.GET.get('next')
        return settings.TUID_FORCE_SERVICE_URL
    return 'https://' + request.get_host() + request.get_full_path()


def login(request):
    """
    Either logs a user in by verifying it's ticket, if no ticket is present the
    user is redirected to the CAS login.
    """

    casClient = cas.CASClient(
            version = 'CAS_2_SAML_1_0',

            service_url = _get_service_url(request),
            server_url  = settings.TUID_SERVER_URL,
    )

    ticket = request.GET.get('ticket')

    if not ticket:  #No ticket present redirect to CAS login
        return HttpResponseRedirect(casClient.get_login_url())
    
    #Ticket is present verify it.
    try:
        user, attr, _ = casClient.verify_ticket(ticket)
    #this happens if the response from the hrz server is empty
    #a simple solution is to reauthenticate the user
    except ParseError:
        request.session.flush()
        casClient = cas.CASClient(
            version = 'CAS_2_SAML_1_0',
            server_url  = settings.TUID_SERVER_URL,
        )
        next_page = casClient.get_logout_url(redirect_url=casClient.get_login_url())
        return HttpResponseRedirect(next_page)

    #Ticket seems to be valid save user and attributes in session
    if user:
        request.session['TUID'] = (user, attr)

        if settings.TUID_CREATE_USER:
            tuid_user , created = TUIDUser.objects.get_or_create(uid = user)
            update_user(tuid_user, user, attr)
            tuid_user.save()

        next_page = request.POST.get('next', request.GET.get('next',
            settings.TUID_LOGIN_DEFAULT_NEXT))
        return HttpResponseRedirect(next_page)

    else:
        raise PermissionDenied('Login failed.')


def logout(request, next_page=None):
    # Flush the session (clear it completely)
    request.session.flush()

    next_page = request.POST.get('next', request.GET.get('next',
            settings.TUID_LOGOUT_DEFAULT_NEXT))

    if request.GET.get('cas_logout'):
        casClient = cas.CASClient(
            version = 'CAS_2_SAML_1_0',

            #service_url = _get_service_url(request),
            server_url  = settings.TUID_SERVER_URL,
        )
        next_page = casClient.get_logout_url(redirect_url="https://" + request.get_host() + next_page)

    return HttpResponseRedirect(next_page)
