#!/usr/bin/env python

from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib


def _format_addr(name, addr):
    if not isinstance(name, bytes):
        name = name.encode('utf-8', 'ignore')
    return formataddr(
        (
            Header(name, 'utf-8').encode(),
            addr
        )
    )

class Sendmail:
    def __call__(self,to_addr, *args,**kwds):
        if isinstance(to_addr,(list,tuple)):
            for i in to_addr:
                self.send(i,*args,**kwds)
        else:
            self.send(to_addr, *args, **kwds)


    def send(self, to_addr, title, txt, to_name=None, from_addr=None, name=None):
        if name is None:
            name = self.name
        if from_addr is None:
            from_addr = self.mail

        if to_name is None:
            to_name = to_addr.split("@", 1)[0]

        msg = MIMEText(txt, 'plain', 'utf-8')
        msg['From'] = _format_addr(name, from_addr)
        msg['To'] = _format_addr(to_name, to_addr)
        msg['Subject'] = Header(title, 'utf-8').encode()
        msg.add_header('Reply-to', self.reply_to)
        msg = msg.as_string()

        port = self.smtp_port
        if port == 465:
            smtp = smtplib.SMTP_SSL(self.smtp_host, port)
        else:
            smtp = smtplib.SMTP(self.smtp_host, port)

        #smtp.set_debuglevel(1)

        smtp.ehlo()
        if port != 25 and port!=465:
            smtp.starttls()
            smtp.ehlo()
        smtp.login(self.smtp_user, self.smtp_password)
        addr_li = [to_addr]
        if self.backup:
            addr_li.append(self.backup)
        smtp.sendmail(from_addr, addr_li, msg)
        smtp.quit()

    def __init__(self, name, mail, reply_to, backup, smtp_host, smtp_port, smtp_user, smtp_password):
        self.name = name
        self.mail = mail
        self.reply_to = reply_to
        self.backup = backup
        self.smtp_host=smtp_host
        self.smtp_port=smtp_port
        self.smtp_user=smtp_user
        self.smtp_password=smtp_password

if __name__ == "__main__":
    from datetime import datetime
    mail_li = [
        "xpure@foxmail.com",
    ]
    from config import CONFIG
    sendmail = Sendmail(**CONFIG)
    for mail in mail_li:
        title = f"测试 {mail} {datetime.now()}"
        txt = f"""{title}
{__file__}
"""
        #sendmail([mail], title, txt)
        sendmail(mail, title, txt)
