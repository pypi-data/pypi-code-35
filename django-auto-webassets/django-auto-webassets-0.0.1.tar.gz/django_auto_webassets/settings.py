# Copyright (c) 2016-2019, Thomas Hartmann
#
# This file is part of the OBOB Subject Database Project,
# see: https://gitlab.com/obob/obob_subjectdb/
#
#    obob_subjectdb is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    obob_subjectdb is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with obob_subjectdb. If not, see <http://www.gnu.org/licenses/>.


class DJANGO_AUTO_WEBASSETS_Settings(object):
    """Container for this modules settings including defaults."""

    defaults = {
        'WEBASSETS_JS_FOLDER': 'js_for_views',
        'WEBASSETS_PATH_TO_REQUIREJS': 'requirejs/require.js',
        'WEBASSETS_PATH_TO_REQUIREJS_CFG': 'requirejs_cfg.js',
        'WEBASSETS_SCRAMBLE_OUT_JS': False,
        'WEBASSETS_R_JS': 'node_modules/.bin/r.js',
        'WEBASSETS_OPTIMIZE': True,
    }

    def __init__(self):
        """Load our settings from django.conf.settings, applying defaults."""
        from django.conf import settings

        for name, default in self.defaults.items():
            value = getattr(settings, name, default)
            setattr(self, name, value)
