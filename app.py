# coding=utf-8

import tornado.web
import torndb
import redis
import conf

class Application(tornado.web.Application):
    """重写类增加数据库的链接"""
    def __init__(self,*args,**kwargs):
        super(Application,self).__init__(*args,**kwargs)# 调用父类init方法
        self.db = torndb.Connection(**conf.db)          # 生成mysql对象
        self.redis = redis.StrictRedis(**conf.redis)    # 生成redis对象