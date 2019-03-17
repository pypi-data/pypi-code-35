# -*- coding: utf-8 -*-
#
#   ktug-hanyang-pua: KTUG HanYang PUA conversion table reader
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

from ..formats import MappingPackFormat
from ..models import Mapping
from ..table import split_table
from ..table import make_groups


logger = logging.getLogger(__name__)


def load_mappings_as_binary_table(input_fp):
    packFormat = MappingPackFormat()
    packSize = packFormat.structfmt.size

    # 그룹 갯수
    n_groups_struct = struct.Struct('<H')
    data = input_fp.read(n_groups_struct.size)
    if len(data) != n_groups_struct.size:
        raise Exception()
    n_groups = n_groups_struct.unpack(data)[0]

    # 그룹
    grouplengths_structfmt = '<{}H'.format(n_groups)
    grouplengths_struct = struct.Struct(grouplengths_structfmt)
    data = input_fp.read(grouplengths_struct.size)
    grouplengths = grouplengths_struct.unpack(data)

    # 매핑
    mappings = []
    for grouplength in grouplengths:
        for i in range(grouplength):
            data = input_fp.read(packSize)
            mapping = packFormat.parse(data)
            mappings.append(mapping)

    # 자모 문자열
    for mapping in mappings:
        target_struct = struct.Struct('<{}H'.format(mapping.target))
        data = input_fp.read(target_struct.size)
        if len(data) != target_struct.size:
            raise Exception()
        target = target_struct.unpack(data)
        source = (mapping.source,)
        yield Mapping(source=source, target=target, comment=None)

    remaining = input_fp.read()
    if len(remaining) != 0:
        logger.warning('remaining data: %s bytes', len(remaining))


def dump_mappings_as_binary_table(mappings, output_fp):
    mappingPackFormat = MappingPackFormat()

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
    output_fp.write(struct.pack('<H', n_groups))

    # 그룹
    grouplengths = tuple(
        end - start + 1 for start, end in groups
    )
    output_fp.write(
        struct.pack(
            '<{}H'.format(len(groups)),
            *grouplengths
        )
    )

    # 매핑
    targets = []
    for mapping, target, comment in mappings:
        targets.extend(target)
    for n_mappings, mapping in enumerate(mappings, 1):
        mapping, target, comment = mapping
        byteseq = mappingPackFormat.format(mapping)
        output_fp.write(byteseq)

    # 자모 문자열
    targetfmt = '<{}H'.format(len(targets))
    target = struct.pack(targetfmt, *targets)
    output_fp.write(target)
    return n_groups, n_mappings
