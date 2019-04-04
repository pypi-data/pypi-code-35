# -*- coding: utf-8 -*-
# This file is part of markdown-aafigure.
# https://github.com/mbarkhau/markdown-aafigure
# (C) 2018 Manuel Barkhau <mbarkhau@gmail.com>
#
# SPDX-License-Identifier:    MIT

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import re
import json
import typing as typ
try:
    try:
        from urllib.parse import quote
    except ImportError:
        from urlparse import quote
except ImportError:
    from urllib import quote
from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor
from markdown.postprocessors import Postprocessor
import aafigure


def draw_aafigure(content, filename=None, output_fmt='svg'):
    if content.startswith('```aafigure'):
        content = content[len('```aafigure'):]
    if content.endswith('```'):
        content = content[:-len('```')]
    options = {'format': output_fmt}
    header, rest = content.split('\n', 1)
    if '{' in header and '}' in header:
        options.update(json.loads(header))
        content = rest
    for option_name in list(options.keys()):
        if option_name not in aafigure.aafigure.DEFAULT_OPTIONS:
            raise ValueError('Invalid Option: {}'.format(option_name))
        option_val = options[option_name]
        default_val = aafigure.aafigure.DEFAULT_OPTIONS[option_name]
        default_type = type(default_val)
        if not isinstance(option_val, default_type):
            options[option_name] = default_type(option_val)
    visitor, output = aafigure.render(content, options=options)
    return output.getvalue()


def fig2svg_uri(fig_text):
    img_data = draw_aafigure(fig_text, output_fmt='svg')
    img_text = img_data.decode('utf-8')
    img_text = quote(img_text.replace('\n', '').replace('>    <', '/><'))
    return 'data:image/svg+xml;utf8,{0}'.format(img_text)


class AafigureExtension(Extension):

    def __init__(self, **kwargs):
        self.config = {'format': ['svg', 'Format to use (svg/png)']}
        self.images = {}
        super(AafigureExtension, self).__init__(**kwargs)

    def reset(self):
        self.images.clear()

    def extendMarkdown(self, md, *args, **kwargs):
        preproc = AafigurePreprocessor(md, self)
        md.preprocessors.register(preproc, name=
            'aafigure_fenced_code_block', priority=50)
        postproc = AafigurePostprocessor(md, self)
        md.postprocessors.register(postproc, name=
            'aafigure_fenced_code_block', priority=0)
        md.registerExtension(self)


class AafigurePreprocessor(Preprocessor):
    RE = re.compile('^```aafigure')

    def __init__(self, md, ext):
        super(AafigurePreprocessor, self).__init__(md)
        self.ext = ext

    def run(self, lines):
        is_in_fence = False
        out_lines = []
        block_lines = []
        for line in lines:
            if is_in_fence:
                block_lines.append(line)
                if '```' not in line:
                    continue
                is_in_fence = False
                fig_text = '\n'.join(block_lines)
                del block_lines[:]
                data_uri = fig2svg_uri(fig_text)
                data_uri_id = id(data_uri)
                marker = "<p id='aafig{0}'>aafig{1}</p>".format(data_uri_id,
                    data_uri_id)
                tag_text = "<p><img src='{0}' /></p>".format(data_uri)
                out_lines.append(marker)
                self.ext.images[marker] = tag_text
            elif self.RE.match(line):
                is_in_fence = True
                block_lines.append(line)
            else:
                out_lines.append(line)
        return out_lines


class AafigurePostprocessor(Postprocessor):

    def __init__(self, md, ext):
        super(AafigurePostprocessor, self).__init__(md)
        self.ext = ext

    def run(self, text):
        for marker, img in self.ext.images.items():
            wrapped_marker = '<p>' + marker + '</p>'
            if wrapped_marker in text:
                text = text.replace(wrapped_marker, img)
            elif marker in text:
                text = text.replace(marker, img)
        return text
