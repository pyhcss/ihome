# coding=utf-8

import hashlib
from utils.session import Session
from basehandler import BaseHandler
from constants import IMAGE_URL_START
from utils.decorate import login_decorate

class RegisterHandler(BaseHandler):
    """注册接口"""
    def post(self):
        try:                                        # 从客户端接收数据
            mobile = self.json_args["mobile"]
            telcode = self.json_args["phonecode"]
            passwd = self.json_args["password"]
        except Exception as e:
            print e                                 # 出现异常为参数不完整
            return self.write({"errcode":"4103","errmsg":"参数错误"})
        else:                                       # 如果某个参数为空 返回错误信息
            if not all((mobile,telcode,passwd)):
                return self.write({"errcode":"4103","errmsg":"参数不能为空"})
            else:
                try:                                # 获取数据库中短信验证码
                    redis_telcode = self.redis.get("tel_code_%s" %mobile)
                except Exception as e:
                    print e                         # 获取不到则手机验证码已过期
                    return self.write({"errcode":"4001","errmsg":"手机验证码已过期"})
                else:
                    if not redis_telcode:           # 如果为空则手机验证码已过期
                        return self.write({"errcode":"4001","errmsg":"手机验证码已过期"})
                    elif redis_telcode != telcode:  # 如果不一样 返回错误信息
                        return self.write({"errcode":"4004","errmsg":"手机验证码错误"})
                    else:                           # 查询数据库中手机号是否注册过
                        try:                        # 生成密码sha1字符串并添加到数据库中
                            pwd = hashlib.sha1(passwd).hexdigest()
                            user_id = self.db.execute("insert into user_info(ui_title,ui_tel,ui_pwd) values(%s,%s,%s)",mobile,mobile,pwd)
                        except Exception as e:
                            print e                 # 出现异常返回错误信息
                            return self.write({"errcode":"4003","errmsg":"手机号已被注册"})
                        else:
                            try:                    # 调用session接口设置session_id
                                self.session = Session(self)
                                self.session.data["id"] = user_id
                                self.session.data["name"] = mobile
                                self.session.data["tel"] = mobile
                                self.session.save()
                            except Exception as e:
                                print e             # 出现异常返回错误信息
                                return self.write({"errcode":"4102","errmsg":"登录失败"})
                            else:                   # 未出现异常返回0
                                return self.write({"errcode":"0","errmsg":"注册成功"})


class NewRegisterHandler(BaseHandler):
    """新注册接口"""
    def post(self):
        try:                                        # 从客户端接收数据
            mobile = self.json_args["mobile"]
            email = self.json_args["email"]
            emailcode = self.json_args["phonecode"]
            passwd = self.json_args["password"]
        except Exception as e:
            print e                                 # 出现异常为参数不完整
            return self.write({"errcode":"4103","errmsg":"参数错误"})
        if not all((mobile,email,emailcode,passwd)):# 如果某个参数为空 返回错误信息
            return self.write({"errcode":"4103","errmsg":"参数不能为空"})
        try:                                        # 获取数据库中邮箱验证码
            redis_emailcode = self.redis.get("email_code_%s_%s" %(email,mobile))
        except Exception as e:
            print e                                 # 获取不到则邮箱验证码已过期
            return self.write({"errcode":"4001","errmsg":"邮箱验证码已过期"})
        if not redis_emailcode:                     # 如果为空则邮箱验证码已过期
            return self.write({"errcode":"4001","errmsg":"邮箱验证码已过期"})
        elif redis_emailcode != emailcode:          # 如果不一样 返回错误信息
            return self.write({"errcode":"4004","errmsg":"邮箱验证码错误"})
        try:                                        # 生成密码sha1字符串并添加到数据库中
            pwd = hashlib.sha1(passwd).hexdigest()
            user_id = self.db.execute("insert into user_info(ui_title,ui_tel,ui_pwd,ui_email) values(%s,%s,%s,%s)",mobile,mobile,pwd,email)
        except Exception as e:
            print e                                 # 出现异常返回错误信息
            return self.write({"errcode":"4003","errmsg":"手机号已被注册"})
        try:                                        # 调用session接口设置session_id
            self.session = Session(self)
            self.session.data["id"] = user_id
            self.session.data["name"] = mobile
            self.session.data["tel"] = mobile
            self.session.data["email"] = email
            self.session.save()
        except Exception as e:
            print e                                 # 出现异常返回错误信息
            return self.write({"errcode":"4102","errmsg":"登录失败"})
        return self.write({"errcode":"0","errmsg":"注册成功"})


class LoginHandler(BaseHandler):
    """登录接口"""
    def post(self):
        try:                                        # 从客户端获取参数
            mobile = self.json_args["mobile"]
            password = self.json_args["password"]
        except Exception as e:
            print e
            return self.write({"errcode":"4103","errmsg":"参数错误"})
        else:
            if not all((mobile,password)):
                return self.write({"errcode":"4103","errmsg":"参数不能为空"})
            else:
                try:                                # 获取数据库客户信息
                    user = self.db.get("select ui_id,ui_title,ui_tel,ui_pwd,ui_image,ui_email from user_info where ui_tel=%s",mobile)
                except Exception as e:
                    print e
                    return self.write({"errcode": "4001", "errmsg": "数据库查询错误"})
                else:
                    if not user:                    # 校验参数返回错误信息
                        return self.write({"errcode": "4104", "errmsg": "用户未注册"})
                    elif user["ui_pwd"] != hashlib.sha1(password).hexdigest():
                        return self.write({"errcode": "4106", "errmsg": "用户名或密码错误"})
                    else:
                        try:                        # 调用session接口设置session_id
                            self.session = Session(self)
                            self.session.data["id"] = user["ui_id"]
                            self.session.data["name"] = user["ui_title"]
                            self.session.data["tel"] = user["ui_tel"]
                            self.session.data["email"] = user["ui_email"]
                            self.session.data["avatar"] = IMAGE_URL_START + user["ui_image"] if user["ui_image"] else ""
                            self.session.save()
                        except Exception as e:
                            print e                 # 出现异常返回错误信息
                            return self.write({"errcode": "4102", "errmsg": "登录失败"})
                        else:                       # 未出现异常返回0
                            return self.write({"errcode": "0", "errmsg": "登录成功"})


class IndexLoginHandler(BaseHandler):
    """主页判断用户是否登录"""
    def get(self):
        session_data = self.get_current_user()
        if session_data:
            return self.write({"errcode":"0","errmsg":"True","name":session_data.get("name")})
        else:
            return self.write({"errcode":"4101","errmsg":"False"})


class LoginOutHandler(BaseHandler):
    """注销接口"""
    @login_decorate
    def get(self):
        try:                                    # 调用session接口删除session数据
            self.session.clear()
        except Exception as e:
            print e                             # 返回注销信息
            return self.write({"errcode":"4001","errmsg":"数据库查询错误"})
        self.write({"errcode":"0","errmsg":"注销成功"})