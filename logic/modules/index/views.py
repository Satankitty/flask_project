# 视图函数
# 导入蓝图对象
from . import index_blue
from logic import redis_store


@index_blue.route('/')
def index():
    redis_store.set("name", "zhangsan")
    return "index"