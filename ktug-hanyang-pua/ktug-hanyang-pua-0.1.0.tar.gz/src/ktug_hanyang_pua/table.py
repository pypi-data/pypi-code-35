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

from .models import Mapping


def switch_source_and_targets(mappings):
    for mapping in mappings:
        yield switch_source_and_target_of_mapping(mapping)


def switch_source_and_target_of_mapping(mapping):
    if isinstance(mapping, Mapping):
        return Mapping(
            source=mapping.target,
            target=mapping.source,
            comment=mapping.comment,
        )
    return mapping


def split_table(mappings):
    for mapping in mappings:
        target = mapping.target
        comment = mapping.comment
        mapping = Mapping(
            source=mapping.source,
            target=len(target),
            comment=len(comment or ''),
        )
        yield mapping, target, comment


def make_groups(codes):
    groups = []
    current_group = None
    for code in codes:
        if current_group is None:
            current_group = [code, code]
        elif current_group[-1] + 1 == code:
            current_group[-1] = code
        else:
            groups.append(current_group)
            current_group = [code, code]

    if current_group is not None:
        groups.append(current_group)

    return groups
