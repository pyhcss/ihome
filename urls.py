# coding=utf-8

import os

from handlers.basehandler import StaticFileHandler
from handlers.userhandler import *
from handlers.code import *
from handlers.loginandregister import *
from handlers.househandler import *

urls = [
    (r"^/api/imagecode",ImageCodeHandler),
    (r"^/api/telcode",TelCodeHandler),
    (r"^/api/register",RegisterHandler),
    (r"^/api/login",LoginHandler),
    (r"^/api/indexlogin",IndexLoginHandler),
    (r"^/api/myinfo",MyInfoHandler),
    (r"^/api/avatar",AvatarHandler),
    (r"^/api/rename",ReNameHandler),
    (r"^/api/auth",AuthHandler),
    (r"^/api/logout",LoginOutHandler),
    (r"^/api/area",AreaHandler),
    (r"^/api/myhouseinfo",MyHouseInfoHandler),
    (r"^/api/newhouse",NewHouseHandler),
    (r"^/api/houseimage",HouseImageHandler),
    (r"^/(.*)",StaticFileHandler,{"path":os.path.join(os.path.dirname(__file__),"static/html"),
                                  "default_filename":"index.html"})
]