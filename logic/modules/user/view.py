from flask import render_template

from . import user_blue


@user_blue.route('/info')
def user_info():
    """个人中心入口"""

    context = {}
    return render_template('news/user.html', context=context)