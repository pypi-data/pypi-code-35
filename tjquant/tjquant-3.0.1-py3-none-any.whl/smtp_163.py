#coding=utf8

import smtplib
from email.mime.text import MIMEText


#subject = '2月25日结果'
#content="今天天气怎么样？"
def send_email(add_list, subject, content):
    msg = MIMEText(content, 'plain', 'utf-8')
    msg['From'] ='Mr. 陈<ctx000001@163.com>'
    # 显示与收件人
    msg['To'] = '财神'
    # 就是标题,最醒目的
    msg['Subject'] = subject
    # 输入Email地址和口令:
    from_addr = "ctx000001@163.com"
    password = "Qazmlp00"
    # 输入SMTP服务器地址:
    smtp_server = "smtp.163.com"
    smtp_port=465
    # 输入收件人地址:
    #to_addr = ["670683134@qq.com","ctx000001@163.com"]
    server = smtplib.SMTP_SSL(smtp_server, smtp_port)
    server.set_debuglevel(1)
    server.login(from_addr, password)
    server.sendmail(from_addr, add_list, msg.as_string())
    server.quit()

if __name__=="__main__":
    send_email(['670683134@qq.com'],"你好","这是一个测试邮件")
