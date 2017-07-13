#!/usr/bin/env python
# coding=utf-8

import random
import io
import time
import functools

from PIL import Image, ImageDraw, ImageFont, ImageFilter
from werkzeug.routing import NotFound
import flask

from common.utils import logger, base64_encode, base64_decode
from common.csrfprotect import csrf_protect_ajax

from common.db_config import use_mongoengine, use_peewee

if use_mongoengine:
    from common.db_config import mongoengine


    class ValidateCode(mongoengine.Document):
        string = mongoengine.StringField(required=True, unique=True)
        base64_img = mongoengine.StringField(required=True)
        meta = {"collection": "VALIDATE_CODE",
                # 'indexes': ['string']
                }

if use_peewee:
    from common.db_config import peewee, db, BaseModel


    class ValidateCode(BaseModel):
        string = peewee.CharField(primary_key=True, unique=True)
        base64_img = peewee.CharField()

        class Meta:
            db_table = "VALIDATE_CODE"

# map:将str函数作用于后面序列的每一个元素
numbers = ''.join(map(str, range(10)))


def create_validate_code(string=None, size=(120, 40), chars=numbers, mode="RGB", bg_color=(255, 255, 255),
                         fg_color=(255, 0, 0), font_size=22, font_type="common/monaco.ttf", length=4, draw_points=True,
                         point_chance=2):
    """
    response = app.make_response(img_bytes)
    response.headers['Content-Type'] = 'image/jpeg'
    return response
    :param string: 生成指定字符串的图片,如果为空，则随机生成
    :param size: 图片的大小，格式（宽，高），默认为(120, 40)
    :param chars: 允许的字符集合，格式字符串
    :param mode: 图片模式，默认为RGB
    :param bg_color: 背景颜色，默认为白色
    :param fg_color: 前景色，验证码字符颜色
    :param font_size: 验证码字体大小
    :param font_type: 验证码字体，默认为 monaco.ttf
    :param length: 验证码字符个数
    :param draw_points: 是否画干扰点
    :param point_chance: 干扰点出现的概率，大小范围[0, 50]
    :return: img_bytes, strs
    """

    width, height = size
    img = Image.new(mode, size, bg_color)  # 创建图形
    draw = ImageDraw.Draw(img)  # 创建画笔

    def get_chars():
        """生成给定长度的字符串，返回列表格式"""
        return random.sample(chars, length)

    def create_points():
        """绘制干扰点"""
        chance = min(50, max(0, int(point_chance)))  # 大小限制在[0, 50]

        for w in range(width):
            for h in range(height):
                tmp = random.randint(0, 50)
                if tmp > 50 - chance:
                    draw.point((w, h), fill=(0, 0, 0))

    def create_strs():
        """绘制验证码字符"""
        c_chars = string if string else get_chars()
        strs = '%s' % ''.join(c_chars)

        font = ImageFont.truetype(font_type, font_size)
        font_width, font_height = font.getsize(strs)

        draw.text(((width - font_width) / 3, (height - font_height) / 4),
                  strs, font=font, fill=fg_color)

        return strs

    if draw_points:
        create_points()
    strs = create_strs()

    # 图形扭曲参数
    params = [1 - float(random.randint(1, 2)) / 100,
              0,
              0,
              0,
              1 - float(random.randint(1, 10)) / 100,
              float(random.randint(1, 2)) / 500,
              0.001,
              float(random.randint(1, 2)) / 500
              ]
    img = img.transform(size, Image.PERSPECTIVE, params)  # 创建扭曲

    img = img.filter(ImageFilter.EDGE_ENHANCE_MORE)  # 滤镜，边界加强（阈值更大）

    buf = io.BytesIO()
    img.save(buf, 'JPEG', quality=70)

    img_bytes = buf.getvalue()

    return img_bytes, strs


def generate_validate_code_to_db(string=None):
    if string:
        if use_mongoengine:
            query_set = ValidateCode.objects(string=string)
            if query_set.count():
                return query_set.first().base64_img
        elif use_peewee:
            with db.execution_context():
                query_set = ValidateCode.select().where(ValidateCode.string == string)
                if query_set.count():
                    return query_set.first().base64_img
        start_time = time.time()
        img_bytes, strs = create_validate_code(string)
        end_time = time.time()
        logger.info("create_validate_code <%s> use time: %f s" % (strs, (end_time - start_time)))

        encode_img = base64_encode(img_bytes, return_type=str)
        size = len(encode_img)
        logger.info("encode_img length = %d" % size)

        start_time = time.time()
        if use_mongoengine:
            ValidateCode(string=string, base64_img=encode_img).save()
        elif use_peewee:
            with db.execution_context():
                ValidateCode.create(string=string, base64_img=encode_img)
        end_time = time.time()
        logger.info("insert <%s> to mongodb use time: %f s" % (strs, (end_time - start_time)))
        return encode_img
    if use_peewee:
        with db.execution_context():
            # Only create the tables if they do not exist.
            db.create_tables([ValidateCode], safe=True)
    time1 = time.time()
    total_size = 0
    for num in range(10000):
        string = "%04d" % num
        if use_mongoengine:
            if ValidateCode.objects(string=string).count():
                logger.info("validate_code <%s> was already in mongodb, skip it" % string)
                continue
        elif use_peewee:
            with db.execution_context():
                if ValidateCode.select().where(ValidateCode.string == string).count():
                    logger.info("validate_code <%s> was already in mongodb, skip it" % string)
                    continue
        # 把strs发给前端,或者在后台使用session保存
        start_time = time.time()
        img_bytes, strs = create_validate_code(string)
        end_time = time.time()
        logger.info("create_validate_code <%s> use time: %f s" % (strs, (end_time - start_time)))

        encode_img = base64_encode(img_bytes, return_type=str)
        size = len(encode_img)
        total_size += size
        logger.info("encode_img length = %d" % size)
        logger.info("total_size = %d" % total_size)

        start_time = time.time()
        if use_mongoengine:
            ValidateCode(string=string, base64_img=encode_img).save()
        elif use_peewee:
            with db.execution_context():
                ValidateCode.create(string=string, base64_img=encode_img)
        end_time = time.time()
        logger.info("insert <%s> to mongodb use time: %f s" % (strs, (end_time - start_time)))
    time2 = time.time()
    logger.info("total use time: %f s" % (time2 - time1))
    logger.info("total_size = %d" % total_size)


def get_validate_code_from_db(string=None):
    if not string:
        num = random.randint(0, 9999)
        string = "%04d" % num
    # start_time = time.time()
    encode_img = generate_validate_code_to_db(string)
    # end_time = time.time()
    # logger.info("create_validate_code <%s> use time: %f s" % (string, (end_time - start_time)))
    # logger.info(encode_img)
    return string, encode_img


def check_validate_code(func):
    if callable(func):
        @functools.wraps(func)
        def check_validate_code_wrapper(*args, **kwargs):
            _validate_code_string = flask.session.pop('_validate_code_string', None)
            flask.session.pop('_validate_code_img', None)
            validate_code = flask.request.values.get('validate_code', None)
            if flask.request.method == "POST" or validate_code:
                if not validate_code or not _validate_code_string or validate_code != _validate_code_string:
                    flask.session['WRONG_VALIDATE_CODE'] = True
                else:
                    flask.session.pop('WRONG_VALIDATE_CODE', None)
            else:
                flask.session.pop('WRONG_VALIDATE_CODE', None)
            need_remove_alert_cookie = not flask.session.get("NO_REMOVE_ALERT_COOKIE", False)
            response = flask.make_response(func(*args, **kwargs))
            if is_validate_code_wrong():
                response.set_cookie('WRONG_VALIDATE_CODE', 'True')
            elif need_remove_alert_cookie:
                response.delete_cookie('WRONG_VALIDATE_CODE')
            return response

        return check_validate_code_wrapper
    else:
        _validate_code_string = flask.session.pop('_validate_code_string', None)
        flask.session.pop('_validate_code_img', None)
        validate_code = func
        logger.info(_validate_code_string)
        logger.info(validate_code)
        if not validate_code or not _validate_code_string or validate_code != _validate_code_string:
            return False
        return True


def is_validate_code_wrong():
    return flask.session.get('WRONG_VALIDATE_CODE', False)


def validate_code_init(app):
    """
    use by
    
    <img id="img_validate_code" src="data:image/jpeg;base64,{{ validate_code_img() }}" style="cursor: pointer;">
    :param app: 
    :return: 
    """
    app.jinja_env.globals['validate_code_img'] = get_validate_code_img

    @app.route('/api/validate_code/', methods=['POST'])
    # @csrf_protect_ajax
    def refresh_validate_code():
        flask.session.pop('_validate_code_string', None)
        encode_img = get_validate_code_img()
        return flask.jsonify({
            "encode_img": encode_img
        })


def get_validate_code():
    if '_validate_code_string' not in flask.session:
        string, encode_img = get_validate_code_from_db()
        flask.session['_validate_code_string'] = string
        flask.session['_validate_code_img'] = encode_img
    return flask.session['_validate_code_string'], flask.session['_validate_code_img']


def get_validate_code_string():
    return get_validate_code()[0]


def get_validate_code_img():
    return get_validate_code()[1]
