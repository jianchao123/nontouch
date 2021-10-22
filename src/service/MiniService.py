# coding:utf-8
import requests
import base64
from aip import AipFace
from datetime import date
from decimal import Decimal
import uuid, json, time
from datetime import datetime
from weixin import WeixinLogin
from qiniu import Auth
from sqlalchemy.exc import SQLAlchemyError
from database.db import db
from database.UserProfile import UserProfile
from database.FaceImg import FaceImg

from utils.WXBizDataCrypt import WXBizDataCrypt
from utils.oss import upload_net_stream_image

from ext import conf
from ext import cache
from utils.rest import md5_encrypt


class MiniService(object):

    TOKEN_ID_KEY = 'hash:token.id:{}'
    INVALID_USER_ID = -1
    USER_OPERATIONS = 'user:operations:{}'

    @staticmethod
    def get_login_status(code):
        db.session.commit()
        wx_login = WeixinLogin(conf.config['MINI_APP_ID'],
                               conf.config['MINI_APP_SECRET'])
        try:
            session_info = wx_login.jscode2session(code)
        except:
            return -10
        print(session_info)
        session_key = session_info.get('session_key')
        open_id = session_info.get('openid')
        user = UserProfile.query.filter(
            UserProfile.wx_open_id == open_id).first()

        code = "MINI " + open_id
        if user:
            is_new_user = False
            # 保存登录信息到redis
            k = MiniService.TOKEN_ID_KEY.format(code)
            cache.set(k, user.id)
            cache.expire(k, 60 * 60 * 2)
        else:
            is_new_user = True
            # 仅供sign_up_user使用
            mapping = dict(open_id=open_id, session_key=session_key)
            cache.hmset(code, mapping)
            cache.expire(code, 60)

        return {"is_new_user": is_new_user, "token": code}

    @staticmethod
    def sign_up_user(encrypted_data, iv, token):
        db.session.commit()
        mapping = cache.hmget(token, "open_id", "session_key")
        if not mapping[0] or not mapping[1]:
            return -10

        pc = WXBizDataCrypt(conf.config['MINI_APP_ID'], str(mapping[1]))
        try:
            data = pc.decrypt(encrypted_data, iv)
        except:
            import traceback
            print traceback.format_exc()
            return -11
        mobile = data["purePhoneNumber"]
        user = UserProfile.query.filter(
            UserProfile.mobile == mobile).first()
        if user:
            user.wx_open_id = str(mapping[0])
            new_id = user.id
        else:
            user = UserProfile()
            user.password = md5_encrypt(mobile)
            user.mobile = mobile
            user.wx_open_id = str(mapping[0])
            user.username = mobile
            user.nickname = mobile
            user.is_open_face_rgz = 1
            user.email = '{}@wgx.com'.format(mobile)
            user.is_active = 1
            user.id_card = ''
            user.balance = Decimal(str(0.0))
            user.avatar = ''
            user.gender = 1
            user.birthday = date.today()
            user.company_id = 1 # 无感行

            db.session.add(user)
            db.session.flush()
            new_id = user.id

            # 保存登录信息到redis
            code = "MINI " + mapping[0]
            k = MiniService.TOKEN_ID_KEY.format(code)
            cache.set(k, new_id)
            cache.expire(k, 60 * 60 * 2)
        try:
            db.session.commit()
            return {"phone": mobile, "id": new_id}
        except SQLAlchemyError:
            db.session.rollback()
            return -2
        finally:
            db.session.close()

    @staticmethod
    def signup_face(url, mobile):
        """
        注册人脸(小程序目前没有添加子账户的功能)
        """
        db.session.commit()
        rgn_client = AipFace(conf.config['BAIDU_APP_ID'],
                             conf.config['BAIDU_API_KEY'],
                             conf.config['BAIDU_SECRET_KEY'])
        q = Auth(conf.config['OSS_ALL_KEY'],
                 conf.config['OSS_ALL_SECRET'])
        private_url = q.private_download_url(url, expires=3600)

        # 注册人脸
        user = UserProfile.query.filter(UserProfile.mobile == mobile).first()
        # 向百度注册人脸
        baidu_res = None
        try:
            res = requests.get(private_url)
            image = base64.b64encode(res.content).decode("utf8")
            baidu_res = rgn_client.addUser(
                image, "BASE64", user.mobile, mobile)
            # 已存在百度人脸库,更新
            print(baidu_res)
            if baidu_res["error_code"] == 223105:
                baidu_res = rgn_client.updateUser(
                    image, "BASE64", user.mobile, mobile)
            elif baidu_res["error_code"] == 222203:
                return -10
        except:
            import traceback
            print traceback.format_exc()

        print baidu_res, baidu_res['error_code']
        if not baidu_res or baidu_res["error_code"]:
            return -11
        # 添加face_img记录
        face_img = FaceImg.query.filter(
            FaceImg.baidu_user_id == mobile).first()
        if not face_img:
            face_img = FaceImg()
        face_img.face_last_time = datetime.now()
        face_img.user = user
        face_img.img = ""  # bytes
        face_img.baidu_user_id = mobile
        face_img.group_id = user.mobile
        face_img.oss_url = url
        face_img.is_sub_account = False
        face_img.face_id = baidu_res["result"]["face_token"]
        face_img.face_last_time = datetime.now()
        face_img.status = 1     # 有效
        db.session.add(face_img)
        # 打开人脸功能
        user.is_open_face_rgz = True
        try:
            db.session.commit()
            from msgqueue import producer
            producer.gen_feature(face_img.id, face_img.oss_url)
            return {'id': 0}
        except SQLAlchemyError:
            db.session.rollback()
            return -2
        finally:
            db.session.close()

    @staticmethod
    def upload_oss(image):
        print image
        path = 'backend/Index/MenuManager/'
        current_time = time.time()
        image_file_name = str(current_time).replace(".", "") + ".jpg"
        upload_net_stream_image(path + image_file_name, image)
        url = 'https://{}.{}/{}'.format(conf.config['OSS_BUCKET'],
                                       conf.config['OSS_POINT'],
                                       path + image_file_name)
        return {"path":  url}
