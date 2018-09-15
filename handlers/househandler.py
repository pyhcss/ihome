# coding=utf-8

import json
from time import strftime
from utils import aliyunoss
from utils.decorate import login_decorate
from basehandler import BaseHandler
from constants import REDIS_AREA_MAX_TIME,IMAGE_URL_START

class AreaHandler(BaseHandler):
    """区域信息接口"""
    def get(self):
        try:                                    # 从缓存数据库获取区域信息
            areas_str = self.redis.get("area_info")
        except Exception as e:
            print e
        if areas_str:                           # 如果有信息则直接返回
            areas = json.loads(areas_str)
        else:                                   # 没有信息从数据库获取
            try:
                ret = self.db.query("select ai_id,ai_name from area_info")
            except Exception as e:
                print e
                return self.write({"errcode":"4001","errmsg":"查询失败"})
            areas = []
            for i in ret:                       # 返回所有区域id name
                area = {"area_id":i["ai_id"],"name":i["ai_name"]}
                areas.append(area)
            try:                                # 添加到redis数据库缓存
                self.redis.setex("area_info",REDIS_AREA_MAX_TIME,json.dumps(areas,ensure_ascii=False).encode("utf-8"))
            except Exception as e:
                print e                         # 返回查询到的区域信息
        return self.write({"errcode":"0","errmsg":"查询成功","areas":areas})


class MyHouseInfoHandler(BaseHandler):
    """查询用户已发布的房源"""
    @login_decorate
    def get(self):
        try:                                    # 从session获取用户id
            user_id = self.session.data["id"]
        except Exception as e:
            print e                             # 返回错误信息
            return self.write({"errcode":"4103","errmsg":"参数错误"})
        houses = []
        try:                                    # 从数据库查询用户发布的房屋信息
            house_info = self.db.query("select hi_id,hi_title,area_info.ai_name,hi_price,hi_ctime,hi_image from house_info inner join area_info on house_info.hi_area=area_info.ai_id where hi_user=%s",user_id)
        except Exception as e:
            print e                             # 返回错误信息
            return self.write({"errcode":"4001","errmsg":"数据库错误"})
        if house_info:                          # 如果有房屋信息 序列化内容
            for house in house_info:
                info = {
                    "house_id":house["hi_id"],
                    "title":house["hi_title"],
                    "area_name":house["ai_name"],
                    "price":str(house["hi_price"] * 100),
                    "ctime":house["hi_ctime"].strftime("%Y-%m-%d"),
                    "img_url":IMAGE_URL_START + house["hi_image"] if house["hi_image"] else ""
                }
                houses.append(info)             # 返回查询结果
        return self.write({"errcode":"0","errmsg":"查询成功","houses":houses})


class NewHouseHandler(BaseHandler):
    """发布新房源接口"""
    @login_decorate
    def post(self):
        try:                                            # 获取客户端信息
            user_id = self.session.data["id"]           # 客户id
            title = self.json_args["title"]             # 房屋标题
            price = self.json_args["price"]             # 房屋单价
            area = self.json_args["area_id"]            # 所属区域
            address = self.json_args["address"]         # 地址
            count = self.json_args["room_count"]        # 房间个数
            acreage = self.json_args["acreage"]         # 房屋面积
            type = self.json_args["unit"]               # 房屋类型
            num = self.json_args["capacity"]            # 容纳人数
            beds = self.json_args["beds"]               # 配床描述
            deposit = self.json_args["deposit"]         # 押金数
            max_day = self.json_args["max_days"]        # 最多入住天数
            min_day = self.json_args["min_days"]        # 最少入住天数
            facility = self.json_args["facility"]       # 配套设施
        except Exception as e:
            print e                                     # 返回错误信息
            return self.write({"errcode":"4103","errmsg":"参数错误"})
        if not all((title,price,area,address,count,type,beds,facility)):
            return self.write({"errcode":"4103","errmsg":"参数错误"})
        try:                                            # 新增数据
            house_id = self.db.execute("insert into house_info(hi_user,hi_title,hi_price,hi_area,hi_address,hi_count,hi_acreage,hi_type,hi_num,hi_beds,hi_deposit,hi_max_day,hi_min_day) "
                                       "values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",user_id,title,price,area,address,count,acreage,type,num,beds,deposit,max_day,min_day)
        except Exception as e:
            print e                                     # 返回错误信息
            return self.write({"errcode":"4001","errmsg":"数据库错误"})
        try:
            for fac_id in facility:                     # 新增配套设施数据
                self.db.execute("insert into house_facilities(hf_type,hf_house) values(%s,%s)",fac_id,house_id)
        except Exception as e:
            print e                                     # 返回错误信息
            return self.write({"errcode":"4001","errmsg":"数据库错误"})
        else:                                           # 返回成功信息
            return self.write({"errcode":"0","errmsg":"创建成功","house_id":house_id})


class HouseImageHandler(BaseHandler):
    """添加房屋图片"""
    @login_decorate
    def post(self):
        try:                                            # 接受用户数据
            house_id = self.get_argument("house_id")
            name = self.request.files["house_image"][0]["filename"]
            data = self.request.files["house_image"][0]["body"]
        except Exception as e:
            print e                                     # 返回错误信息
            return self.write({"errcode":"4103","errmsg":"参数错误"})
        try:                                            # 调用oss保存图片并返回图片名
            new_name = aliyunoss.imagefile(name,data)
        except Exception as e:
            print e                                     # 返回错误信息
            return self.write({"errcode":"4301","errmsg":"第三方错误"})
        if not new_name:
            return self.write({"errcode":"4103","errmsg":"参数错误"})
        try:                                            # 新增房屋图片并更新房屋主图片信息
            self.db.execute("insert into house_image(him_house,him_image) values(%s,%s);update house_info set hi_image=%s where hi_id=%s and hi_image is null",house_id,new_name,new_name,house_id)
        except Exception as e:
            print e                                     # 返回响应信息
            return self.write({"errcode":"4001","errmsg":"数据库错误"})
        return self.write({"errcode":"0","errmsg":"上传成功","url":IMAGE_URL_START + new_name})
