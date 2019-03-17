# -*- coding: utf-8 -*-
#
#   ktug-hanyang-pua: KTUG HanYang PUA conversion table reader
#   Copyright (C) 2015-2019 mete0r <mete0r@sarangbang.or.kr>
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Affero General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Affero General Public License for more details.
#
#   You should have received a copy of the GNU Affero General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
from __future__ import absolute_import
from __future__ import print_function
from struct import Struct
import sys

from parsec import joint
from parsec import optional
from parsec import regex
from parsec import sepBy
from parsec import string
from parsec import spaces
from parsec import try_choice

from .models import Comment
from .models import Empty
from .models import EMPTY
from .models import Mapping
from .models import Node


PY3 = sys.version_info.major == 3

if PY3:
    unichr = chr


class IterableFormat(object):

    __slots__ = (
        'itemFormat',
    )

    def __init__(self, itemFormat):
        self.itemFormat = itemFormat

    def __repr__(self):
        return '{}({})'.format(
            type(self).__name__,
            self.itemFormat,
        )

    def format(self, iterable):
        itemFormat = self.itemFormat
        for item in iterable:
            yield itemFormat.format(item)

    def parse(self, iterable):
        itemFormat = self.itemFormat
        for item in iterable:
            yield itemFormat.parse(item)


class LineFormat(object):

    __slots__ = (
        'parse',
    )

    def __init__(self):
        #
        # Parser combinators
        #

        SPACES = spaces()
        optional_spaces = optional(SPACES)
        empty = SPACES.parsecmap(lambda x: EMPTY)
        comment = string('%%%') >> regex('.*')
        comment = comment.parsecmap(Comment)
        codepoint_hex = regex('[0-9A-F]+')
        codepoint_hex = codepoint_hex.parsecmap(lambda x: int(x, 16))
        codepoint = string('U+') >> codepoint_hex
        codepoint_seq = sepBy(codepoint, SPACES)
        codepoint_seq = codepoint_seq.parsecmap(tuple)
        arrow = string('=>')
        arrow = optional_spaces >> arrow << optional_spaces
        mapping = joint(
            codepoint_seq << arrow,
            codepoint_seq,
            optional(comment),
        )
        mapping = mapping.parsecmap(lambda x: Mapping(x[0], x[1], x[2]))
        line = try_choice(
            mapping,
            try_choice(
                comment,
                empty,
            )
        )
        self.parse = line.parse

    def __repr__(self):
        return '{}()'.format(
            type(self).__name__,
        )

    def format(self, line):
        if isinstance(line, Mapping):
            return self.format_mapping(line)
        elif isinstance(line, Comment):
            return self.format_comment(line)
        elif isinstance(line, Empty):
            return ''
        else:
            raise TypeError(line)

    def format_mapping(self, mapping):
        source, target, comment = mapping
        mapping = '{} => {}'.format(
            ' '.join(
                'U+{:4X}'.format(codepoint)
                for codepoint in source
            ),
            ' '.join(
                'U+{:4X}'.format(codepoint)
                for codepoint in target
            ),
        )
        mapping = mapping.rstrip()
        if comment is None:
            return mapping
        return '{} {}'.format(
            mapping, self.format_comment(comment),
        )

    def format_comment(self, comment):
        return '%%%{}'.format(comment.text)


class MappingPackFormat(object):

    __slots__ = (
        'structfmt',
    )

    def __init__(self):
        self.structfmt = Struct('<HH')

    def format(self, mapping):
        source = mapping.source
        target = mapping.target
        return self.structfmt.pack(source, target)

    def parse(self, byteseq):
        if len(byteseq) != self.structfmt.size:
            raise ValueError(len(byteseq))
        source, target = self.structfmt.unpack(byteseq)
        return Mapping(
            source=source,
            target=target,
            comment=None,
        )


class MappingDictFormat(object):

    __slots__ = (
        'comment',
    )

    def __init__(self, comment=True):
        self.comment = comment

    def format(self, mapping):
        d = {
            'source': unichr(mapping.source),
            'target': u''.join(unichr(code) for code in mapping.target),
        }
        if self.comment:
            d['comment'] = mapping.comment
        return d

    def parse(self, d):
        source = ord(d['source'])
        target = tuple(ord(c) for c in d['target'])
        if self.comment:
            comment = d['comment']
        else:
            comment = None
        return Mapping(
            source=source,
            target=target,
            comment=comment,
        )


class NodePackFormat(object):

    __slots__ = (
        'structfmt',
    )

    def __init__(self):
        self.structfmt = Struct(
            '<hHH',
        )

    def format(self, node):
        node = (
            node.parent,
            node.source or 0,
            node.target or 0,
        )
        return self.structfmt.pack(*node)

    def parse(self, byteseq):
        parent, source, target = self.structfmt.unpack(byteseq)
        return Node(
            parent=parent,
            source=source or None,
            target=target or None,
        )


class NodeDictFormat(object):

    def format(self, node):
        return {
            'parent': node.parent,
            'source': node.source,
            'target': node.target,
        }

    def parse(self, form):
        return Node(**form)
