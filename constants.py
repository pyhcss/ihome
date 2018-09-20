# coding=utf-8

REDIS_CAPTCHA_MAX_TIME = 120    # redis图片验证码有效期(秒)
REDIS_TEL_MAX_TIME = 300        # redis手机验证码有效期(秒)
REDIS_EMAIL_MAX_TIME = 300      # redis邮箱验证码有效期(秒)
SESSION_MAX_TIME = 3600         # session有效期(秒)
                                # 图片资源起始链接
IMAGE_URL_START = "http://ssihome.oss-cn-qingdao.aliyuncs.com/"
                                # 房屋默认图片链接
HOUSE_IMAGE_DEFAULT = "eb8b8f329204d0c73395cd8eb214a187d9d5feb4.png"
REDIS_AREA_MAX_TIME = 86400     # 区域信息缓存最长有效期(秒)
REDIS_INDEX_IMAGE_MAX_TIME = 3600 # 主页图片缓存有效期(秒)
REDIS_HOUSE_INFO_MAX_TIME = 3600 # 房屋详情页缓存有效期(秒)
ONE_PAGE_COUNT = 2              # 列表页每页数据个数
REDIS_PAGE_COUNT = 10           # redis房屋列表页缓存数量
REDIS_PAGE_MAX_TIME = 1800      # 房屋列表页缓存有效期(秒)