# This file is a part of the AnyBlok project
#
#    Copyright (C) 2015 Georges Racinet <gracinet@anybox.fr>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.
from anyblok import Declarations
from anyblok.column import String


@Declarations.register(Declarations.Model.Authorization)
class ModelPermissionGrant:
    """Default model for ModelBasedAuthorizationRule"""

    model = String(primary_key=True)
    principal = String(primary_key=True)
    permission = String(primary_key=True)
