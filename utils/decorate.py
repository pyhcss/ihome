# coding=utf-8

def login_decorate(fun):
    """登录验证装饰器"""
    def warpper(self,*args,**kwargs):
        if self.get_current_user():         # 如果返回值data有数据 代表已经登录 执行原函数
            fun(self,*args,**kwargs)
        else:                               # 如果没有数据 代表未登录 直接返回错误信息
            return self.write({"errcode":"4101","errmsg":"用户未登录"})
    return warpper