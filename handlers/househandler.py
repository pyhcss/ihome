# coding=utf-8

import math
import json
from time import strftime
from utils import aliyunoss
from utils.decorate import login_decorate
from basehandler import BaseHandler
from constants import *

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
            house_info = self.db.query("select hi_id,hi_title,area_info.ai_name,hi_price,hi_ctime,hi_image from house_info inner join area_info on house_info.hi_area=area_info.ai_id where hi_user=%s order by hi_id desc",user_id)
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
        sql = "insert into house_facilities(hf_type,hf_house) values"
        sql_val = []
        values = []
        for fac_id in facility:                     # 新增配套设施数据
            sql_val.append("(%s,%s)")
            values.append(fac_id)
            values.append(house_id)
        sql += ",".join(sql_val)
        try:
            self.db.execute(sql,*tuple(values))
        except Exception as e:
            print e                                     # 返回错误信息
            try:
                self.db.execute("delete from house_info where hi_id=%s",house_id)
            except Exception as e:
                print e
                return self.write({"errcode":"4001","errmsg":"数据库错误"})
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


class IndexImageHandler(BaseHandler):
    """获取主页图片链接"""
    def get(self):
        try:                                            # 从redis缓存获取数据
            data = self.redis.get("index_image")
        except Exception as e:
            print e
        if data:                                        # 获取成功直接返回
            return self.write({"errcode": "0", "errmsg": "查询成功", "houses": json.loads(data)})
        try:                                            # 查询最新的5条带图片的房屋信息
            houses_info = self.db.query("select hi_id,hi_title,hi_image from house_info where hi_image is not null order by hi_id desc limit 0,5")
        except Exception as e:
            print e                                     # 返回错误信息
            return self.write({"errcode":"4001","errmsg":"数据库错误"})
        houses = []
        for house in houses_info:
            houses.append({                             # 封装数据
                "house_id":house["hi_id"],
                "title":house["hi_title"],
                "img_url":IMAGE_URL_START + house["hi_image"]
            })
        try:                                            # 缓存数据到redis
            self.redis.setex("index_image",REDIS_INDEX_IMAGE_MAX_TIME,json.dumps(houses,ensure_ascii=False).encode("utf-8"))
        except Exception as e:
            print e                                     # 返回数据
        return self.write({"errcode":"0","errmsg":"查询成功","houses":houses})


class HouseInfoHandler(BaseHandler):
    """房屋详情页"""
    def get(self):                                      # 调用方法查询session有无数据
        session_data = self.get_current_user()
        try:
            house_id = self.get_argument("house_id","") # 拿到客户端参数house_id
        except Exception as e:
            print e                                     # 返回错误信息
            return self.write({"errcode":"4103","errmsg":"参数错误"})
        if not house_id:
            return self.write({"errcode":"4103","errmsg":"参数错误"})
        else:
            try:                                        # 从redis缓存获取数据
                data_json = self.redis.get("house_info_%s" %house_id)
            except Exception as e:
                print e
            if data_json:                               # 如果有数据 反序列化
                data = json.loads(data_json)
            else:
                try:                                    # 调用数据库查询相关房屋信息
                    house_info = self.db.get("select hi_price,hi_title,user_info.ui_image,"
                                             "user_info.ui_title,user_info.ui_id,hi_address,"
                                             "hi_count,hi_acreage,hi_type,hi_num,hi_beds,hi_deposit,"
                                             "hi_min_day,hi_max_day from house_info inner join area_info"
                                             " on house_info.hi_area=area_info.ai_id inner join user_info"
                                             " on house_info.hi_user=user_info.ui_id where hi_id=%s",house_id)
                    img_urls = self.db.query("select him_image from house_image where him_house=%s "
                                             "order by him_id desc limit 0,5",house_id)
                    facis = self.db.query("select hf_type from house_facilities where hf_house=%s",house_id)
                    comments = self.db.query("select user_info.ui_title,oi_utime,oi_comment from order_info inner join user_info on oi_user=ui_id where oi_house=%s and oi_status=4 order by oi_utime desc",house_id)
                except Exception as e:
                    print e
                    return self.write({"errcode":"4001","errmsg":"数据库错误"})
                data = {                                # 封装房屋相关信息
                    "images":[IMAGE_URL_START + x["him_image"] for x in img_urls],
                    "price":str(house_info["hi_price"]*100),
                    "title":house_info["hi_title"],
                    "user_avatar":IMAGE_URL_START + house_info["ui_image"],
                    "user_name":house_info["ui_title"],
                    "user_id":house_info["ui_id"],
                    "address":house_info["hi_address"],
                    "room_count":house_info["hi_count"],
                    "acreage":house_info["hi_acreage"],
                    "unit":house_info["hi_type"],
                    "capacity":house_info["hi_num"],
                    "beds":house_info["hi_beds"],
                    "deposit":str(house_info["hi_deposit"]*100),
                    "min_days":house_info["hi_min_day"],
                    "max_days":house_info["hi_max_day"],
                    "facilities":[i["hf_type"] for i in facis],
                    "comments":[{"user_name":i["ui_title"],"ctime":i["oi_utime"].strftime("%Y-%m-%d"),"content":i["oi_comment"]} for i in comments]
                }
                try:                                    # 生成数据缓存
                    self.redis.setex("house_info_%s" %house_id,REDIS_HOUSE_INFO_MAX_TIME,json.dumps(data,ensure_ascii=False).encode("utf-8"))
                except Exception as e:
                    print e
            if not session_data:                        # 如果session_data无相关信息
                return self.write({"errcode":"0","user_id":"","errmsg":"查询成功","data":data})
            else:
                try:                                    # 如果session_data有相关信息
                    return self.write({"errcode":"0","user_id":self.session.data["id"],"errmsg":"查询成功","data":data})
                except Exception as e:
                    print e
                    return self.write({"errcode": "0", "user_id": "", "errmsg": "查询成功", "data": data})


class HouseListHandler(BaseHandler):
    """房屋列表页数据"""
    def get(self):
        try:                                            # 接受客户端参数
            start_date = self.get_argument("sd","")     # 开始时间
            end_date = self.get_argument("ed","")       # 结束时间
            area_id = self.get_argument("aid","")       # 区域id
            sort_key = self.get_argument("sk","new")    # booking销量 price-inc正序 price-des倒序
            page = int(self.get_argument("p","1"))      # 页面编号
        except Exception as e:
            print e
            return self.write({"errcode":"4103","errmsg":"参数错误"})
                                                        # 判断起止时间
        if end_date <= start_date and end_date != "" and start_date !="":
            return self.write({"errcode":"4103","errmsg":"起止时间不能相同"})
        try:                                            # 从缓存数据库获取总页数
            page_count = self.redis.hget("house_list_%s_%s_%s_%s" %(start_date,end_date,area_id,sort_key),"page_count")
        except Exception as e:
            print e
        if page_count:
            if int(page_count) < int(page):             # 如果客户端页数大于总页数
                return self.write({"errcode": "4103", "errmsg": "参数错误"})
            try:                                        # 从缓存数据库获取数据
                data = self.redis.hget("house_list_%s_%s_%s_%s" %(start_date,end_date,area_id,sort_key),str(page))
            except Exception as e:
                print e
            if data:                                    # 返回缓存数据库中的数据信息
                return self.write({"errcode": "0", "errmsg": "查询成功","total_page":page_count,"data":json.loads(data)})
        sql = "select distinct hi_id,hi_image,ui_image,hi_price,hi_title,hi_count,hi_order_count,hi_address from house_info left join order_info on hi_id=oi_house left join user_info on hi_user=ui_id"
        sql_where = []                                  # 条件列表
        sql_data = {}                                   # 参数字典
        if all((start_date,end_date)):                  # 根据起止时间添加查询条件
            sql_where.append("((%(end_date)s <= oi_start_day or %(start_date)s >= oi_end_day) or oi_start_day is null)")
            sql_data["start_date"] = start_date
            sql_data["end_date"] = end_date
        elif start_date:
            sql_where.append("((%(start_date)s < oi_start_day or %(start_date)s >= oi_end_day) or oi_start_day is null)")
            sql_data["start_date"] = start_date
        elif end_date:
            sql_where.append("((%(end_date)s <= oi_start_day or %(end_date)s > oi_end_day) or oi_start_day is null)")
            sql_data["end_date"] = end_date
        if area_id:                                     # 根据城市id添加条件
            sql_where.append("hi_area=%(area_id)s")
            sql_data["area_id"] = area_id
        if sql_where:
            sql += " where "
        sql += " and ".join(sql_where)                  # 组合sql语句
        if sort_key == "new":                           # 根据排序规则组合sql语句
            sql += " order by hi_ctime desc"
        elif sort_key == "booking":
            sql += " order by hi_order_count desc"
        elif sort_key == "price-inc":
            sql += " order by hi_price asc"
        elif sort_key == "price-des":
            sql += " order by hi_price desc"
        try:                                            # 首次查询返回结果
            data = self.db.query(sql,**sql_data)        # 计算总共的页面数
            page_count = int(math.ceil(len(data)/float(ONE_PAGE_COUNT)))
            # if len(data) % ONE_PAGE_COUNT != 0:
            #     page_count = len(data) / ONE_PAGE_COUNT+1
            # else:
            #     page_count = len(data) / ONE_PAGE_COUNT
        except Exception as e:
            print e                                     # 返回错误信息
            return self.write({"errcode":"4001","errmsg":"数据库错误"})
        sql += " limit "+str((page-1)*ONE_PAGE_COUNT) + "," + str(ONE_PAGE_COUNT*REDIS_PAGE_COUNT)
        try:                                            # 组合分页sql语句
            data_sql = self.db.query(sql,**sql_data)    # 查询数据库获得结果
        except Exception as e:
            print e
            return self.write({"errcode": "4001", "errmsg": "数据库错误"})
        a = 1;list = [];redis_data = {};page_index = page
        for i in data_sql:                              # 按照redis中hash缓存查询结果
            list.append({
                "house_id": i["hi_id"],
                "image_url": IMAGE_URL_START + i["hi_image"] if i["hi_image"] else "",
                "avatar": IMAGE_URL_START + i["ui_image"] if i["ui_image"] else "",
                "price": str(i["hi_price"] * 100),
                "title": i["hi_title"],
                "room_count": i["hi_count"],
                "order_count": i["hi_order_count"],
                "address": i["hi_address"]
            })
            if a % ONE_PAGE_COUNT == 0:                 # 按照每页数据量储存
                redis_data[str(page_index)] = json.dumps(list,ensure_ascii=False).encode("utf-8")
                list = []
                page_index += 1
            a += 1
        if list:                                        # 最终剩余数据量最后一次储存
            redis_data[str(page_index)] = json.dumps(list,ensure_ascii=False).encode("utf-8")
        redis_data["page_count"] = page_count           # 缓存页面总数
        redis_key = "house_list_%s_%s_%s_%s" %(start_date,end_date,area_id,sort_key)
        try:                                            # 添加到缓存数据库
            self.redis.hmset(redis_key,redis_data)
            self.redis.expire(redis_key,REDIS_PAGE_MAX_TIME)
        except Exception as e:
            print e
            try:                                        # 出现异常删除缓存
                self.redis.delete(redis_key)
            except Exception as e:
                print e
        if page_count:                                  # 如果页面总数不为0
            return self.write({"errcode": "0", "errmsg": "查询成功","total_page":str(page_count),"data":json.loads(redis_data[str(page)])})
        else:                                           # 如果页面总数为0
            return self.write({"errcode": "0", "errmsg": "查询成功","total_page":str(page_count),"data":[]})
