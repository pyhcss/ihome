# coding=utf-8

REDIS_CAPTCHA_MAX_TIME = 120 # redis图片验证码有效期(秒)
REDIS_TEL_MAX_TIME = 300     # redis手机验证码有效期(秒)
SESSION_MAX_TIME = 3600      # session有效期(秒)
                             # 图片资源起始链接
IMAGE_URL_START = "http://ssihome.oss-cn-qingdao.aliyuncs.com/"
REDIS_AREA_MAX_TIME = 86400  # 区域信息缓存最长有效期(秒)