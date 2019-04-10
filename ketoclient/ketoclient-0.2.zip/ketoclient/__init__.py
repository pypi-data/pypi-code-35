import logging

from checkallowed import CheckAllowed
from checkallowed import NoCheck
from Properties import ENABLE_RBAC
from Properties import POLICY_MANAGEMENT_URL

logging.basicConfig(
       format = '%(thread)d - %(name)s - %(levelname)s - %(message)s',
        level=logging.DEBUG)

if ENABLE_RBAC:
    checkAccess = CheckAllowed(POLICY_MANAGEMENT_URL).checkAccess

else:
    checkAccess = NoCheck().checkAccess

