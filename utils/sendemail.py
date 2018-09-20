# coding=utf-8

import smtplib
from email.mime.text import MIMEText
from email.header import Header


def sendemail(address,code,times="5"):
    from_mail = "admin@sjsclub.com"
    to_mail = address

    message = MIMEText("您好,欢迎注册ihom网站,您的验证码是"+ code +",请于"+ times +"分钟之内注册,本邮箱非真实邮箱,请勿回复,谢谢使用","plain","utf-8")
    message["From"] = Header("","utf-8")
    message["To"] = Header("","utf-8")
    message["Subject"] = Header("ihome","utf-8")
    try:
        smtp_server = smtplib.SMTP("localhost")
        smtp_server.sendmail(from_mail,to_mail,message.as_string())
        return "发送成功"
    except Exception as e:
        print e
        return "发送失败"

if __name__ == "__main__":
    res = sendemail("2352840536@qq.com","995905","5")
    print res
