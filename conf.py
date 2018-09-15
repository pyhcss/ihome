# coding=utf-8

import os

# application 配置
settings = {
    "static_path":os.path.join(os.path.dirname(__file__),"static"),
    "template_path":os.path.join(os.path.dirname(__file__),"template"),
    "cookie_secret":"kfVLP/qhTK6mhxb6LYWngJQ6ZYERFUk4kFQssHGnJjw=",
    "xsrf_cookies":True,
    "debug":True,
}

# mysql数据库配置
db = {
    "host": "127.0.0.1",
    "database": "ihome",
    "user": "root",
    "password": "yunlong",
    "time_zone":"+8:00",
}

# redis数据库配置
redis = {
    "host": "127.0.0.1",
    "port": 6379,
}