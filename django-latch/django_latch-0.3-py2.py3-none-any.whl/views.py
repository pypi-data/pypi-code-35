import logging

from functools import wraps

from http.client import HTTPException

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ImproperlyConfigured
from django.contrib import messages
from django.conf import settings
from django.db import transaction
from django.utils.translation import gettext_lazy as _

from latch.models import LatchSetup, UserProfile
from latch.forms import LatchPairForm, LatchUnpairForm

logger = logging.getLogger(__name__)


def latch_is_configured(view):
    """
    Decorator for views that check that Latch is configured in the site.
    If Latch is not configured, redirects to status page and shows
    a message.
    """

    @wraps(view)
    def wrapper(request, *args, **kwargs):
        try:
            LatchSetup.instance()
        except ImproperlyConfigured:
            messages.error(request, _("Latch is not configured"))
            return redirect(status)

        return view(request, *args, **kwargs)

    return wrapper


@latch_is_configured
@login_required
def pair(request, template_name="latch_pair.html"):
    """
    Pairs the current user with a given latch token ID.
    """
    if UserProfile.accountid(request.user) is not None:
        messages.error(request, _("Account is already paired"))
        return redirect(status)

    if request.method == "POST":
        return _process_pair_post(request)

    form = LatchPairForm()
    return render(request, template_name, {"form": form})


def _process_pair_post(request, template_name="latch_message.html"):
    form = LatchPairForm(request.POST)
    if form.is_valid():
        form.clean()
        try:
            latch_instance = LatchSetup.instance()
            account_id = latch_instance.pair(form.cleaned_data["latch_pin"])
            if "accountId" in account_id.get_data():
                UserProfile.save_user_accountid(
                    request.user, account_id.get_data()["accountId"]
                )
                messages.success(request, _("Account paired with Latch"))
            else:
                logger.warning(
                    "Pair process of user %s failed with error %s",
                    request.user,
                    account_id.get_error(),
                )
                messages.error(request, _("Account not paired with Latch"))

        except HTTPException as err:
            logger.exception("Couldn't connect with Latch service")

            msg = (
                _("Error pairing the account: %(error)s") % {"error": err}
                if settings.DEBUG
                else _("Error pairing the account")
            )

            messages.error(request, msg)

        return redirect(status)


@latch_is_configured
@login_required
def unpair(request, template_name="latch_unpair.html"):
    """
    Unpairs a given user.
    """
    if request.method == "POST":
        form = LatchUnpairForm(request.POST)
        if form.is_valid():
            return _process_unpair_post(request)
    else:
        form = LatchUnpairForm()
    return render(request, template_name, {"form": form})


def _process_unpair_post(request, template_name="latch_message.html"):
    try:
        acc_id = UserProfile.accountid(request.user)
        if acc_id:
            # Actual unpairing of the account is made in the signal
            # Using an atomic transaction rolls back if Latch service
            # is unreachable.
            with transaction.atomic():
                UserProfile.delete_user_account_id(acc_id)
            messages.success(request, _("Latch removed from your account"))
        else:
            messages.warning(request, _("Your account is not latched"))
    except UserProfile.DoesNotExist:
        messages.error(request, _("Your account has no profile"))
    except HTTPException as err:
        logger.exception("Couldn't connect with Latch service")

        msg = (
            _("Error unpairing the account: %(error)s") % {"error": err}
            if settings.DEBUG
            else _("Error unpairing the account")
        )

        messages.error(request, msg)

    return redirect(status)


@login_required
def status(request, template_name="latch_status.html"):
    """
    Gives information about Latch status, if it's configured,
    and data relative to the user making the request.
    """
    configured = True
    try:
        LatchSetup.instance()
    except ImproperlyConfigured:
        configured = False

    acc_id = None
    account_status = None
    try:
        if configured:
            acc_id = UserProfile.accountid(request.user)
            if acc_id:
                latch_instance = LatchSetup.instance()
                status_response = latch_instance.status(acc_id)
                data = status_response.get_data()["operations"]
                account_status = data[LatchSetup.appid()]["status"]

    except HTTPException:
        logger.exception("Couldn't connect with Latch service")
        return render(request, template_name, {"error": True})

    return render(
        request,
        template_name,
        {
            "configured": configured,
            "accountid": acc_id,
            "account_status": account_status,
        },
    )
