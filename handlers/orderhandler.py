# coding=utf-8

from time import strftime
from basehandler import BaseHandler
from utils.decorate import login_decorate
from datetime import datetime
from constants import IMAGE_URL_START


class NewOrderHandler(BaseHandler):
    """创建订单接口"""
    @login_decorate
    def post(self):
        try:                                            # 从客户端获取信息
            house_id = self.json_args["house_id"]       # 房屋id
            start_date = self.json_args["start_date"]   # 开始时间
            end_date = self.json_args["end_date"]       # 结束时间
            user_id = self.session.data["id"]           # 从session获取下单客户id
        except Exception as e:
            print e
            return self.write({"errcode":"4103","errmsg":"参数错误"})
        if not all((house_id,start_date,end_date)):
            return self.write({"errcode":"4103","errmsg":"参数错误"})
        elif start_date >= end_date:
            return self.write({"errcode":"4103","errmsg":"起止日期不能相同"})
        try:                                            # 查询数据库确认订单不冲突
            house = self.db.get("select hi_id,hi_price,hi_order_count from house_info left join order_info on hi_id=oi_house where hi_id=%s and (oi_start_day >= %s or oi_end_day <= %s or oi_start_day is null)",house_id,start_date,end_date)
        except Exception as e:
            print e
            self.write({"errcode":"4001","errmsg":"数据库错误"})
        if not house:                                   # 返回查询结果
            self.write({"errcode":"4004","errmsg":"房间已被预定"})
        d1 = datetime.strptime(start_date,"%Y-%m-%d")   # 计算预定天数
        d2 = datetime.strptime(end_date,"%Y-%m-%d")
        day_count = (d2-d1).days
        amount = day_count * house["hi_price"]          # 计算订单金额
        try:                                            # 创建订单信息
            order_id = self.db.execute("insert into order_info(oi_user,oi_house,oi_start_day,"
                                       "oi_end_day,oi_count_day,oi_price,oi_amount) values(%s,%s,%s,%s,%s,%s,%s)",
                                       user_id,house["hi_id"],start_date,end_date,day_count,house["hi_price"],amount)
            self.db.execute("update house_info set hi_order_count=%s where hi_id=%s",int(house["hi_order_count"])+1,house_id)
        except Exception as e:
            print e
            return self.write({"errcode":"4001","errmsg":"数据库错误"})
        if order_id:                                    # 返回创建结果
            return self.write({"errcode":"0","errmsg":"创建成功"})
        else:
            return self.write({"errcode":"4001","errmsg":"数据库错误"})


class MyOrderHandler(BaseHandler):
    """查询自己的订单及客户订单"""
    @login_decorate
    def get(self):                                      # 获取客户身份
        auth = self.get_argument("role","")
        user_id = self.session.data["id"]
        if not auth:
            return self.write({"errcode":"4103","errmsg":"参数错误"})
        if auth == "custom":                            # 查询自己的订单
            sql = "select oi_id,oi_status,hi_image,hi_title,oi_ctime,oi_start_day,oi_end_day,oi_amount,oi_count_day,oi_comment from order_info left join house_info on oi_house=hi_id where oi_user=%s order by oi_ctime desc"
        elif auth == "landlord":                        # 查询客户订单
            sql = "select oi_id,oi_status,hi_image,hi_title,oi_ctime,oi_start_day,oi_end_day,oi_amount,oi_count_day,oi_comment from order_info left join house_info on oi_house=hi_id where hi_user=%s order by oi_ctime desc"
        try:                                            # 调用数据库查询数据
            orders = self.db.query(sql,user_id)
        except Exception as e:
            print e
            return self.write({"errcode":"4001","errmsg":"数据库错误"})
        data = [                                        # 组合数据
            {
                "order_id":i["oi_id"],
                "status":i["oi_status"],
                "img_url":IMAGE_URL_START + i["hi_image"],
                "title":i["hi_title"],
                "ctime":i["oi_ctime"].strftime("%Y-%m-%d"),
                "start_date":i["oi_start_day"].strftime("%Y-%m-%d"),
                "end_date":i["oi_end_day"].strftime("%Y-%m-%d"),
                "amount":str(i["oi_amount"]*100),
                "days":i["oi_count_day"],
                "comment":i["oi_comment"]
            } for i in orders
        ]
        if not data:                                    # 返回查询结果
            return self.write({"errcode": "0", "errmsg": "查询成功"})
        return self.write({"errcode": "0", "errmsg": "查询成功","orders":data})


class OrderHandler(BaseHandler):
    """接单/拒单/评论接口"""
    @login_decorate
    def post(self):
        try:
            commit = self.json_args["commit"]           # 获取请求类别
            order_id = self.json_args["order_id"]       # 获取订单id
            user_id = self.session.data["id"]           # 获取客户id
        except Exception as e:
            print e
            return self.write({"errcode":"4103","errmsg":"参数错误"})
        if not all((commit,order_id)):
            return self.write({"errcode":"4103","errmsg":"参数错误"})
        elif "accept" == commit or "reject" == commit:  # 接单或拒单
            try:                                        # 查询订单房屋所属id
                house = self.db.get("select hi_user from order_info left join house_info on oi_house=hi_id where oi_id=%s",order_id)
            except Exception as e:
                print e
                return self.write({"errcode":"4001","errmsg":"数据库错误"})
            if not house:                               # 查询不到或不匹配返回错误信息
                return self.write({"errcode":"4002","errmsg":"无数据"})
            elif house["hi_user"] != user_id:
                return self.write({"errcode":"4105","errmsg":"用户身份错误"})
            else:
                try:
                    if "accept" == commit:              # 接单更新数据库信息
                        self.db.execute("update order_info set oi_status=1 where oi_id=%s",order_id)
                    elif "reject" == commit:
                        try:                            # 拒单更新数据库信息
                            reject_reason = self.json_args["reject_reason"]
                        except Exception as e:
                            print e
                            return self.write({"errcode":"4103","errmsg":"参数错误"})
                        self.db.execute("update order_info set oi_status=6,oi_comment=%s where oi_id=%s",reject_reason,order_id)
                except Exception as e:
                    print e                             # 返回信息
                    return self.write({"errcode":"4001","errmsg":"数据库错误"})
                return self.write({"errcode":"0","errmsg":"修改成功"})
        elif "comment" == commit:                       # 评价接口
            try:
                comment = self.json_args["comment"]
            except Exception as e:
                print e
                return self.write({"errcode":"4103","errmsg":"参数错误"})
            try:                                        # 获取订单客户id
                order = self.db.get("select oi_user from order_info where oi_id=%s",order_id)
            except Exception as e:
                print e
                return self.write({"errcode":"4001","errmsg":"数据库错误"})
            if not order:                               # 判断所属人
                return self.write({"errcode":"4002","errmsg":"无数据"})
            elif order["oi_user"] != user_id:
                return self.write({"errcode":"4105","errmsg":"用户身份错误"})
            else:
                try:                                    # 更新评价信息
                    self.db.execute("update order_info set oi_status=4,oi_comment=%s where oi_id=%s",comment,order_id)
                except Exception as e:
                    print e
                    return self.write({"errcode":"4001","errmsg":"数据库错误"})
                return self.write({"errcode":"0","errmsg":"修改成功"})
