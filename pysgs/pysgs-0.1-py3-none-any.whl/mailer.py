"""
Process the email configuration
"""
import os
import mimetypes
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from pysgs.server import Server
from pysgs.exceptions import SGSError


class Mailer(Server):
    """
    Mailer class to process messages
    """

    def __init__(self, api_key=""):
        """
        Keyword Arguments:
            api_key {str} -- SendGrid Api Key (default: {''})
        """
        Server.__init__(self, api_key=api_key)
        self.message = MIMEMultipart()

    def send(self):
        """Call sender method

        Returns:
            dict -- smtplib response
        """

        return super.sender(self.message)

    def setup(self, sender='', recipients=None, subject=''):
        """Setting mail configuration

        Keyword Arguments:
            sender {str} -- Email who sends the message (default: {''})
            recipients {str} or {list} -- Recipient Emails (default: {None})
            subject {str} -- Subject of the message (default: {''})

        Raises:
            Exception -- Recipients information has not a valid type
        """
        self.message['From'] = sender
        self.message['Subject'] = subject

        if isinstance(recipients, list):
            self.message['To'] = ", ".join(recipients)
        elif isinstance(recipients, str):
            self.message['To'] = recipients
        else:
            raise SGSError('Recipients information has not a valid type.')

    def add_attachment(self, path_attach=''):
        """Add an attachment to the message

        Keyword Arguments:
            path_attach {str} -- File path (default: {''})

        Raises:
            Exception -- Path is not a valid file type
        """
        if not os.path.isfile(path_attach):
            raise SGSError('Path is not a valid file type.')

        def guess_mime(path_attach):
            """
            Guess file mimetype
            """
            ctype, encoding = mimetypes.guess_type(path_attach)
            if ctype is None or encoding is not None:
                ctype = 'application/octet-stream'

            main_type, sub_type = ctype.split('/', 1)
            return main_type, sub_type

        def open_attach(path_attach):
            """
            Open and read file
            """
            with open(path_attach, 'rb') as file_name:
                return file_name.read()
            return ""

        # Guess Mime
        main_type, sub_type = guess_mime(path_attach)
        if main_type == 'text':
            content = ""
            with open(path_attach) as file_name:
                content = file_name.read()

            attach = MIMEText(content, _subtype=sub_type)
        else:
            # Object
            content = open_attach(path_attach)
            if main_type == 'image':
                attach = MIMEImage(content, _subtype=sub_type)
            elif main_type == 'audio':
                attach = MIMEAudio(content, _subtype=sub_type)
            else:
                attach = MIMEBase(main_type, sub_type)
                attach.set_payload(content)

        # Set the filename parameter
        attach.add_header(
            'Content-Disposition',
            'attachment',
            filename=path_attach
        )

        self.message.attach(attach)

    def add_content(self, text="", content_type="html"):
        """[summary]

        Keyword Arguments:
            text {str} -- Plain text or HTML content (default: {""})
            content_type {str} -- "html" or "text" (default: {"html"})
        """
        self.message.attach(MIMEText(text, content_type))
