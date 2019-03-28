# -*- coding: utf-8 -*-
"""
Endi storage services
"""
import datetime
import hashlib
import os
import logging

from endi_payment.models import EndiPaymentArchiveSeal


class DefaultArchiveService(object):
    def __init__(self, context, request):
        self.request = request
        self.logger = logging.getLogger("endi_payment")

    def archive(self, history):
        self.logger.debug(u"Archiving history item {}".format(history.id))
        id_key = u"No persistent archive system has been used"
        result = EndiPaymentArchiveSeal(
            remote_identification_key=id_key,
            endi_payment_history_id=history.id
        )
        return result

    def is_archived(self, history):
        return False


class FileArchiveService(object):
    """
    FileStorageService simply logs the history in a file
    """
    settings_key = "endi_payment_archive_storage_path"

    def __init__(self, context, request):
        self.request = request
        self.storage_path = self.request.registry.settings[self.settings_key]
        today = datetime.date.today()
        self.filename = "payment_storage_{}_{}.csv".format(
            today.year, today.month
        )
        self.filepath = os.path.join(self.storage_path, self.filename)

    def archive(self, history):
        """
        Archive the given history entry

        :returns: A Sha1 sum of the output file content
        :rtype: str
        """
        with open(self.filepath, 'a') as fbuf:
            fbuf.write(history.serialize())

        with open(self.filepath, 'rb') as fbuf:
            id_key = hashlib.sha1(fbuf.read()).hexdigest()

        result = EndiPaymentArchiveSeal(
            remote_identification_key=id_key,
            endi_payment_history_id=history.id
        )
        return result

    def is_archived(self, history):
        """
        Check if the payment history entry has been archived

        :param obj history: The EndiPaymentHistory instance
        :rtype: bool
        """
        from endi_payment.database import HistorySessionFactory
        session = HistorySessionFactory()
        query = session.query(EndiPaymentArchiveSeal.id)
        query = query.filter(
            EndiPaymentArchiveSeal.endi_payment_history_id == history.id
        )
        return query.count() > 0

    @classmethod
    def check_settings(cls, settings):
        """
        Check the settings contains the endi_payment_archive_storage_path if
        this given service is configured in the ini file

        :raises: KeyError if the key is missing
        :raises: Exception if the directory doesn't exist
        """
        if cls.settings_key not in settings:
            raise KeyError(
                u"You should configure {} in your .ini file".format(
                    cls.settings_key
                )
            )

        storage_path = settings[cls.settings_key]
        if not os.path.isdir(storage_path):
            raise Exception(
                u"Invalid storage path {}".format(storage_path)
            )
