import base64
import tempfile
import compressed_rtf
from email_master.util import EmailAttachmentList, EmailAttachment, EmailParser
from extract_msg import Message
from extract_msg.utils import xstr
import hashlib


class MSGParser(EmailParser):
    """
    See https://msdn.microsoft.com/en-us/library/cc433490(v=exchg.80).aspx for full property list
    """

    def __init__(self, email_data, filename="unknown.msg", ignore_errors=False, exclude_attachment_extensions=None):
        """
        Parse an MSG File
        :param fn: filename of msg file
        :param email_data: base64 data of the MSG file
        """
        super(MSGParser, self).__init__(email_data,
                                        filename=filename,
                                        ignore_errors=ignore_errors,
                                        exclude_attachment_extensions=exclude_attachment_extensions)
        temp_file = tempfile.SpooledTemporaryFile()  # Create a temp file for the ole library
        temp_file.write(base64.b64decode(email_data))
        self.msg = Message(temp_file)

    def get_cc(self):
        return self.msg.cc or u""

    def get_bcc(self):
        return self.msg._getStringStream('__substg1.0_0E02') or u""

    def get_raw_content(self):
        return self.email_data

    def get_raw_headers(self):
        return u"\n".join([u"{}: {}".format(h[0], h[1]) for h in self.get_headers() or []])

    def get_reply_to(self):
        return self.msg._getStringStream('__substg1.0_1042') or u""

    def get_id(self):
        return self.msg._getStringStream('__substg1.0_1035') or u""

    def get_sender(self):
        return self.msg.sender or u""

    def get_plaintext_body(self):
        return self.msg.body or u""

    def get_html_body(self, decode_html=True):
        return self.msg._getStringStream('__substg1.0_1013') or u""

    def get_rtf_body(self):
        data = self.msg._getStream("__substg1.0_10090102")
        if data:
            return compressed_rtf.decompress(data) or u""
        else:
            return u""

    def get_date(self):
        return self.msg.date or u""

    def get_subject(self):
        return self.msg.subject or u"(No Subject)"

    def get_type(self):
        return u"MSG"

    def get_recipients(self):
        return u",".join([self.msg.cc or u"", self.msg.to or u""])

    def get_headers(self):
        headers = self.msg.header._headers
        return headers if headers else []

    def get_attachments(self):
        raw_attachments = self.msg.attachments
        attachments = EmailAttachmentList()

        for raw_attachment in raw_attachments:
            if raw_attachment.data:
                data = raw_attachment.data
            else:
                data = self.msg._getStream(raw_attachment.dir + '__substg1.0_37010102')

            if not data:
                # No data in the attachment ignore
                continue
            elif isinstance(data, Message):
                # Following code taken from extract_msg.save()
                eml_data = 'From: ' + xstr(self.msg.sender) + "\n"
                eml_data += 'To: ' + xstr(self.msg.to) + "\n"
                eml_data += 'CC: ' + xstr(self.msg.cc) + "\n"
                eml_data += 'Subject: ' + xstr(self.msg.subject) + "\n"
                eml_data += 'Date: ' + xstr(self.msg.date) + "\n"
                eml_data += '-----------------' + "\n" + "\n"
                eml_data += self.msg.body

                data = eml_data

            fallback_name = "unknown-{}".format(hashlib.md5(data).hexdigest())

            filename = raw_attachment.longFilename or fallback_name
            header_info = raw_attachment.shortFilename or fallback_name

            attachments.add_attachment(EmailAttachment(header_info, filename, data))

        return attachments
