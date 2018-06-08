from flask import render_template, g, redirect ,url_for
from logic.utils.comment import login_in_data
from . import user_blue


@user_blue.route('/info')
@login_in_data
def user_info():
    """个人中心入口"""
    # 1.获取登录用户信息
    user = g.user
    if not user:
        return redirect(url_for('index.index'))

    # 构造渲染模板的上下文
    context = {
        'user':user
    }
    # 渲染用户中心模板
    return render_template('news/user.html', context=context)