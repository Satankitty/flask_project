from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from redis import StrictRedis
from flask_wtf import CSRFProtect
from flask_session import Session
from config import ProductionConfig, DevelopmentConfig, UnittestConfig


app = Flask(__name__)

# 配置文件的加载
app.config.from_object(DevelopmentConfig)
# 创建连接到SQLAlchemy的对象
db = SQLAlchemy(app)

# 创建连接到Redis的数据库对象
redis_store = StrictRedis(host=DevelopmentConfig.REDIS_HOST, port=DevelopmentConfig.REDIS_PORT)

# 开启 CSRF保护：当不适用flaskForm表单类， 但是需要用post请求方法是需自己开启CSRF保护
CSRFProtect(app)

# 配置flask session 将session 数据写入到服务器的redis的数据库
Session(app)