# -*- coding: utf-8 -*-

# @Date    : 2018-10-19
# @Author  : Peng Shiyu

from __future__ import unicode_literals, print_function
import logging
import smtplib
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr


class SendEmail(object):
    """
    发送邮件用的比较多，单独整理出来方便使用
    """

    def __init__(self, smtp_server, from_address, password, smtp_port=25, from_name=None):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.from_address = from_address
        self.password = password
        self.from_name = from_name if from_name else from_address

        self.server = None
        self.receives = []
        self._login()

    def __del__(self):
        self.server.quit()

    def _login(self):
        """
        登录服务器
        """
        if self.smtp_port == 25:
            self.server = smtplib.SMTP(self.smtp_server, self.smtp_port)

        elif self.smtp_port == 465:
            self.server = smtplib.SMTP_SSL(self.smtp_server, self.smtp_port)

        else:
            raise Exception("port: {} not support".format(self.smtp_port))

        # self.server.set_debuglevel(0)
        self.server.login(self.from_address, self.password)

    def _format_address(self, email_address):
        name, address = parseaddr(email_address)
        return formataddr((Header(name, 'utf-8').encode(), address))

    def add_receive(self, to_address, to_name=None):
        """
        添加收件人
        :param to_address: str 收件人地址
        :param to_name: str 收件人名称(可选)
        """
        to_name = to_name if to_name else to_address
        self.receives.append((to_address, to_name))

    def send_all(self, title, body=None, body_type="plain"):
        """
        发送邮件给所有人
        :param title: str 邮件标题
        :param body: str 邮件内容
        :param body_type: 邮件内容类型 plain：文本，html：网页
        """
        body = body if body else title

        for to_address, to_name in self.receives:
            self.send(to_address, to_name, title, body, body_type)

    def send(self, to_address, title, body=None, to_name=None, body_type="plain"):
        """
        发送邮件
        :param to_address: str 收件人地址
        :param title: str 邮件标题
        :param body: str 邮件内容
        :param to_name: str 收件人名称（可选）
        :param body_type: srt 邮件内容类型 plain：文本，html：网页
        """
        to_name = to_name if to_name else to_address
        body = body if body else title

        msg = MIMEText(body, body_type, 'utf-8')
        msg['From'] = self._format_address('%s <%s>' % (self.from_name, self.from_address))
        msg['To'] = self._format_address('%s <%s>' % (to_name, to_address))
        msg['Subject'] = Header(title, 'utf-8').encode()

        logging.info("send {}".format(to_address))

        self.server.sendmail(self.from_address, [to_address], msg.as_string())


if __name__ == '__main__':

    # 用于临时发邮件用
    send_email = SendEmail(
        smtp_server="smtp.163.com",
        smtp_port=25,
        from_address="xxx@163.com",
        password="password",
        from_name="mouday"
    )

    send_email.send(
        to_address="xxx@gmail.com",
        title="你好世界",
        body="你好世界"
    )
