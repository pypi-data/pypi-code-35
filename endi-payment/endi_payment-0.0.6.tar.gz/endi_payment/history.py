# -*- coding: utf-8 -*-
"""
Payment History service, records modification done on payments
"""
import logging

from endi_payment.interfaces import IPaymentArchiveService
from endi_payment.models import EndiPaymentHistory


class HistoryLogService(object):
    """
    History service that's only logging the actions in a log file.

    To be used in dev mode
    """
    def __init__(self, context, request):
        self.request = request
        self.logger = logging.getLogger("endi_payment")
        self.archive_service = request.find_service(
            IPaymentArchiveService
        )

    def record(self, action, invoice, payment):
        self.logger.debug("Recording an action")
        self.logger.debug("Action : %s" % action)
        self.logger.debug("User : %s" % self.request.user)
        self.logger.debug("Invoice id : %s" % invoice.id)


class HistoryDBService(HistoryLogService):
    """
    Service logging datas in a database using a specific connexion
    """

    def get_previous_entry_hash(self, dbsession):
        """
        Produce a hash of the csv representation of the previous history entry

        :param obj dbsession: The current database session
        :rtype: str
        """
        previous_entry = dbsession.query(
            EndiPaymentHistory
        ).order_by(EndiPaymentHistory.id).first()

        if previous_entry:
            result = previous_entry.get_hash()
        else:
            result = ""
        return result

    def record(self, action, invoice, payment):
        self.logger.info("Recording an action")
        self.logger.info("Action : %s" % action)
        self.logger.info("User : %s" % self.request.user)
        self.logger.info("Invoice id : %s" % invoice.id)
        self.logger.info("It's production mode")

        from endi_payment.database import LocalSessionContext
        with LocalSessionContext() as dbsession:
            previous_entry_hash = self.get_previous_entry_hash(dbsession)
            record = EndiPaymentHistory(
                action_type=action,
                payment_id=payment.id,
                mode=payment.mode,
                amount=payment.amount,
                bank_remittance_id=payment.bank_remittance_id,
                date=payment.date,
                invoice_id=invoice.id,
                invoice_pdf_file_hash=invoice.pdf_file_hash,
                bank_cg=payment.bank.compte_cg,
                tva_value=payment.tva.value,
                user_login=self.request.user.login.login,
                previous_entry_hash=previous_entry_hash,
            )
            dbsession.add(record)
            dbsession.flush()
            archive_seal = self.archive_service.archive(record)
            if archive_seal is not None:
                dbsession.add(archive_seal)
            else:
                self.logger.debug(u"Not archive seal was produced")

        self.logger.info(u"Recorded")
