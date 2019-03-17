"""SMTP class file."""

import smtplib


class SMTP(object):
    """SMTP class."""

    def __init__(self, server, verbose=False):
        """Initialize an SMTP class instance."""
        self.server = server
        self.verbose = verbose

        # smtplib package
        self.smtplib = smtplib

        # attempt to connect to SMTP server
        try:
            self.smtp = smtplib.SMTP(self.server)
        except smtplib.SMTPException as e:
            print('ERROR connecting to SMTP server: %s' % (self.server))
            print(e)

    def send(self, to, frm, subject, body):
        """Send an email message."""
        # create the message string
        message = "From: %s\nTo: %s\nSubject: %s\n\n%s""" % (
            frm,
            to,
            subject,
            body
        )
        # attempt to send the message
        try:
            self.smtp.sendmail(frm, [to], message)
        except smtplib.SMTPException as e:
            print('ERROR sending email to: %s' % (to))
            print(e)
