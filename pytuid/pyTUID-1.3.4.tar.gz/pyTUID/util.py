from json import loads as json_decode

from .models import TUIDUser
from . import settings

def update_user(tuid_user, cas_user, cas_attr):
    """Updates a TUID user object with the attributes returned from CAS"""
    tuid_user.uid = cas_user
    
    attr_dict = cas_attr

    mapping = settings.TUID_MAPPING
    for key in mapping:
        old_value = getattr(tuid_user, key)
        value = attr_dict.get(mapping[key], old_value)
        setattr(tuid_user, key, value)

