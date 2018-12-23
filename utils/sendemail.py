# coding=utf-8

import smtplib
from email.mime.text import MIMEText
# from email.header import Header


def sendemail(address,code,times="5"):
    smtp_address = "smtp.163.com"
    from_mail = "newzn_ihome@163.com"
    from_pwd = "******"
    to_mail = address

    message = MIMEText("您好,欢迎注册ihom网站,您的验证码是"+ code +",请于"+ times +"分钟之内注册,谢谢使用","plain","utf-8")
    message["From"] = from_mail
    message["To"] = to_mail
    message["Subject"] = "ihome"
    try:
        smtp_server = smtplib.SMTP(smtp_address,port=25)
        smtp_server.login(from_mail,from_pwd)
        smtp_server.sendmail(from_mail,to_mail,message.as_string())
        return "发送成功"
    except Exception as e:
        print e
        return "发送失败"

if __name__ == "__main__":
    res = sendemail("","995905","5")
    print res
