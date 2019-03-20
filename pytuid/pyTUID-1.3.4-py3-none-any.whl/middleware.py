from django.utils.deprecation import MiddlewareMixin

from .models import TUIDUser
from .util import update_user
from . import settings

class TUIDMiddleware(MiddlewareMixin, object):

    def process_request(self, request):

        if 'TUID' in request.session.keys():
            if settings.TUID_CREATE_USER:
                request.TUIDUser = TUIDUser.objects.filter(uid=request.session['TUID'][0]).first()
            else:
                tuid_user = TUIDUser()
                update_user(tuid_user, *request.session['TUID'])
                request.TUIDUser = tuid_user
        else:
            request.TUIDUser = None
