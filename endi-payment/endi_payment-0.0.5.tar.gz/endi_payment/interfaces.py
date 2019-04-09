# -*- coding: utf-8 -*-
from zope.interface import Interface


class IPaymentRecordHistoryService(Interface):
    """
    History manipulation tool iinterface for Payment action log
    """

    def record_action(self, action, invoice, payment):
        """
        History manipulation tool for Payment registration
        """
        pass


class IPaymentArchiveService(Interface):
    """
    Archive service is used to archive payment datas and secure its content
    integrity with the help of third-party services
    """

    def archive(self, history):
        """
        Stores a single history item

        :param obj history: A EndiPaymentHistory instance
        :rtype: class:`endi_payment.models.EndiPaymentArchiveSeal
        """
        pass

    def is_archived(self, history):
        """
        Check if the given history item has been archived remotely

        :param obj history: A EndiPaymentHistory instance
        :rtype: bool
        """
        pass
