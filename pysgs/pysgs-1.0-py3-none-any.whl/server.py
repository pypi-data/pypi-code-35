"""
Use smtplib to send message through SendGrid
"""
import smtplib
from pysgs.exceptions import SGSError


class Server:
    """
    Server class to send messages
    """

    def __init__(self, api_key=''):
        """
        Keyword Arguments:
            api_key {str} -- SendGrid Api Key (default: {''})
        """

        # SendGrid Login
        self.api_user = 'apikey'
        self.api_key = api_key

        # SMTP
        self.smtp_port = '25'
        self.smtp_host = 'smtp.sendgrid.net'
        self.start()

    def start(self):
        """
        Initialize SMTP Server
        """
        smtp_data = "{}: {}".format(self.smtp_host, self.smtp_port)
        self.service = smtplib.SMTP(smtp_data)
        self.service.starttls()

        # Using Credentials
        self.service.login(self.api_user, self.api_key)

    def close(self):
        """
        Quit SMTP Server
        """
        self.service.quit()

    def sender(self, message):
        """Send message with smtplib

        Arguments:
            message {dict} -- Message to send

        Raises:
            Exception -- Message could not been send.

        Returns:
            dict -- smtplib response
        """
        if not message:
            raise SGSError('Message could not been send.')

        return self.service.sendmail(
            message['From'],
            message['To'],
            message.as_string()
        )
