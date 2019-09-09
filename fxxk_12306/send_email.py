#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
# @Time    : 2019/9/10 上午12:09
# @Author  : Chilson
# @Email   : qiushun_fang@126.com

import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr
from config import Config
from fxxk_12306.logger import Logger

logger = Logger('Email').get_logger()

def send_successful_email(sender = Config.MAIL_SENDER, receivers=Config.MAIL_RECEIVERS):
    mail_host = 'smtp.126.com'  # 设置服务器
    mail_username = Config.MAIL_USERNAME  # 用户名
    mail_password = Config.MAIL_PASSWORD  # 口令
    mail_msg = """
        <p>Fxxk-12306 抢票成功,请尽快去支付哦!...</p>
        <p><a href="https://www.12306.cn">这是链接</a></p>
    """
    message = MIMEText(mail_msg, 'html', 'utf-8')
    message['From'] = formataddr(['抢票程序', sender])
    message['To'] = formataddr(['幸运儿', ','.join(receivers)])
    subject = 'Fxxk-12306 抢票成功'
    message['Subject'] = Header(subject, 'utf-8')

    try:
        smtp_obj = smtplib.SMTP()
        smtp_obj.connect(mail_host, 25)  # 25 为 SMTP 端口号
        smtp_obj.login(mail_username, mail_password)
        smtp_obj.sendmail(sender, receivers, message.as_string())
        logger.info('邮箱发送成功!')
    except smtplib.SMTPException as e:
        logger.error('无法发送邮件', e)


if __name__ == '__main__':
    send_successful_email()