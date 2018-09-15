# coding=utf-8

import tornado.web
import tornado.ioloop
import tornado.httpserver

from urls import urls
from conf import settings
from app import Application
from tornado.options import options,define

# 定义端口 启动时可以命令行键入port=int值
define("port",default=8000,type=int,help="please input port")


def main():
    options.parse_command_line()                        # 读取命令行参数 且自动开启log
    app = Application(urls,**settings)                  # 生成application对象
    http_server = tornado.httpserver.HTTPServer(app)    # 生成http_server对象
    http_server.listen(options.port)                    # 定义监听端口
    tornado.ioloop.IOLoop.current().start()             # 启动服务器 开启监听


if __name__ == "__main__":
    main()