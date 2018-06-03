from logic import constants
from logic.models import User, News
from . import news_blue
from flask import render_template, session, current_app


@news_blue.route('/detail/<int:news_id>')
def news_detail(news_id):
    """新闻详情"""
    # 1. 获取登录用户信息
    user_id = session.get('user_id', None)
    user = None
    if user_id:
        try:
            user = User.query.get(user_id)
        except Exception as e:
            current_app.logger.error(e)
    # 2. 点击排行:查询新闻数据,根据clicks点击属性实现倒序
    news_clicks = []
    try:
        news_clicks = News.query.order_by(News.clicks.desc()).limit(constants.CLICK_RANK_MAX_NEWS)
    except Exception as e:
        current_app.logger.error(e)

    context = {
        'user':user,
        'news_clicks':news_clicks
    }
    return render_template('news/detail.html',context=context)