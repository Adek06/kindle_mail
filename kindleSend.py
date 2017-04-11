# -*- coding:UTF:8 -*-
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

def send():

    # 账户设置
    server = 'smtp.sohu.com'
    port = 25
    sender = "****@sohu.com"
    password = "*****"
    to = "****@163.com"
    subject ="测试一下"
    
    # 加附件
    msg = MIMEMultipart()
    mobipart = MIMEApplication(open('/home/****/kindle_mail/test.mobi','rb').read())  # 查找文件
    mobipart.add_header('Content-Disposition','attachment',filename ='test.mobi') # 给文件加入头
    msg.attach(mobipart)

    # 邮件本体
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = to

    # 发送邮件
    try:
        send_mail = smtplib.SMTP(server,port)
        send_mail.ehlo()
        send_mail.starttls()
        send_mail.ehlo()
        send_mail.login(sender,password)
        send_mail.sendmail(sender,to,msg.as_string())
        send_mail.quit()
        print "电子书发送成功！"
    except:
        print "有些问题！"

send()
