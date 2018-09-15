#coding=gbk

#coding=utf-8

#-*- coding: UTF-8 -*-  

from CCPRestSDK import REST
import ConfigParser

#主帐号
accountSid= '8a216da865187d9a0165189ddf910058';

#主帐号Token
accountToken= '3cb1d8233f8446c48e2e765179dd4a0f';

#应用Id
appId='8a216da865187d9a0165189ddfea005e';

#请求地址，格式如下，不需要写http://
serverIP='app.cloopen.com';

#请求端口 
serverPort='8883';

#REST版本号
softVersion='2013-12-26';

  # 发送模板短信
  # @param to 手机号码
  # @param datas 内容数据 格式为数组 例如：{'12','34'}，如不需替换请填 ''
  # @param $tempId 模板Id

class CCP(object):
    """短信验证码接口 单例模式"""
    _instance = None
    _first_init = True

    def __new__(cls):
        if cls._instance == None:
            cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self):
        if self._first_init == True:
            # 初始化REST SDK
            self.rest = REST(serverIP, serverPort, softVersion)
            self.rest.setAccount(accountSid, accountToken)
            self.rest.setAppId(appId)
            self._first_init = True

    def sendTemplateSMS(self,to,datas,tempId):
        # sendTemplateSMS(手机号码,内容数据,模板Id)
        return self.rest.sendTemplateSMS(to, datas, tempId)

if __name__ == "__main__":
    data = CCP().sendTemplateSMS("13146461202", ["567890", 2], 1)
    print data["statusCode"]    # 状态码 000000表示正确发送
    print data["templateSMS"]   # 消息id和创建时间戳 字典
