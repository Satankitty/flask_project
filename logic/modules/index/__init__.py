from flask import Blueprint


# 创建蓝图
index_blue = Blueprint('index', __name__)

# 导入views, 保证蓝图注册路由的代码能执行
from . import views
