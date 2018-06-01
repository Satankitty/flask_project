# 视图函数
# 导入蓝图对象
from logic.models import User
from . import index_blue
from flask import render_template, current_app, session


@index_blue.route('/')
def index():
    """主页浏览器右上角用户信息:
    1. 如果未登陆主页右上角显示登陆,注册
    反之,显示用户名"""
    # 1. 从session中取出user_id
    user_id = session.get('user_id', None)
    user = None
    if user_id:
        try:
            user = User.query.get(user_id)
        except Exception as e:
            current_app.logger.error(e)
    context={
        'user':user
    }


    return render_template('news/index.html',context=context)


@index_blue.route('/favicon.ico', methods=['GET'] )
def favicon():
    return current_app.send_static_file('news/favicon.ico')