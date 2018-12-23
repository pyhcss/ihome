# coding=utf-8

import oss2
import hashlib

# 阿里云账号RAM账号的AccessKeyid以及AccessKeySecret
accessKeyid = ''
accessKeySecret = ''


def imagefile(file_name,file_data):
    """上传图片文件 原文件名 文件数据"""
    if not file_data:                       # 如果数据为空 返回None
        return None
    try:                                    # 使用sha1校验生成文件名
        hash_name = hashlib.sha1(file_data).hexdigest()
        new_file_name = hash_name + file_name[-4:]
    except Exception as e:
        print e
        return None                         # 出现错误返回None
    else:
                                            # 生成权限验证的id和key组合
        auth = oss2.Auth(accessKeyid,accessKeySecret)
                                            # 验证权限 外网访问域名 储存空间名
        bucket = oss2.Bucket(auth, 'http://oss-cn-qingdao.aliyuncs.com', 'ssihome')
                                            # 储存文件名 文件二进制数据
        bucket.put_object(new_file_name,file_data)
        return new_file_name


if __name__ == "__main__":
    name = raw_input("请输入要上传的文件")
    with open(name,"rb") as e:
        data = e.read()
    imagefile("abc.jpg",data)
