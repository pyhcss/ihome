# coding=utf-8

import json
import tornado.web
from utils.session import Session


class BaseHandler(tornado.web.RequestHandler):
    """自定义基类"""
    @property
    def db(self):
        return self.application.db

    @property
    def redis(self):
        return self.application.redis

    def prepare(self):
        pass

    def write_error(self,status_code,**kwargs):
        pass

    def set_default_headers(self):
        self.set_header("Content-Type","application/json;charset=utf-8")

    def initialize(self):
        """进入请求方法前执行"""
        self.xsrf_token
        if self.request.headers.get("Content-Type","").startswith("application/json"):
            self.json_args = json.loads(self.request.body)
        else:
            self.json_args = None

    def get_current_user(self):
        """判断用户是否登录"""
        self.session = Session(self)
        return self.session.data

    def on_finish(self):
        pass


class StaticFileHandler(tornado.web.StaticFileHandler):
    """重写静态文件类"""
    def __init__(self,*args,**kwargs):
        super(StaticFileHandler,self).__init__(*args,**kwargs)
        self.xsrf_token