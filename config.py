import os,base64
from flask import Flask
from redis import StrictRedis


class Config(object):
    """配置文件的加载"""

    # 配置秘钥 项目中的CSRF 和session需要用到
    SECRET_KEY = base64.b64encode(os.urandom(148))
    # 开启调试模式
    DEBUG = True

    # 配置MySQL的数据库，其=》app.config[SQLALCHEMY_TRACK_MODIFICATIONS] = False 可以从SQLAlchemy源码查看

    SQLALCHEMY_DATABASE_URI = "mysql://root:mysql@127.0.0.1:3306/flask_project"

    # 不追踪数据库的更改，因为会明显的内存开销
    SQLALCHEMY_TRACK_MODIFICATIONS = Flask

    # 配置Redis的数据库
    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = 6379
    # 配置flask session数据库将session写入到数据库的redis数据库
    # 指定session的数据存储在redis
    SESSION_TYPE = "redis"
    # 告诉session 服务器的位置
    SESSION_REDIS = StrictRedis(host=REDIS_HOST, port=REDIS_PORT)
    # 将session 签名后再存储
    SESSION_USE_SIGNER = True

    SESSION_PERMANENT = True
    # 设置session的有效时间为7天
    PERMANENT_SESSION_LIFETIME = 60*60*24*7