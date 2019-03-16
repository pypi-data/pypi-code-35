class OptionalFeatures(object):

    async def check_update(self, update, update_type, update_flavor):
        """
        To be implemented by user, called as validator before an update is handled, if the return value is not True the
        update is not queued

        :param update: The update (a dict) received from the Telegram webhook
        :return: True/Other value
        """
        return True

    async def on_exception(self, update, exception, when):
        """
         To be implemented by user, called after an exception (e.g. to report it on a telegram chat, to send you a mail
         with the error, ecc..)

        :param update: The update (a dict) received from the Telegram webhook
        :param exception: The exception object
        :param when: A string containing info about when the Exception was thrown
        """
        pass
