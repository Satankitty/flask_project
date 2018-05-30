# 注册和登录
import re,json, random
from flask import request, abort, current_app, make_response, jsonify
from logic.utils.captcha.captcha import captcha
from . import psssport_blue
from logic import redis_store, constants, response_code
from logic.libs.yuntongxun.sms import CCP

@psssport_blue.route('/image_code', )
def image_code():
    """提供图片验证码
    1.接收参数(图片验证码唯一标示 uuid
    2.校验参数(判断参数是否存在)
    3.生成图片验证码
    4.存储图片验证码
    5.相应图片验证码
    """
    # 1.接收参数(图片验证码唯一标识 uuid
    imageCodeId = request.args.get("imageCodeId")
    # 2.校验参数(判断参数是否存在)
    if not imageCodeId:
        abort(403)
    # 3.生成图片验证码:text写入到redis,image相应到浏览器
    name, text, image = captcha.generate_captcha()
    # 4.存储图片验证码
    try:
      redis_store.set('ImageCode:'+imageCodeId, text, constants.IMAGE_CODE_REDIS_EXPIRES)
    except Exception as e:
        current_app.logger.error(e)
        abort(500)
    # 5. 将图片的类型指定为image/ipg
    response = make_response(image)
    response.headers['Content-Type'] = 'image/jpg'
    # 6.相应图片验证码
    return response


def sms_code():
    """发送短信验证码
    1.接受参数(手机号,图片验证码,图片验证码编号)
    2.校验参数(判断参数是否存在,手机号是否合法)
    3.查询服务器存储的图片验证码
    4.跟客户端的传人的图片验证码对比
    5.如果对比成功,生成短信验证码数据
    6.调用CCP()单例类封装的发送短信的方法,发送短信
    7.将短信验证码存储到服务器(将来注册时要判断短信验证码是否正确)
    8.响应发送短信验证码的结果
     """
    # 1.接受参数(手机号, 图片验证码, 图片验证码)
    json_str = request.data
    # 将json字符串转换成json格式
    json_dict = json.load(json_str)
    mobile = json_dict.get("mobile")
    client_image_code = json_dict.get("image_code")
    image_code_id = json_dict.get("image_code_id")
    # 2.校验参数(判断参数是否存在,手机号是否合法)
    if not all([mobile, client_image_code, image_code_id]):
        return jsonify(errno =response_code.RET.PARAMERR, errmsg = '参数不完整' )
    if not re.match(r'^1[345678][0-9]{9}$', mobile):
        return jsonify(errno =response_code.RET.PARAMERR, errmsg = '参数错误' )
    # 3.查询服务器存储的图片验证码
    try:
        server_image_id = redis_store.get('ImageCode:'+image_code_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno =response_code.RET.DBERR, errmsg = '查询图片验证码失败' )
    if not server_image_id:
        return jsonify(errno =response_code.RET.DBERR, errmsg = '图片验证码不存在' )
    # 4.跟客户端的传人的图片验证码对比
    if server_image_id.lower() != client_image_code.lower():
        return jsonify(errno =response_code.RET.PARAMERR, errmsg = '验证码输入有误' )
    # 5.如果对比成功, 生成短信验证码数据
    if server_image_id.lower() == client_image_code.lower():
        # %06d: 不够6位补0 比如67 =>000067
        sms_code = '%06d' % random.radomint(0, 9999)
        result = CCP().send_template_sms(mobile, [sms_code, 2], 1)
    if result != 0:
        return jsonify(errno =response_code.RET.THIRDERR, errmsg = '发送短信验证码失败' )

    # 7.将短信验证码存储到服务器(将来注册时要判断短信验证码是否正确)
    try:
        redis_store.set('sms:' + mobile, sms_code, constants.SMS_CODE_REDIS_EXPIRES)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno =response_code.RET.DBERR, errmsg = '存储短信验证码失败' )
    # 8.响应发送短信验证码的结果
    return jsonify(errno =response_code.RET.OK, errmsg = '发送短信验证码成功' )