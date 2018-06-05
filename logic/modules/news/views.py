from logic import constants, db, response_code
from logic.models import User, News
from . import news_blue
from flask import render_template, session, current_app, g, abort, jsonify, request
from logic.utils.comment import login_in_data


@news_blue.route('/news_collect', methods=['PSOT'])
@login_in_data
def news_collect():
    """新闻收藏"""
    # 1.获取登录用户信息
    user = g.user
    if not user:
        return jsonify(errno =response_code.RET.SESSIONERR, errmsg='用户未登录' )
    # 2. 接受参数：
    news_id = request.get('new_id')
    action = request.get('action')
    # 3. 校验参数
    if not all([news_id, action]):
        return jsonify(errno =response_code.RET.PARAMERR, errmsg='缺少参数')
    if news_id != int(news_id):
        return jsonify(errno =response_code.RET.PARAMERR, errmsg='参数错误')
    if action not in ['collect', 'cancel_collect']:
        return jsonify(errno =response_code.RET.PARAMERR, errmsg='参数错误')
    # 4. 查询当前要收藏或取消收藏的新闻是否存在
    try:
        news = News.query.get(news_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno =response_code.RET.DBERR, errmsg='查询新闻失败')
    if not news:
        return jsonify(errno =response_code.RET.NODATA, errmsg='新闻不存在')
    # 5. 实现收藏和取消收藏
    if action == 'action':
        # 此处判断是为了防止用户重复添加收藏新闻
        if news not in user.collection_news:
           user.collection_news.append(news)
    if action == 'cancel_collect':
        if news in user.collection_news:
            user.collection_news.remove(news)
    try:
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno =response_code.RET.DBERR, errmsg='操作失败')
    # 6. 响应收藏和取消收藏的结果
    return jsonify(errno =response_code.RET.OK, errmsg='OK')







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
    is_collected = False
    if news in user.collection_news:
        is_collected = True

    context = {
        'user':user,
        'news_clicks':news_clicks,
        'news':news.to_dict(),
        'is_collected':is_collected
    }
    return render_template('news/detail.html',context=context)