from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from redis import StrictRedis
from flask_wtf import CSRFProtect
import os,base64




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



app = Flask(__name__)

# 配置文件的加载
app.config.from_object(Config)
# 创建连接到SQLAlchemy的对象
db = SQLAlchemy(app)

# 创建连接到Redis的数据库对象
redis_store = StrictRedis(host=Config.REDIS_HOST, port=Config.REDIS_PORT)

#开启 CSRF保护：当不适用flaskForm表单类， 但是需要用post请求方法是需自己开启CSRF保护
CSRFProtect(app)


@app.route('/')
def index():
    return 'index'
    redis_store.set("name", "zhangsan")

if __name__ == '__main__':
    app.run()