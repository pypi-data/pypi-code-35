# Copyright (c) 2013, System Engineering Software Society
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
from sympathy.api import exporters
from sympathy.api import node as synode
import sylib.table_sources


class DataExportText(exporters.TextDataExporterBase):
    """Exporter for Text files."""
    EXPORTER_NAME = "Text"
    FILENAME_EXTENSION = "txt"

    def __init__(self, parameters):
        super().__init__(parameters)
        if 'encoding' not in parameters:
            parameters.set_string(
                'encoding', label='Output encoding',
                description='Encoding to use for created file',
                editor=synode.Util.combo_editor(
                    options=list(
                        sylib.table_sources.CODEC_LANGS.keys())),
                value='UTF-8')

    def parameter_view(self, node_context_input):
        return self._parameters['encoding'].gui()

    def create_filenames(self, input_list, filename, *args):
        return super(DataExportText, self).create_filenames(
            input_list, filename, *args)

    def export_data(self, in_sytext, fq_outfilename,
                    **kwargs):
        encoding = sylib.table_sources.CODEC_LANGS[
            self._parameters['encoding'].value]

        with open(fq_outfilename, 'w', encoding=encoding, newline="") as f:
            f.write(in_sytext.get())
