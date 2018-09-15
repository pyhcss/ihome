#coding=gbk

#coding=utf-8

#-*- coding: UTF-8 -*-  

from CCPRestSDK import REST
import ConfigParser

#���ʺ�
accountSid= '8a216da865187d9a0165189ddf910058';

#���ʺ�Token
accountToken= '3cb1d8233f8446c48e2e765179dd4a0f';

#Ӧ��Id
appId='8a216da865187d9a0165189ddfea005e';

#�����ַ����ʽ���£�����Ҫдhttp://
serverIP='app.cloopen.com';

#����˿� 
serverPort='8883';

#REST�汾��
softVersion='2013-12-26';

  # ����ģ�����
  # @param to �ֻ�����
  # @param datas �������� ��ʽΪ���� ���磺{'12','34'}���粻���滻���� ''
  # @param $tempId ģ��Id

class CCP(object):
    """������֤��ӿ� ����ģʽ"""
    _instance = None
    _first_init = True

    def __new__(cls):
        if cls._instance == None:
            cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self):
        if self._first_init == True:
            # ��ʼ��REST SDK
            self.rest = REST(serverIP, serverPort, softVersion)
            self.rest.setAccount(accountSid, accountToken)
            self.rest.setAppId(appId)
            self._first_init = True

    def sendTemplateSMS(self,to,datas,tempId):
        # sendTemplateSMS(�ֻ�����,��������,ģ��Id)
        return self.rest.sendTemplateSMS(to, datas, tempId)

if __name__ == "__main__":
    data = CCP().sendTemplateSMS("13146461202", ["567890", 2], 1)
    print data["statusCode"]    # ״̬�� 000000��ʾ��ȷ����
    print data["templateSMS"]   # ��Ϣid�ʹ���ʱ��� �ֵ�
