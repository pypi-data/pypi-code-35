#  Copyright (c) 2013-2015, Enthought, Inc.
#  All rights reserved.
#
#  This software is provided without warranty under the terms of the BSD
#  license included in LICENSE and may be redistributed only under the
#  conditions described in the aforementioned license.  The license is also
#  available online at https://opensource.org/licenses/BSD-3-Clause.
import warnings

warnings.warn(
    "hatcher.core.repository has moved to hatcher.core.v0.repository",
    DeprecationWarning)

from hatcher.core.v0.repository import (
    Repository as BaseRepository,
    SinglePlatformRepository as BaseSinglePlatformRepository,
)
from .model_registry import ModelRegistry


class Repository(BaseRepository):

    def __init__(self, organization_name, name, url_handler):
        super(Repository, self).__init__(
            organization_name, name, url_handler, ModelRegistry(api_version=0))


class SinglePlatformRepository(BaseSinglePlatformRepository):

    def __init__(self, repository, platform, url_handler):
        super(SinglePlatformRepository, self).__init__(
            repository, platform, url_handler, ModelRegistry(api_version=0))
