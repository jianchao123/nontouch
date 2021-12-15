# coding:utf8
import json
from aip import AipFace
import requests
import base64

res = requests.get(
    "http://wgxing-dev.oss-cn-shanghai.aliyuncs.com/person/face/123456987012365487.png")
image = base64.b64encode(res.content).decode("utf8")


# class Setting(object):
#     BAIDU_APP_ID = '24831558'
#     BAIDU_API_KEY = 'Si8bUb5dIqK4ZwtiKL5tFkKP'
#     BAIDU_SECRET_KEY = 'XNRNi6MpIZjBqfSN0adcOHIPOk2GQVEk'
#
#
# settings = Setting()
#
# rgn_client = AipFace(settings.BAIDU_APP_ID, settings.BAIDU_API_KEY,
#                      settings.BAIDU_SECRET_KEY)
d = {
    'image': image,
    'image_type': 'BASE64',
    'version': 6002,
    'access_token': '24.a16ae9b713123bc5cbf6b53f4e2ae117.2592000.1633863300.282335-24831558'
}
import base64
res = requests.post('https://aip.baidubce.com/rest/2.0/face/v1/feature', d)
if res.status_code == 200:
    d = json.loads(res.content)
    print d
    if d['error_code'] == 0:
        result = d['result']
        if result['face_num'] > 0:
            print result['face_list'][0]['feature']

# NGclO5H1oD3X/o+7NqMVvcVkIb2Z7k09EzLovNy59Ttu+ey8BlqMvUvTtb1R4EW9BbBUvTdWxL0Jol69Mv5BvKylH7wqo7e8XqrjvBRmpT1+7b08e5WFvFTSGr7zIys8GWHGvAif8Lxhi9o9fIsKvcNAjTvXMQi+zgogPSNAhbwrlhW+PYaTPeKiXzqvuu485csVPrr0Mr3nTN08/oF2PUzkIT0JIyi9An5hvX/xPz2TkpI9RDUWvo0FET3tK/o85siBvWQpnD1eA+i9v7gXvVzcEr5YiTE9a6nUPeyXibwMqNa8mUvuPJ6qkrz0N3U9x4rFPDx6Tr3f+6m93IpLvSZ4K700DJ88/exuPDHAmL00UC69UP1bvaRZhDxMD/C91Ol6vTI7mj0D/oK8Q+6YvQYuuL3IkQS94SkxPBu//bsRVv+8IW9XvVnVFr7aKVA9dYTgvMohjzyKnye9hnnwvdjGGL0cVrw8xc6Bvb15ALyHWzK9tMVHPBOMrr1Rcs+7n5Y+PNqHebxuvNE93uCfvf+VOL3xdme8NU45vUqRsL3wPuy7dTkNPeJMMTz/fik9SdQFvrLa/LxqNbM9i4I0vdqnAL3emsk9Vd/RPLjmUT04UJs89TBxPKxO/7wwEYI9wwGkPTPx/zwaQQc9XoQFvB/LHb0DhHc9VDGwPKrasrob1I29g05CO/n1nj14+Mm80a0JPGYFND2wmFy92HNZO2ZZ6L27H/+98KYZPQHhyr2h6769mCSAvQ4pOj028E097z6Wu8qWrrv0UVS97ZoxPU4zfD3p/J+9tVI9vStARL24qxi9JgOXPT8vF73Y2Em8qQi8u8ZcF71xKac9ndPhvfzqD73BYqq9Rp9Wvd9/Vz2PNGI+s7kUvjx25jy39I89WgkAvZPntj235Cm80HPVvNJ4tj00JXg8Lu8Ru+G0Ab7+9li9sxTmO8SkUTxTLaY8KTqtvXZMObpTroS86FgIPkNdeD2c9xy8UCtNvQ0uo7zFuKu9dc+aPOzcADwHL2492t4mvfXbDDwtORg+whJhO+zqJT1jKZq9KDdnO+9LGj3GlRW9xUYHPuEiZzxMa+g8V2sHPlDrXru7BFo8+LujPZE3kbwkea+8cjgZPh7//LtR/2u82QDePReI3Tyynnu9r+FAPeL7ir24mp096v+APQyEwj0ALaU6Q46GvRp8yT2WvJ88BKK7PFnGszzk7ZY9by3oOouY2Ly1O9i8EOsePRvdPb1I4IE9njLdu6Eo8LsOG+W76xahvY6IJD2M7C89e14YubniET1dbNQ8+O4OPYTanz1gkv28ZLd3PdWq9j0NICW9tJaAu0w2obuStDY9/nCDvUKJsz371vW8P1pxPQ==
# hj8IkunJWxZR4j2Z5htEnRXpB4HpJ4YE43/uiTvJXw2yo2myHQMctSbjQbpAxhw9qLU3oNbE56TFa60olbh+rZDTWdFpXc5WcNTUWUradV2/ef3AlU1jR+LX8slGZvLNtntZcVfnYHX9gjJ6DDnHfNKxnGGwN3/mH9ze6WAr/uyPpr4RTsDsFnGlFJgHQ3ye+We2AI60JIQCacSJdwGUjYc4bLAHZmW12c4NuBJsIzx5LBuiL8NqpWz+l6lHf28t34QZUuLjYtRcW2dYlSPaXbHey0H4le1FvZ1oyVrPVM4ENKLyhAe6dus4i/n7PWl996NR4X5JbWVF4M5p8v1r7c7CJJGogxCWLomwGdi9LJ2ZorUA1V2hBLqacgnk5pAMStjuMIJ1hDRq3aE5plxXPXdjAKGbhp6k4W0ErIDCG63E2HBQZgEcVefx+NiNp+pcCDg6QeKWoUVC553Jvtn6TAx5PXKDj4n2KzB3eTJDLX1xn03hGcan5bTOWGnD9znvfFXykV39fhXEfoOZRNdPnedo2wIg2T6F2RJriE7Ms41sViSwKK08NcPnpLnsYgM8qI6VIdviKyV/tMspKzTBLdPW2lF1XGlVExov2RZf4NwKysTBrXnZxZxlV0gJ20LMKfzfcp7dP3ZYv895WjT0/vTbpGH/5AnkpSDL6jbdlu0=
################################## 更新 #####################################
# 存在该user_id的用户才能更新 (同一张图片face_id一样)
# d = rgn_client.updateUser(image, "BASE64", "china", "18508217537")
# print(d) # {'result': {'face_token': 'ce046ec37a5149c05261f12eeff96f1e', 'location': {'left': 127.41, 'rotation': -1, 'top': 143.37, 'height': 139, 'width': 139}}, 'error_msg': 'SUCCESS', 'error_code': 0, 'log_id': 2010012575790, 'timestamp': 1577847657, 'cached': 0}
# if d["error_code"] == 223103:
#     print("用户不存在")
# elif not d["error_code"]:
#     print("更新成功")


################################# 添加 #########################################
# 只有该user_id的用户不存在才能添加
# data = rgn_client.addUser(image, "BASE64", "china", "18508217534")
# print(data) # {'cached': 0, 'log_id': 3545750555757, 'error_code': 0, 'timestamp': 1577847143, 'result': {'face_token': '54ca60a85fd9cd895b4126cf8678d628', 'location': {'top': 149.97, 'left': 125.87, 'height': 133, 'rotation': 0, 'width': 141}}, 'error_msg': 'SUCCESS'}
# if data["error_code"] == 223105:
#     print("不能重复注册人脸,请先删除以前的子账户或关闭账号")
# elif not data["error_code"]:
#     print("添加成功")

################################ 删除 ###########################################
# face_token = None
# delete_user_mobile = "18508217533"
# d = rgn_client.faceGetlist(delete_user_mobile, "china")
# print(d)
# if d["error_code"] == 223103:
#     print("用户不存在")
# elif not d["error_code"]:
#     face_token = d["result"]["face_list"][0]["face_token"]
#
# if face_token:
#     d = rgn_client.faceDelete(delete_user_mobile, "china", face_token)
#     if not d["error_code"]:
#         print("删除成功")
#     else:
#         print("删除失败")

################################ 搜索 ########################################
# d = rgn_client.search(image, "BASE64", "china")
# import json
# print(json.dumps(d))