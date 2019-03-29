# -*- coding: utf-8 -*-
# This file is part of Adiczion's Tryton Module.
# The COPYRIGHT and LICENSE files at the top level of this repository
# contains the full copyright notices and license terms.
from trytond.pool import Pool, PoolMeta
from trytond.model import Workflow, ModelView, fields
from trytond.transaction import Transaction
from decimal import Decimal
from trytond.pyson import Eval
from sql import Null
import logging

_logger = logging.getLogger(__name__)

__all__ = ['SaleLine']


class SaleLine(metaclass=PoolMeta):
    __name__ = 'sale.line'

    discount = fields.Numeric('Discount (%)',
        digits=(16, Eval('_parent_sale', {}).get('currency_digits', 2)),
        states={
            'invisible': Eval('type') != 'line',
        },
        depends=['type','unit_price', 'quantity', 'amount'],
        help="Discount on the line: "
            "Unit Price = Base Price x (1 - Discount)")
    base_price = fields.Numeric('Base Price (Tax excl.)', digits=(16, 4),
        states={
            'invisible': Eval('type') != 'line',
            },
        depends=['type'],
        help="Unit price of the product excluding taxes and discount.")


    @classmethod
    def __register__(cls, module_name):
        """
        Set base_price with their correct value.

        :param module_name: Module name
        :return: Nothing
        """
        sql_table = cls.__table__()
        super(SaleLine, cls).__register__(module_name)
        cursor = Transaction().connection.cursor()
        table = cls.__table_handler__(module_name)

        # Migration for existing data
        # Get the line
        cursor.execute(*sql_table.select(sql_table.id,
            where=(sql_table.base_price == Null)))
        res = [x[0] for x in cursor.fetchall()]
        if res:
            # Update the original price
            cursor.execute(*sql_table.update(
                columns=[sql_table.base_price, sql_table.discount],
                values=[sql_table.unit_price, Decimal(0.0)],
                where=sql_table.id.in_(res)))

    @staticmethod
    def default_discount():
        return Decimal(0.0)

    @fields.depends('unit_price', 'discount', 'base_price')
    def _compute_unit_price(self):
        if self.base_price:
            self.unit_price = self.base_price * \
                (1 - (Decimal(str(self.discount or '0.0')) * Decimal(0.01)))
            if self.unit_price:
                self.unit_price = self.unit_price.quantize(
                    Decimal(1) / 10 ** self.__class__.unit_price.digits[1])

    @fields.depends('discount', 'type', 'quantity', 'unit', 'amount',
        methods=['_compute_unit_price', 'on_change_with_amount'])
    def on_change_discount(self):
        if self.discount:
            self._compute_unit_price()
            self.amount = self.on_change_with_amount()

    @fields.depends('discount', 'unit_price', 'base_price',
        methods=['_compute_unit_price'])
    def on_change_quantity(self):
        super(SaleLine, self).on_change_quantity()
        if not self.product:
            return
        self.base_price = self.unit_price
        if self.discount:
            self._compute_unit_price()

    @fields.depends('discount', 'unit_price', 'product', 'base_price',
        methods=['_get_context_sale_price'])
    def on_change_product(self):
        super(SaleLine, self).on_change_product()
        if not self.product:
            return
        self.discount = Decimal(0.0)
        self.base_price = self.unit_price

    @fields.depends('sale', '_parent_sale.currency', '_parent_sale.party',
        '_parent_sale.sale_date', 'unit', 'product', 'taxes', 'discount')
    def on_change_unit_price(self):
        if not self.product:
            return
        self.discount = Decimal(0.0)
