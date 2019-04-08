#
# Copyright (c) 2016, Grigoriy Kramarenko
# All rights reserved.
# This file is distributed under the same license as the current project.
#
from datetime import datetime, date, time
from decimal import Decimal
from json import JSONEncoder as OrigJSONEncoder
from types import GeneratorType
from uuid import UUID

from django.utils.encoding import force_text
from django.utils.functional import Promise
from django.utils.timezone import is_aware

from directapps.conf import USE_TIME_ISOFORMAT


class JSONEncoder(OrigJSONEncoder):
    """
    A subclass of JSONEncoder that can encode date / time, numeric type,
    generators, lazy translation objects, and exceptions. Almost like in
    Django, but with additions and a little faster.
    """
    use_time_isoformat = USE_TIME_ISOFORMAT

    def default(self, o):
        # See "Date Time String Format" in the ECMA-262 specification.
        if isinstance(o, datetime):
            r = o.isoformat()
            if not self.use_time_isoformat and o.microsecond:
                r = r[:23] + r[26:]
            if r.endswith('+00:00'):
                r = r[:-6] + 'Z'
            return r
        elif isinstance(o, date):
            return o.isoformat()
        elif isinstance(o, time):
            iso = self.use_time_isoformat
            if not iso and is_aware(o):
                raise ValueError("JSON can't represent timezone-aware times.")
            r = o.isoformat()
            if not iso and o.microsecond:
                r = r[:12]
            if iso and r.endswith('+00:00'):
                r = r[:-6] + 'Z'
            return r
        elif isinstance(o, Decimal):
            return str(o)
        elif isinstance(o, UUID):
            return str(o)
        elif isinstance(o, Exception):
            return force_text(o)
        elif isinstance(o, Promise):
            return force_text(o)
        elif isinstance(o, GeneratorType):
            return list(o)
        else:
            return OrigJSONEncoder.default(self, o)
