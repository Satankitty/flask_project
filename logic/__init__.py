from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from redis import StrictRedis
from flask_wtf import CSRFProtect
from flask_session import Session
from config import configs


# 创建SQLAlchemy的对象
db = SQLAlchemy()
# 创建redis的对象
redis_store = StrictRedis()


def create_app(config_name):
    app = Flask(__name__)

    # 配置文件的加载
    app.config.from_object(configs[config_name])
    # 创建连接到SQLAlchemy的对象
    # db = SQLAlchemy(app)
    db.init_app(app)

    # 创建连接到Redis的数据库对象
    # redis_store = StrictRedis(host=configs[config_name].REDIS_HOST, port=configs[config_name].REDIS_PORT)
    redis_store.__init__(host=configs[config_name].REDIS_HOST, port=configs[config_name].REDIS_PORT)

    # 开启 CSRF保护：当不适用flaskForm表单类， 但是需要用post请求方法是需自己开启CSRF保护
    CSRFProtect(app)

    # 配置flask session 将session 数据写入到服务器的redis的数据库
    Session(app)
    return app