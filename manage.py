from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from redis import StrictRedis



class Config(object):
    """配置文件的加载"""

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


@app.route('/')
def index():
    return 'index'
    redis_store.set("name", "zhangsan")

if __name__ == '__main__':
    app.run()