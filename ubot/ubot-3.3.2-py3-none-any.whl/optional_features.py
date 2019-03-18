class OptionalFeatures:
    async def check_update(self, update, update_type, update_flavor):
        """
        To be implemented by user, called as validator before an update is handled, if the return value is not True the
        update is not queued

        :param update: The update (a dict) received from the Telegram webhook
        :return: True/Other value
        """
        return True
