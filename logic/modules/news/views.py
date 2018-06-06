from logic import constants, db, response_code
from logic.models import User, News, Comment
from . import news_blue
from flask import render_template, session, current_app, g, abort, jsonify, request
from logic.utils.comment import login_in_data


@news_blue.route('/news_collect', methods=['POST'])
@login_in_data
def news_collect():
    """新闻收藏"""

    # 1.获取登录用户信息
    user = g.user
    if not user:
        return jsonify(errno=response_code.RET.SESSIONERR, errmsg='用户未登录')

    # 2. 接受参数：
    news_id = request.json.get('news_id')
    action = request.json.get('action')
    # 3. 校验参数
    if not all([news_id, action]):
        return jsonify(errno =response_code.RET.PARAMERR, errmsg='缺少参数')

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
    if action == 'collect':
        # 此处判断是为了防止用户重复添加收藏新闻
        if news not in user.collection_news:
           user.collection_news.append(news)
    else:
        if news in user.collection_news:
            user.collection_news.remove(news)
    try:
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno =response_code.RET.DBERR, errmsg='操作失败')
    # 6. 响应收藏和取消收藏的结果
    return jsonify(errno =response_code.RET.OK, errmsg='OK')




@news_blue.route('/news_comment',methods=['POST'])
@login_in_data
def news_comment():
    """新闻评论"""
    # 0. 获取登录用户信息
    user = g.user
    if not user:
        return jsonify(errno =response_code.RET.SESSIONERR, errmsg='用户未登录')
    # 1. 接收参数
    news_id = request.json.get('news_id')
    comment_content = request.json.get('comment')
    parent_id = request.json.get('parent_id')

    # 2.校验参数
    if not all([comment_content, news_id]):
        return jsonify(errno =response_code.RET.PARAMERR, errmsg='缺少参数')
    try:
        news_id = int(news_id)
        if parent_id:
            parent_id = int(parent_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno =response_code.RET.PARAMERR, errmsg='参数错误')
    # 3. 查询要评论的新闻是否存在
    try:
        news = News.query.get(news_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno =response_code.RET.DBERR, errmsg='查询新闻失败')
    if not news:
        return jsonify(errno =response_code.RET.NODATA, errmsg='新闻不存在')
    # 4.实现评论新闻和回复内容
    comment = Comment()
    comment.user_id = user.id
    comment.news_id = news_id
    comment.content = comment_content
    if parent_id:
        comment.parent_id = parent_id
    try:
        db.session.add(comment)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(e)
        return jsonify(errno =response_code.RET.DBERR, errmsg='评论失败')
    # 构造响应评论内容
    # data = {
    #     'comment': comment.to_dict()
    # }

    # 5. 响应评论结果
    return jsonify(errno =response_code.RET.OK, errmsg='OK', data=comment.to_dict())





@news_blue.route('/detail/<int:news_id>')
def news_detail(news_id):
    """新闻详情"""

    # 1.获取登录用户信息
    user_id = session.get('user_id', None)
    user = None
    if user_id:
        # 如果有user_id，说明登录中，就取出User模型对象信息
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
    # 5. 展示新闻评论和评论回复
    try:
        comments = Comment.query.filter(Comment.news_id==news_id).order_by(Comment.create_time.desc()).all()
    except Exception as e:
        current_app.logger.error(e)
    comment_dict_list =[]
    for comment in comments:
        comment_dict = comment.to_dict()
        comment_dict_list.append(comment_dict)


    context = {
        'user':user,
        'news_clicks':news_clicks,
        'news':news.to_dict(),
        'is_collected':is_collected,
        'comments': comment_dict_list

    }



    return render_template('news/detail.html',context=context)