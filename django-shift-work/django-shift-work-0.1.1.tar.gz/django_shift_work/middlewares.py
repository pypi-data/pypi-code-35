from django.utils import timezone
from django.conf import settings
from datetime import timedelta, datetime
import abc


class BaseShiftWorkMiddleWare(abc.ABC):

    variable_name = 'shift'

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        now = timezone.localtime()
        obj = self.get_obj(now)
        setattr(request, self.variable_name, obj)

        response = self.get_response(request)
        return response

    @abc.abstractmethod
    def get_obj(self, now):
        pass


class ShiftWorkMiddleWare(BaseShiftWorkMiddleWare):

    def get_obj(self, now):
        date_now = now.date()
        tzinfo = now.tzinfo
        shift_plan = getattr(settings, 'SHIFT_PLAN', None)

        if shift_plan is None:
            return

        ret = {}

        for key, boundary in shift_plan.items():
            start = datetime.combine(date_now, boundary[0], tzinfo=tzinfo)
            end = datetime.combine(date_now, boundary[1], tzinfo=tzinfo)

            if end < start:
                if now >= start:
                    end += timedelta(days=1)
                else:
                    start -= timedelta(days=1)

            if start <= now < end:
                ret['name'] = key
                ret['start'] = start
                ret['end'] = end
                break


        return ret
