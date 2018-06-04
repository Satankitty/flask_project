from logic import constants, db
from logic.models import User, News
from . import news_blue
from flask import render_template, session, current_app, g, abort
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
    # 3.查询和展示新闻详情数据
    news = None
    try:
        news = News.query.get(news_id)
    except Exception as e:
        current_app.logger.error(e)
    if not news:
        abort(404)
    # 4. 更新新闻点击量
    news.clicks += 1
    try:
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()

    context = {
        'user':user,
        'news_clicks':news_clicks,
        'news':news.to_dict()
    }
    return render_template('news/detail.html',context=context)