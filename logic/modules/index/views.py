# 视图函数
# 导入蓝图对象
from logic import constants, response_code
from logic.models import User, News, Category
from . import index_blue
from flask import render_template, current_app, session, request, jsonify


@index_blue.route('/news_list')
def index_news_list():
    """提供主页新闻列表数据"""
    #1. 接收参数(新闻分类id,当前第几页,每页多少条)
    cid = request.args.get('cid', '1')
    page = request.args.get('page', '1')
    per_page = request.args.get('per_page','10')
    #2.校验参数(判断以上参数是否是数字)
    try:
        cid = int(cid)
        page = int(page)
        per_page = int(per_page)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno =response_code.RET.PARAMERR, errmsg = '参数有误' )
    #3.根据参数查询用户需要的数据:根据新闻发布时间倒序,最后实现分页
    if cid ==1:
        paginate = News.query.order_by(News.create_time.desc()).paginate(page, per_page, False)
    else:
        paginate = News.query.filter(News.category_id == cid).order_by(News.create_time.desc()).paginate(page, per_page, False)
    #4.构造相应新闻数据
    news_list = paginate.items
    totle_page = paginate.pages
    current_page = paginate.page
    news_dict_List = []
    for news in news_list:
        news_dict_List.append(news.to_basic_dict())
    data = {
        'news_dict_List':news_dict_List,
        'totle_page':totle_page,
        'current_page':current_page

    }


    #5.响应新闻数据
    return jsonify(errno =response_code.RET.OK, errmsg = 'Ok',data = data)
@index_blue.route('/')
def index():
    """主页浏览器右上角用户信息:
    1. 如果未登陆主页右上角显示登陆,注册
    反之,显示用户名
    2.点击排行
    3. 查询和展示新闻分类标签"""
    # 1. 从session中取出user_id
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
    # 3. 查询和展示新闻分类标签
    categories = []
    try:
        categories = Category.query.all()
    except Exception as e:
        current_app.logger.error(e)

    # 构造模板上下文
    context={
        'user':user,
        'news_clicks':news_clicks,
        'categories':categories
    }


    return render_template('news/index.html',context=context)


@index_blue.route('/favicon.ico', methods=['GET'] )
def favicon():
    return current_app.send_static_file('news/favicon.ico')