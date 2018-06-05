from flask import session, current_app,g

from logic.models import User
from functools import wraps


def do_rank(rank):
    if rank ==1:
        return "first"
    elif rank ==2:
        return "second"
    elif rank ==3:
        return "third"
    else:
        return ""

#
# def login_in_user():
#     user_id = session.get('user_id', None)
#     user = None
#     if user_id:
#         try:
#             user = User.query.get(user_id)
#         except Exception as e:
#             current_app.logger.error(e)
#     return user


def login_in_data(view_func):
    """自定义装饰器获取用户登录信息"""
    # 还原装饰器修改后的__name__,还有别装饰函数中的描述信息
    @wraps(view_func)
    def wrapper(*args,**kwargs):
        user_id = session.get('user_id', None)
        user = None
        if user_id:
            try:
                user = User.query.get(user_id)
            except Exception as e:
                current_app.logger.error(e)
        g.user = user
        return view_func(*args,**kwargs)
    return wrapper