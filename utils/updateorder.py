# coding=utf-8

import datetime

def order_status(handler):
    olddate = (datetime.datetime.now()-datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    try:
        handler.db.execute("update order_info set oi_status=5 where oi_end_day=%s and (oi_status=0 or oi_status=1);update order_info set oi_status=3 where oi_end_day=%s and oi_status=2",olddate,olddate)
    except Exception as e:
        print e
