# coding=utf-8

import re
import random
from constants import *
from basehandler import BaseHandler
from libs.yuntongxun.ccp import CCP
from utils.captcha.captcha import captcha


class ImageCodeHandler(BaseHandler):
    """图片验证码接口"""
    def get(self):
        pre = self.get_argument("pre","")       # 获取上一次验证码id
        cur = self.get_argument("cur","")       # 获取新验证码id
        if pre != "":                           # 上一次验证码不为空时从数据库删除验证码
            try:
                self.redis.delete("image_code_%s" %pre)
            except Exception as e:
                print e
        if cur == "":                           # 新验证码id为空时 返回空数据
            self.write({"errcode":"4103","errmsg":"参数错误"})
        else:                                   # 生成验证码图片及文本信息
            id,text,image = captcha.generate_captcha()
            try:                                # 写入redis数据库
                self.redis.setex("image_code_%s" %cur,REDIS_CAPTCHA_MAX_TIME,text)
            except Exception as e:
                return self.write({"errcode":"4004","errmsg":"数据库出错"})
            else:
                self.write(image)               # 返回验证码数据


class TelCodeHandler(BaseHandler):
    """短信验证码接口"""
    def post(self):
        try:                                        # 获取手机号 验证码 验证码id
            mobile = self.json_args["mobile"]
            imagecode = self.json_args["imagecode"]
            imagecode_id = self.json_args["imagecode_id"]
        except Exception as e:                      # 出现异常返回参数错误
            return self.write({"errcode":"4103","errmsg":"参数错误"})
        else:                                       # 任意一项为空时返回参数不完整
            if not all((mobile,imagecode,imagecode_id)):
                return self.write({"errcode":"4103","errmsg":"参数不完整"})
            elif not re.match(r"^1\d{10}$",mobile): # 判断手机号是否正确
                return self.write({"errcode":"4004","errmsg":"手机号错误"})
            else:
                try:                                # 从数据库获取图片验证码文本
                    redis_imagecode = self.redis.get("image_code_%s" %imagecode_id)
                except Exception as e:
                    return self.write({"errcode":"4001","errmsg":"数据库查询错误"})
                else:                               # 比较图片验证码是否正确
                    if redis_imagecode == None:
                        return self.write({"errcode":"4002","errmsg":"验证码已过期"})
                    elif redis_imagecode.lower() != imagecode.lower():
                        return self.write({"errcode":"4004","errmsg":"验证码错误"})
                    else:                           # 生成随机6位数手机验证码
                        code = str(random.randint(0,999999)).zfill(6)
                        try:                        # 手机验证码存入数据库
                            self.redis.setex("tel_code_%s" %mobile,REDIS_TEL_MAX_TIME,code)
                        except Exception as e:
                            return self.write({"errcode":"4004","errmsg":"数据库错误"})
                        else:
                            try:                    # 调用接口发送验证码短信
                                status = CCP().sendTemplateSMS(mobile, [code, 5], 1)
                                                    # 判断是否发送成功
                                if status["statusCode"] != "000000":
                                    return self.write({"errcode":"4301","errmsg":"验证码发送失败"})
                            except Exception as e:
                                return self.write({"errcode":"4301","errmsg":"验证码发送失败"})
                            else:
                                return self.write({"errcode":"0","errmsg":"验证码发送成功"})


