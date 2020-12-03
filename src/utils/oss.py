# coding: utf-8
import oss2
from ext import conf


def upload_local_file(local_file_path, oss_file_path):
    """上传本地文件"""
    auth = oss2.Auth(conf.config['OSS_ALL_KEY'], conf.config['OSS_ALL_SECRET'])
    bucket = oss2.Bucket(
        auth, conf.config['OSS_POINT'], conf.config['OSS_BUCKET'])
    with open(local_file_path, 'rb') as fd:
        bucket.put_object(oss_file_path, fd)


def upload_net_stream_image(image_file_name, file_stream):
    """上传网络流到oss"""
    auth = oss2.Auth(conf.config['OSS_ALL_KEY'], conf.config['OSS_ALL_SECRET'])
    print conf.config['OSS_ALL_KEY'], conf.config['OSS_ALL_SECRET']
    print conf.config['OSS_BUCKET'], conf.config['OSS_POINT']
    bucket = oss2.Bucket(
        auth, conf.config['OSS_POINT'], conf.config['OSS_BUCKET'])
    result = bucket.put_object(image_file_name,
                               file_stream)
    print(result.resp)
    print(result.status)
