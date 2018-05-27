# 视图函数
# 导入蓝图对象
from . import index_blue


@index_blue.route('/')
def index():
    return "index"