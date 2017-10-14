import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

SERVER = 'smtp.***.***'
PORT = 25
SENDER = "****@**.***"
PASSWORD = "****"
GETTER = "****@**.***"
SUBJECT = "测试一下"

def addMIME(bookName, subject, sender, toEmail):
    filePath = str(os.getcwd())+"/kindleBooks/"+bookName
    msg = MIMEMultipart()
    mobipart = MIMEApplication(open(filePath,'rb').read())  # 查找文件
    mobipart.add_header('Content-Disposition','attachment',filename = bookName) # 给文件加入头
    msg.attach(mobipart)

    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = toEmail
    return msg.as_string()

def send(bookName, subject, server,port,sender,password,toEmail):
    msg = addMIME(bookName, subject, sender, toEmail)
    try:
        send_mail = smtplib.SMTP(server,port)
        send_mail.ehlo()
        send_mail.starttls()
        send_mail.ehlo()
        send_mail.login(sender,password)
        send_mail.sendmail(sender,toEmail,msg)
        send_mail.quit()
        print("电子书发送成功！")
    except:
        print("发送过程有些问题！")
def getBook():
    booklist = os.listdir("./kindleBooks")
    return booklist
if __name__ == "__main__":
    #发送邮件
    booklist = getBook()
    noEnd = True
    while(noEnd):
        print("你是要发送一下的书吗？Y/N")
        for i in range(len(booklist)):
            print(str(i+1)+"、"+booklist[i])
        ANSER = input(">>> ")
        if ANSER in ['y','Y']:
            noEnd = False
            for i in range(len(booklist)):
                send(booklist[i], SUBJECT, SERVER, PORT, SENDER, PASSWORD, GETTER)
        elif ANSER in ['n','N']:
            exit()
        else:
            pass
