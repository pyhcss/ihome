# coding=utf-8

from basehandler import BaseHandler
from utils.decorate import login_decorate
from constants import IMAGE_URL_START
from utils import aliyunoss


class MyInfoHandler(BaseHandler):
    """用户信息接口"""
    @login_decorate
    def get(self):
        if not self.session.data.get("avatar"):     # 如果session没有头像 返回其他信息
            return self.write({"errcode":"0","errmsg":"登录成功","data":{"mobile":self.session.data["tel"],"name":self.session.data["name"],"email":self.session.data["email"]}})
        else:                                       # 如果session有头像 带头像链接返回
            return self.write({"errcode":"0","errmsg":"登录成功","data":{"mobile":self.session.data["tel"],"name":self.session.data["name"],"email":self.session.data["email"],"avatar":self.session.data["avatar"]}})


class AvatarHandler(BaseHandler):
    """用户上传头像接口"""
    @login_decorate
    def post(self):
        try:                                        # 接受文件数据及源文件名
            filename = self.request.files["avatar"][0]["filename"]
            data = self.request.files["avatar"][0]["body"]
        except Exception as e:
            print e                                 # 返回错误信息
            return self.write({"errcode":"4103","errmsg":"上传失败、请重新操作"})
        try:                                        # 调用接口上传图片 返回图片名
            new_file_name = aliyunoss.imagefile(filename,data)
            if not new_file_name:                   # 如果图片名为空 返回错误信息
                return self.write({"errcode":"4103","errmsg":"上传失败、请重新操作"})
        except Exception as e:
            print e                                 # 上传失败返回错误信息
            return self.write({"errcode":"4301","errmsg":"上传失败"})
        try:
            id = self.session.data["id"]            # 调用数据库及session存储图片名和链接地址
            self.db.execute("update user_info set ui_image=%s where ui_id=%s",new_file_name,id)
            self.session.data["avatar"] = IMAGE_URL_START + new_file_name
            self.session.save()
        except Exception as e:
            print e                                 # 返回错误信息
            return self.write({"errcode":"4001","errmsg":"数据库错误"})
        else:                                       # 返回成功信息和图片链接
            return self.write({"errcode":"0","errmsg":"上传成功","data":self.session.data["avatar"]})


class ReNameHandler(BaseHandler):
    """修改用户名"""
    @login_decorate
    def post(self):
        try:                                        # 获取用户名
            name = self.json_args["name"]
        except Exception as e:
            print e                                 # 提示用户名已存在
            return self.write({"errcode":"4003","errmsg":"用户名已存在、请重新设置"})
        if not name or len(name) < 4:               # 提示用户名不合法
            return self.write({"errcode":"4003","":"用户名不能为空且必须大于等于4个字符"})
        try:
            id = self.session.data["id"]            # 修改数据库及session中用户名
            self.db.execute("update user_info set ui_title=%s where ui_id=%s",name,id)
            self.session.data["name"] = name
            self.session.save()
        except Exception as e:
            print e                                 # 返回错误信息
            return self.write({"errcode":"4001","errmsg":"数据库错误"})
        else:                                       # 返回修改成功
            return self.write({"errcode":"0","errmsg":"修改成功"})


class AuthHandler(BaseHandler):
    """查看实名认证信息接口"""
    @login_decorate
    def get(self):
        """实名认证查询接口"""
        try:
            id = self.session.data["id"]            # 根据session中的id 查询数据库实名认证信息
            user = self.db.get("select ui_name,ui_card from user_info where ui_id=%s",id)
        except Exception as e:
            print e                                 # 返回错误信息
            return self.write({"errcode":"4001","errmsg":"数据库查询错误"})
        if not all((user["ui_name"],user["ui_card"])):
            self.session.data["id_card"] = False    # 如果没有数据 返回并设置session为false
            self.session.save()
            return self.write({"errcode":"4002","errmsg":"无数据"})
        else:
            self.session.data["id_card"] = True     # 如果有数据 返回并设置session为true
            self.session.save()
            return self.write({"errcode":"0","errmsg":"查询成功","data":{"real_name":user["ui_name"],"id_card":user["ui_card"]}})

    @login_decorate
    def post(self):
        """实名认证接口"""
        try:                                        # 获取用户是否已经认证成功
            id_card = self.session.data["id_card"]
            id = self.session.data["id"]
        except Exception as e:
            print e                                 # 获取不到为非法请求
            return self.write({"errcode":"4201","errmsg":"非法请求"})
        if id_card:                                 # 如果为true则已存在认证信息
            return self.write({"errcode":"4003","errmsg":"实名认证信息已存在"})
        else:
            try:
                name = self.json_args["real_name"]  # 获取前端数据 真实姓名和身份证号
                card = self.json_args["id_card"]
            except Exception as e:
                print e                             # 返回错误信息
                return self.write({"errcode":"4103","errmsg":"参数错误"})
            if not all((name,card)):                # 返回错误信息
                return self.write({"errcode":"4103","errmsg":"姓名或身份证号不能为空"})
            elif len(name) < 2 or len(name) > 4 or len(card) != 18:
                return self.write({"errcode":"4103","errmsg":"姓名或身份证号不符"})
            else:
                try:                                # 更新数据库数据及session数据
                    self.db.execute("update user_info set ui_name=%s,ui_card=%s where ui_id=%s",name,card,id)
                    self.session.data["id_card"] = True
                    self.session.save()
                except Exception as e:
                    print e                         # 返回错误信息
                    return self.write({"errcode":"4001","errmsg":"数据库错误"})
                else:                               # 返回成功信息
                    return self.write({"errcode":"0","errmsg":"实名认证成功"})