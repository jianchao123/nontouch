# coding:utf-8
from aip import AipFace
from ext import conf
import requests
import base64

# res = requests.get(
#     "https://wgxing-test.oss-cn-zhangjiakou.aliyuncs.com/app/avatar/IMG_7223.JPG")
# image = base64.b64encode(res.content).decode("utf8")


rgn_client = AipFace(conf.config['BAIDU_APP_ID'],
                     conf.config['BAIDU_API_KEY'],
                     conf.config['BAIDU_SECRET_KEY'])

################################## 更新 #####################################
# 存在该user_id的用户才能更新 (同一张图片face_id一样)
# d = rgn_client.updateUser(image, "BASE64", "dev", "18508217537")
# print(d) # {'result': {'face_token': 'ce046ec37a5149c05261f12eeff96f1e', 'location': {'left': 127.41, 'rotation': -1, 'top': 143.37, 'height': 139, 'width': 139}}, 'error_msg': 'SUCCESS', 'error_code': 0, 'log_id': 2010012575790, 'timestamp': 1577847657, 'cached': 0}
# if d["error_code"] == 223103:
#     print("用户不存在")
# elif not d["error_code"]:
#     print("更新成功")


################################# 添加 #########################################
# 只有该user_id的用户不存在才能添加
# data = rgn_client.addUser(image, "BASE64", "dev", "18508217534")
# print(data) # {'cached': 0, 'log_id': 3545750555757, 'error_code': 0, 'timestamp': 1577847143, 'result': {'face_token': '54ca60a85fd9cd895b4126cf8678d628', 'location': {'top': 149.97, 'left': 125.87, 'height': 133, 'rotation': 0, 'width': 141}}, 'error_msg': 'SUCCESS'}
# if data["error_code"] == 223105:
#     print("不能重复注册人脸,请先删除以前的子账户或关闭账号")
# elif not data["error_code"]:
#     print("添加成功")

################################ 删除 ###########################################
# face_token = None
# delete_user_mobile = "18508217533"
# d = rgn_client.faceGetlist(delete_user_mobile, "dev")
# print(d)
# if d["error_code"] == 223103:
#     print("用户不存在")
# elif not d["error_code"]:
#     face_token = d["result"]["face_list"][0]["face_token"]
#
# if face_token:
#     d = rgn_client.faceDelete(delete_user_mobile, "dev", face_token)
#     if not d["error_code"]:
#         print("删除成功")
#     else:
#         print("删除失败")

################################ 搜索 ########################################
# d = rgn_client.search(image, "BASE64", "dev")
# import json
# print(json.dumps(d))