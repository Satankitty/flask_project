from logic import constants
from logic.models import User, News
from . import news_blue
from flask import render_template, session, current_app,g
from logic.utils.comment import login_in_data


@news_blue.route('/news_collect')
@login_in_data
def new_collect():
    """新闻收藏"""
@news_blue.route('/detail/<int:news_id>')
@login_in_data
def news_detail(news_id):
    """新闻详情"""
    # 1. 获取登录用户信息
    user = g.user
    # user = login_in_data()
    # user_id = session.get('user_id', None)
    # user = None
    # if user_id:
    #     try:
    #         user = User.query.get(user_id)
    #     except Exception as e:
    #         current_app.logger.error(e)
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