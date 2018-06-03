from logging.handlers import RotatingFileHandler
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from redis import StrictRedis
from flask_wtf import CSRFProtect
from flask_session import Session
from config import configs
import logging
from flask_wtf import csrf
from logic.utils.comment import do_rank

def setuploggin(level):
    # 设置日志的记录等级
    logging.basicConfig(level=level)
    # 创建日志记录器, 指明日志保存的路径 每个日志文件的最大大小 保存日志文件个数上限
    file_log_handler = RotatingFileHandler("logs/log", maxBytes=1024*1024*100, backupCount=10)
    # 创建日志的格式
    formatter = logging.Formatter('%(levelname)s %(filename)s:%(lineno)d %(message)s')
    # 为刚创建的日志设置日志记录格式
    file_log_handler.setFormatter(formatter)
    # 为全局的日志工具对象(flask app 使用的)添加日志记录器
    logging.getLogger().addHandler(file_log_handler)


# 创建SQLAlchemy的对象
db = SQLAlchemy()
# 创建redis的对象
redis_store = None


def create_app(config_name):
    app = Flask(__name__)
    # 调用日志等级的函数:根据不同的环境,选择不同的日志等级
    setuploggin(configs[config_name].LOGGING_LEVEL)
    # 配置文件的加载
    app.config.from_object(configs[config_name])
    # 创建连接到SQLAlchemy的对象
    # db = SQLAlchemy(app)
    db.init_app(app)

    # 创建连接到Redis的数据库对象
    global redis_store
    redis_store = StrictRedis(host=configs[config_name].REDIS_HOST, port=configs[config_name].REDIS_PORT,decode_responses=True)
    # redis_store.__init__(host=configs[config_name].REDIS_HOST, port=configs[config_name].REDIS_PORT)

    # 开启 CSRF保护：当不适用flaskForm表单类， 但是需要用post请求方法是需自己开启CSRF保护
    CSRFProtect(app)

    # 将过滤器函数变成模板可以使用的过滤器
    app.add_template_filter(do_rank, 'rank')

    # 业务逻辑一开始,通过请求钩子在每次请求结束后写入cookie
    @app.after_request
    def after_request(response):
        # 1.生成csrf_token
        csrf_token = csrf.generate_csrf()
        #2. 将csrf_token写入到浏览器
        response.set_cookie('csrf_token', csrf_token)
        return response


    # 配置flask session 将session 数据写入到服务器的redis的数据库
    Session(app)
    # 蓝图注册到路由
    from logic.modules.index import index_blue
    app.register_blueprint(index_blue)
    from logic.modules.passport import passport_blue
    app.register_blueprint(passport_blue)
    from logic.modules.news import news_blue
    app.register_blueprint(news_blue)
    return app