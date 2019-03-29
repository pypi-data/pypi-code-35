# -*- coding: utf-8 -*-
# This file is part of Adiczion's Tryton Module.
# The COPYRIGHT and LICENSE files at the top level of this repository
# contains the full copyright notices and license terms.
from trytond.pool import Pool
from . import sale


def register():
    Pool.register(
        sale.SaleLine,
        module='sale_discount', type_='model')
