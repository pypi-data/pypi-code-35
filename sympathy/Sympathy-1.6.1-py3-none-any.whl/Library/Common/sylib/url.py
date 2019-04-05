# Copyright (c) 2018 System Engineering Software Society
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the System Engineering Software Society nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.
# IN NO EVENT SHALL SYSTEM ENGINEERING SOFTWARE SOCIETY BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
import six
import requests
import tempfile
from sympathy.api import exceptions


def download_datasource(datasource, filename=None, tempfile_kwargs=None):
    assert filename or tempfile_kwargs
    if datasource.decode_type() == datasource.modes.url:
        url = datasource['path']
        scheme = six.moves.urllib.parse.urlparse(url).scheme
        if six.moves.urllib.parse.urlparse(url).scheme in [
                'http', 'https']:
            headers = datasource['env']
            r = requests.get(url, headers=headers)

            if r.status_code != requests.codes.ok:
                raise exceptions.SyDataError(
                    'Failed, getting optaining the requested data')

            if filename:
                file_obj = open(filename, 'w+b')
            elif tempfile_kwargs:
                file_obj = tempfile.NamedTemporaryFile(
                    delete=False, **tempfile_kwargs)

            with file_obj as http_temp:
                for chunk in r.iter_content(chunk_size=1024):
                    http_temp.write(chunk)

            result_filename = http_temp.name
            datasource = type(datasource)()
            datasource.encode_path(result_filename)
        else:
            raise exceptions.SyDataError(
                "Datasource URL contains unhandled scheme: {}. "
                "Currently, http and https are supported.".
                format(scheme))
    return datasource
