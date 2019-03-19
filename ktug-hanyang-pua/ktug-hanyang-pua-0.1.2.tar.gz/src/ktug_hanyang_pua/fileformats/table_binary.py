# -*- coding: utf-8 -*-
#
#   ktug-hanyang-pua: KTUG Hanyang PUA table reader/writer
#   Copyright (C) 2015-2017 mete0r <mete0r@sarangbang.or.kr>
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
import logging
import struct

from ..models import Mapping
from ..table import split_table
from ..table import make_groups


logger = logging.getLogger(__name__)


ushort = struct.Struct('<H')
ushort_pair = struct.Struct('<2H')


def read_struct(fp, struct):
    data = fp.read(struct.size)
    return struct.unpack(data)


def write_struct(fp, struct, tpl):
    data = struct.pack(*tpl)
    fp.write(data)


def load_mappings_as_binary_table(input_fp):

    # 그룹 갯수
    n_groups = read_struct(input_fp, ushort)[0]

    # 그룹
    groupheaders = [
        read_struct(input_fp, ushort_pair)
        for i in range(n_groups)
    ]

    # 매핑
    mappings = []
    mappingtargetlen_struct = struct.Struct('<H')
    for groupstart, grouplength in groupheaders:
        for i in range(grouplength):
            source = groupstart + i
            targetlen = read_struct(input_fp, mappingtargetlen_struct)[0]
            mapping = Mapping(
                source=source,
                target=targetlen,
                comment=None,
            )
            mappings.append(mapping)

    # 자모 문자열
    for mapping in mappings:
        target_struct = struct.Struct('<{}H'.format(mapping.target))
        target = read_struct(input_fp, target_struct)
        source = (mapping.source,)
        yield Mapping(source=source, target=target, comment=None)

    remaining = input_fp.read()
    if len(remaining) != 0:
        logger.warning('remaining data: %s bytes', len(remaining))


def dump_mappings_as_binary_table(mappings, output_fp):

    mappings = (
        Mapping(
            source=m.source[0],
            target=m.target,
            comment=m.comment,
        )
        for m in mappings
    )
    mappings = sorted(mappings)
    mappings = list(mappings)
    groups = make_groups(m.source for m in mappings)
    mappings = split_table(mappings)
    mappings = list(mappings)

    # 그룹 갯수
    n_groups = len(groups)
    write_struct(output_fp, ushort, (n_groups, ))

    # 그룹
    for groupstart, groupend in groups:
        grouplength = groupend - groupstart + 1
        write_struct(output_fp, ushort_pair, (groupstart, grouplength))

    # 매핑
    targets = []
    for mapping, target, comment in mappings:
        targets.extend(target)
    for n_mappings, mapping in enumerate(mappings, 1):
        mapping, target, comment = mapping
        write_struct(output_fp, ushort, (mapping.target, ))  # target length

    # 자모 문자열
    targetfmt = '<{}H'.format(len(targets))
    target = struct.pack(targetfmt, *targets)
    output_fp.write(target)
    return n_groups, n_mappings
