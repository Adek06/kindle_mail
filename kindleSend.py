import os
import smtplib
import pickle
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

PORT = 25
SUBJECT = "convert"

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

def pickleToDick(server, getter, sender, password):
    d = dict(Server = server,Getter = getter,Sender = sender, Password = password )
    with open('User.txt','wb') as f:
        pickle.dump(d,f)        

def login():
    if('User.txt' in os.listdir()):
        with open('./User.txt','rb') as f:
            d = pickle.load(f)
        if d != '':
            print('使用帐号'+d['Sender']+'登录')
            return d['Server'], d['Getter'], d['Sender'], d['Password']
    else:
        noLogin = True

    while noLogin:
        SERVER = input("请输入smtp服务器:")
        GETTER = input("请输入kindle邮箱地址：")
        SENDER = input("请输入发送人的邮箱地址：")
        PASSWORD = input("请输入邮箱密码（该密码只会保存在本地，却不会以任何形式漏出）：")
        send_mail = smtplib.SMTP(SERVER, 25)
        send_mail.ehlo()
        send_mail.starttls()
        send_mail.ehlo() 
        x = send_mail.login(SENDER, PASSWORD)
        if x[0] < 500:
            print("登录成功")
            pickleToDick(SERVER, GETTER, SENDER, PASSWORD)
            return SERVER, GETTER, SENDER, PASSWORD
        else:
            print("请重新确认信息")

        

def send(bookName, subject, server,port,sender,password,toEmail):
    try:
        msg = addMIME(bookName, subject, sender, toEmail)
        send_mail = smtplib.SMTP(server,port)
        send_mail.ehlo()
        send_mail.starttls()
        send_mail.ehlo()
        send_mail.login(sender,password)
        send_mail.sendmail(sender,toEmail,msg)
        send_mail.quit()
        print(bookName+"发送成功！")
    except smtplib.SMTPDataError:
        print("你的邮件被当成了垃圾邮件，请不要重复发送过多电子书")
def getBook():
    booklist = os.listdir("./kindleBooks")
    return booklist
if __name__ == "__main__":
    #发送邮件
    booklist = getBook()
    SERVER, GETTER, SENDER, PASSWORD = login()
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
