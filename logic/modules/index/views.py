# 视图函数
# 导入蓝图对象
from . import index_blue
from flask import render_template


@index_blue.route('/')
def index():
    return render_template('/news/index.html')