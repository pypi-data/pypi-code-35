# -*- coding: utf-8 -*-
import datetime
import csv
import hashlib
import StringIO

from sqlalchemy import (
    Column,
    Integer,
    BigInteger,
    String,
    DateTime,
    Text,
    ForeignKey,
)
from sqla_inspect.ascii import force_encoding
from autonomie_base.models.base import default_table_args
from endi_payment.database import ModelBase


class EndiPaymentHistory(ModelBase):
    __tablename__ = "endi_payment_history"
    __table_args__ = default_table_args
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime(), default=datetime.datetime.now)
    # ADD/UPDATE/DELETE
    action_type = Column(String(6))
    # Original payment instance id
    payment_id = Column(Integer, nullable=False)
    # Payment mode
    mode = Column(String(50))
    # The amount of the payment (* 10 000)
    amount = Column(BigInteger(), nullable=False)
    # The string identifying the bank remittance id
    bank_remittance_id = Column(String(255))
    # Date the payment has been received
    date = Column(DateTime(), nullable=False)
    # The invoice database item's id
    invoice_id = Column(Integer, nullable=False)
    # The invoice PDF sha1 hash that can be used to check pdf files
    invoice_pdf_file_hash = Column(String(255), nullable=False)
    # The bank CG account
    bank_cg = Column(String(120), default="")
    # The TVA associated to the recorded payment
    tva_value = Column(Integer, nullable=False)
    # The login of the user responsible for this modification
    user_login = Column(String(64), nullable=False)
    # The previous entry's md5sum
    previous_entry_hash = Column(String(255), nullable=False)

    def as_csv(self):
        """
        Returns a csv representation of this entry
        """
        data_list = [
            self.id,
            self.created_at.isoformat(),
            self.action_type,
            self.payment_id,
            self.mode,
            self.amount,
            self.bank_remittance_id,
            self.date.isoformat(),
            self.invoice_id,
            self.invoice_pdf_file_hash,
            self.bank_cg,
            self.tva_value,
            self.user_login,
            self.previous_entry_hash,
        ]
        line = StringIO.StringIO()

        data_list = [force_encoding(i, 'utf-8') for i in data_list]

        writer = csv.writer(line)
        writer.writerow(data_list)
        return line.getvalue()

    def serialize(self):
        """
        Serialize the current entry
        """
        return self.as_csv()

    def as_binary(self):
        """
        Builds a binary representation of the current model's csv string
        """
        return bytes(self.as_csv())

    def get_hash(self):
        return hashlib.sha1(self.as_binary()).hexdigest()


class EndiPaymentArchiveSeal(ModelBase):
    __tablename__ = "endi_payment_archive_seal"
    __table_args__ = default_table_args
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.datetime.now)
    remote_identification_key = Column(Text(), nullable=False)
    endi_payment_history_id = Column(ForeignKey('endi_payment_history.id'))
