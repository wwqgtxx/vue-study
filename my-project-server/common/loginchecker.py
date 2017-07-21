#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author wwqgtxx <wwqgtxx@gmail.com>
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from future import standard_library

standard_library.install_aliases()
from builtins import *
from threading import Thread
import functools
import time
import hashlib
import uuid
import flask
import itsdangerous
from datetime import datetime, timedelta
from enum import Enum
from werkzeug.security import check_password_hash, generate_password_hash
from common.utils import logger, DefaultNamespace
from common.db_config import use_mongoengine, use_peewee

use_sha3 = False

if use_sha3:
    try:
        hashlib.algorithms = hashlib.algorithms_available
        import werkzeug.security

        werkzeug.security._hash_funcs = werkzeug.security._find_hashlib_algorithms()
        werkzeug.security._has_native_pbkdf2 = None
    except AttributeError:
        use_sha3 = False

try:
    import flask_socketio
except ImportError:
    logger.warning("can't import flask_socketio")
    flask_socketio = None

try:
    import flask_admin
except ImportError:
    logger.warning("can't import flask_admin")
    flask_admin = None

from common.csrfprotect import csrf_protect, csrf_protect_ajax, get_csrf_token
from common.validate_code import check_validate_code, is_validate_code_wrong


class ReturnType(Enum):
    JSON = "JSON"
    DISCONNECT = "DISCONNECT"


if use_mongoengine:
    from common.db_config import mongoengine


    class User(mongoengine.Document):
        username = mongoengine.StringField(required=True, unique=True)
        password = mongoengine.StringField(required=True)
        role = mongoengine.StringField(required=True, default="normal")
        is_admin = mongoengine.BooleanField(required=True, default=False)
        meta = {"collection": "USER_INFO"}


    class UserLoginData(mongoengine.Document):
        uid = mongoengine.UUIDField(required=True, unique=True)
        user = mongoengine.ReferenceField(User)
        username = mongoengine.StringField(required=True)
        timestamp = mongoengine.LongField(required=True)
        datetime = mongoengine.DateTimeField(required=True)
        utc_datetime = mongoengine.DateTimeField(required=True)
        meta = {"collection": "USER_LOGIN"}

if use_peewee:
    from common.db_config import peewee, db, BaseModel


    class User(BaseModel):
        id = peewee.CharField(primary_key=True, unique=True)
        username = peewee.CharField(unique=True)
        password = peewee.CharField()
        role = peewee.CharField(default="normal")
        is_admin = peewee.BooleanField(default=False)

        class Meta:
            db_table = "USER_INFO"


    class UserLoginData(BaseModel):
        uid = peewee.CharField(primary_key=True, unique=True)
        user = peewee.ForeignKeyField(User)
        username = peewee.CharField()
        timestamp = peewee.BigIntegerField()
        datetime = peewee.DateTimeField()
        utc_datetime = peewee.DateTimeField()

        class Meta:
            db_table = "USER_LOGIN"


class UserWasExist(Exception):
    pass


class LoginChecker(object):
    def __init__(self, only_post=True, ignore_check_user=False, delete_timeout_data=False):
        self.only_post = only_post
        self.ignore_check_user = ignore_check_user
        self.login_view = None
        self.logout_view = None
        self.register_view = None
        self.user_settings_view = None
        self.check_login_view = None
        if delete_timeout_data:
            Thread(target=self.delete_timeout_data).start()
        if use_mongoengine:
            pass
        elif use_peewee:
            with db.execution_context():
                # Only create the tables if they do not exist.
                db.create_tables([User, UserLoginData], safe=True)
        else:
            self.ignore_check_user = True

    def add_user(self, username, password, is_admin=False):
        password = self.generate_password_hash(password)
        if use_mongoengine:
            try:
                user = User(username=username, password=password, is_admin=is_admin)
                user.save()
                logger.info("create new user <username=%s,user_id=%s> into mongodb" % (username, user.id))
                return user
            except mongoengine.NotUniqueError:
                raise UserWasExist
        elif use_peewee:
            try:
                with db.execution_context():
                    user = User.create(id=str(uuid.uuid4()), username=username, password=password, is_admin=is_admin)
                    logger.info("create new user <username=%s,user_id=%s> into mysql" % (username, user.id))
                    return user
            except peewee.PeeweeException:
                raise UserWasExist

    def change_password(self, username, password):
        password = self.generate_password_hash(password)
        if use_mongoengine:
            User.objects(username=username).update_one(password=password)
            user_logon_data_objects = UserLoginData.objects(username=username)  # type:mongoengine.queryset.QuerySet
            user_logon_data_objects.delete()
        elif use_peewee:
            with db.execution_context():
                query = User.update(password=password).where(User.username == username)  # type:peewee.Query
                query.execute()
                query = UserLoginData.delete().where(UserLoginData.username == username)  # type:peewee.Query
                query.execute()

    def change_username(self, username, new_username):
        if use_mongoengine:
            if self.check_has_user(new_username):
                raise UserWasExist
            User.objects(username=username).update_one(username=new_username)
            user_logon_data_objects = UserLoginData.objects(username=username)  # type:mongoengine.queryset.QuerySet
            user_logon_data_objects.modify(username=new_username)
        elif use_peewee:
            if self.check_has_user(new_username):
                raise UserWasExist
            with db.execution_context():
                query = User.update(username=new_username).where(User.username == username)  # type:peewee.Query
                query.execute()
                query = UserLoginData.update(username=new_username).where(
                    UserLoginData.username == username)  # type:peewee.Query
                query.execute()
        self.username = new_username

    def change_role(self, username, role):
        if use_mongoengine:
            User.objects(username=username).update_one(role=role)
        elif use_peewee:
            with db.execution_context():
                query = User.update(role=role).where(User.username == username)  # type:peewee.Query
                query.execute()
        self.role = role

    def check_has_user(self, username):
        if use_mongoengine:
            return True if User.objects(username=username).count() else False
        elif use_peewee:
            with db.execution_context():
                return True if User.select().where(User.username == username).count() else False
        else:
            return False

    def check_password_hash(self, pwhash, password):
        return check_password_hash(pwhash, password)

    def check_user_password(self, username, password):
        user_info = self.get_user_info(username)
        if not user_info:
            if username == "admin":
                self.add_user("admin", "admin", True)
                logger.info('Create default admin user with <username:admin,password:admin>')
                return self.check_user_password(username, password)
            return False
        if self.ignore_check_user:
            return user_info
        db_password = user_info.password
        if self.check_password_hash(db_password, password):
            return user_info
        else:
            return False

    def delete_timeout_data(self, ttl=7):
        if isinstance(ttl, int):
            ttl = timedelta(days=ttl)
        old_datetime = datetime.utcnow() - ttl
        if use_mongoengine:
            result = UserLoginData.objects(utc_datetime__lt=old_datetime).delete()
            logger.info("delete %d timeout data" % result)
        elif use_peewee:
            with db.execution_context():
                query = UserLoginData.delete().where(UserLoginData.utc_datetime < old_datetime)  # type:peewee.Query
                result = query.execute()
                logger.info("delete %d timeout data" % result)

    def generate_password_hash(self, password):
        if use_sha3:
            return generate_password_hash(password, method='pbkdf2:sha3_512')
        else:
            return generate_password_hash(password, method='pbkdf2:sha512')

    def get_user_info(self, username=None, user_id=None):
        if user_id is not None:
            if use_mongoengine:
                return User.objects(id=user_id).first()
            elif use_peewee:
                with db.execution_context():
                    return User.get(User.id == user_id)
        if username is None:
            username = self.username
        if username is None:
            return None
        if self.ignore_check_user:
            user = DefaultNamespace()
            user.username = username
            user.is_admin = (username == "admin")
            user.password = "admin" if (username == "admin") else ""
            user.id = hash(username)
            return user
        if use_mongoengine:
            return User.objects(username=username).first()
        elif use_peewee:
            with db.execution_context():
                try:
                    return User.get(User.username == username)
                except User.DoesNotExist:
                    return None

    def init_view(self, app):
        @app.route('/api/login/', methods=['POST'])
        def api_login():
            data = {"status": "error"}
            if flask.request.is_json:
                json = flask.request.get_json()
                username = json.get('username', None)
                password = json.get('password', None)
                validate_code = json.get('validate_code', None)
                if not validate_code:
                    data["reason"] = "no_validate_code"
                    return flask.jsonify(data)
                if not check_validate_code(validate_code):
                    data["reason"] = "error_validate_code"
                    return flask.jsonify(data)
                if username == '':
                    username = "None"
                if username:
                    user_info = self.check_user_password(username, password)
                    if user_info:
                        uid = str(uuid.uuid1())
                        signed_uid = itsdangerous.Signer(user_info.password, salt='LoginChecker:uid').sign(
                            uid.encode(errors='ignore')).decode(
                            errors='ignore')
                        self.signed_uid = signed_uid
                        self.username = username
                        self.uid = uid
                        self.is_admin = user_info.is_admin
                        self.user_id = user_info.id
                        self.role = user_info.role
                        if use_mongoengine:
                            user_login_data = UserLoginData(uid=uid, user=user_info, username=username,
                                                            timestamp=int(time.time() * 1e3),
                                                            datetime=datetime.now(),
                                                            utc_datetime=datetime.utcnow())
                            user_login_data.save()
                            logger.info("<username=%s,uid=%s> save login with mongodb" % (username, uid))
                        elif use_peewee:
                            with db.execution_context():
                                UserLoginData.create(uid=uid, user=user_info, username=username,
                                                     timestamp=int(time.time() * 1e3),
                                                     datetime=datetime.now(),
                                                     utc_datetime=datetime.utcnow())
                                logger.info("<username=%s,uid=%s> save login with peewee" % (username, uid))
                        data["status"] = "ok"
                        data["username"] = self.username
                        data["is_admin"] = self.is_admin
                        data["role"] = self.role
                        data["uid"] = self.signed_uid
                        data["_csrf_token"] = get_csrf_token()
                        resp = flask.make_response(flask.jsonify(data))
                        self.save_login_info_to_cookie(resp)
                        return resp
                data["reason"] = "error_user"
            else:
                data["reason"] = "no_json"

            return flask.jsonify(data)

        @app.route('/api/logout/', methods=['GET', 'POST'])
        def api_logout():
            data = {"status": "ok"}
            response = flask.make_response(flask.jsonify(data))
            return self.remove_login(response)

        @app.route('/api/register/', methods=['POST'])
        def api_register():
            data = {"status": "error"}
            if flask.request.is_json:
                json = flask.request.get_json()
                username = json.get('username', None)
                password = json.get('password', None)
                validate_code = json.get('validate_code', None)
                if not validate_code:
                    data["reason"] = "no_validate_code"
                    return flask.jsonify(data)
                if not check_validate_code(validate_code):
                    data["reason"] = "error_validate_code"
                    return flask.jsonify(data)
                if username:
                    try:
                        self.add_user(username, password)
                    except UserWasExist:
                        data["reason"] = "user_was_exist"
                        return flask.jsonify(data)
                    data["status"] = "ok"
                    return flask.jsonify(data)
            else:
                data["reason"] = "no_json"
            return flask.jsonify(data)

        @app.route('/api/user_settings/', methods=['POST'])
        @csrf_protect_ajax
        @self.need_login
        def user_settings():
            data = {"status": "error"}
            if flask.request.is_json:
                json = flask.request.get_json()
                username = json.get('username', None)
                password = json.get('password', None)
                if username:
                    try:
                        self.change_username(self.username, username)
                        self.username = username
                        data["status"] = "ok"
                        resp = flask.make_response(flask.jsonify(data))
                        self.save_login_info_to_cookie(resp)
                        return resp
                    except UserWasExist:
                        data["reason"] = "user_was_exist"
                    return flask.jsonify(data)
                if password:
                    self.change_password(self.username, password)
                    data["status"] = "ok"
                    response = flask.make_response(flask.jsonify(data))
                    return self.remove_login(response)
                data["reason"] = "no_message"
            else:
                data["reason"] = "no_json"
            return flask.jsonify(data)

        @app.route('/api/check_login/', methods=['POST', 'GET'])
        def check_login():
            if not self.is_login:
                return flask.jsonify({"status": "ok", "result": "not_login"})
            return flask.jsonify(
                {"status": "ok",
                 "result": "is_login",
                 "username": self.username,
                 "is_admin": self.is_admin,
                 "role": self.role,
                 "uid": self.signed_uid
                 })

    @property
    def is_admin(self):
        return self.is_login and flask.session.get("LoginChecker:is_admin", False)

    @is_admin.setter
    def is_admin(self, value):
        flask.session["LoginChecker:is_admin"] = value

    @is_admin.deleter
    def is_admin(self):
        flask.session.pop("LoginChecker:is_admin", False)

    @property
    def is_login(self):
        if self.username is None:
            username = flask.request.cookies.get('MEMBER_LOGIN', None)
            signed_uid = flask.request.cookies.get('UID', None)
            if username and signed_uid and (use_mongoengine or use_peewee):
                user_info = self.get_user_info(username)
                if user_info:
                    try:
                        uid = itsdangerous.Signer(user_info.password, salt='LoginChecker:uid').unsign(
                            signed_uid).decode(
                            errors='ignore')
                    except itsdangerous.BadData:
                        return False
                    if use_mongoengine:
                        user_login_data = UserLoginData.objects(uid=uid, user=user_info.id, username=username).first()
                        if user_login_data:
                            self.is_admin = user_info.is_admin
                            self.username = username
                            self.uid = uid
                            self.signed_uid = signed_uid
                            self.user_id = user_info.id
                            self.role = user_info.role
                            user_login_data.timestamp = int(time.time() * 1e3)
                            user_login_data.datetime = datetime.now()
                            user_login_data.utc_datetime = datetime.utcnow()
                            user_login_data.save()
                            logger.info("<username=%s,uid=%s> pass login with mongodb" % (username, uid))
                            return True
                        return False
                    elif use_peewee:
                        with db.execution_context():
                            user_login_data = UserLoginData.get(UserLoginData.uid == uid,
                                                                UserLoginData.user == user_info.id,
                                                                UserLoginData.username == username)
                            if user_login_data:
                                self.is_admin = user_info.is_admin
                                self.username = username
                                self.uid = uid
                                self.signed_uid = signed_uid
                                self.user_id = user_info.id
                                self.role = user_info.role
                                user_login_data.timestamp = int(time.time() * 1e3)
                                user_login_data.datetime = datetime.now()
                                user_login_data.utc_datetime = datetime.utcnow()
                                user_login_data.save()
                                logger.info("<username=%s,uid=%s> pass login with peewee" % (username, uid))
                                return True
                            return False
                return False
            return False
        return True

    @is_login.deleter
    def is_login(self):
        del self.username
        del self.uid
        del self.signed_uid
        del self.is_admin
        del self.user_id
        del self.role

    def need_login(self, return_type=ReturnType.JSON, need_admin=False):
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                if (not self.is_login) or (need_admin and not self.is_admin):
                    if return_type is ReturnType.JSON:
                        data = {"status": "error"}
                        if not self.is_login:
                            data["reason"] = "not_login"
                        else:
                            data["reason"] = "not_admin"
                        resp = flask.make_response(flask.jsonify(data))
                        self.remove_login(resp)
                        return resp
                    elif flask_socketio and return_type is ReturnType.DISCONNECT:
                        return flask_socketio.disconnect()
                    else:
                        return False
                if return_type is not ReturnType.DISCONNECT:
                    response = flask.make_response(func(*args, **kwargs))
                    self.save_login_info_to_cookie(response)
                    return response
                else:
                    return func(*args, **kwargs)

            return wrapper

        if callable(return_type):
            func = return_type
            return_type = ReturnType.JSON
            return decorator(func)
        else:
            return decorator

    def remove_login(self, response):
        username = self.username
        uid = self.uid
        del self.is_login
        response.delete_cookie('MEMBER_LOGIN')
        response.delete_cookie('UID')
        response.delete_cookie('IS_ADMIN')
        if username and uid:
            if use_mongoengine:
                UserLoginData.objects(uid=uid, username=username).delete()
                logger.info("<username=%s,uid=%s> remove login with mongodb" % (username, uid))
            elif use_peewee:
                with db.execution_context():
                    query = UserLoginData.delete().where(UserLoginData.uid == uid,
                                                         UserLoginData.username == username)  # type:peewee.Query
                    query.execute()
                    logger.info("<username=%s,uid=%s> remove login with peewee" % (username, uid))
        return response

    def remove_user(self, username):
        if use_mongoengine:
            User.objects(username=username).delete()
        elif use_peewee:
            with db.execution_context():
                query = User.delete().where(User.username == username)  # type:peewee.Query
                query.execute()

    @property
    def role(self):
        return flask.session.get('LoginChecker:role', None)

    @role.setter
    def role(self, value):
        flask.session['LoginChecker:role'] = value

    @role.deleter
    def role(self):
        flask.session.pop('LoginChecker:role', None)

    def save_login_info_to_cookie(self, response):
        response.set_cookie('UID', self.signed_uid)
        response.set_cookie('MEMBER_LOGIN', self.username)
        response.set_cookie('IS_ADMIN', str(self.is_admin))

    def set_login_view(self, func):
        self.login_view = func
        return func

    def set_logout_view(self, func):
        self.logout_view = func
        return func

    def set_register_view(self, func):
        self.register_view = func
        return func

    def set_user_settings_view(self, func):
        self.user_settings_view = func
        return func

    def set_check_login_view(self, func):
        self.check_login_view = func
        return func

    @property
    def signed_uid(self):
        return flask.session.get('LoginChecker:signed_uid', None)

    @signed_uid.setter
    def signed_uid(self, value):
        flask.session['LoginChecker:signed_uid'] = value

    @signed_uid.deleter
    def signed_uid(self):
        flask.session.pop('LoginChecker:signed_uid', None)

    @property
    def uid(self):
        return flask.session.get('LoginChecker:uid', None)

    @uid.setter
    def uid(self, value):
        flask.session['LoginChecker:uid'] = value

    @uid.deleter
    def uid(self):
        flask.session.pop('LoginChecker:uid', None)

    @property
    def username(self):
        return flask.session.get("LoginChecker:username", None)

    @username.setter
    def username(self, value):
        flask.session["LoginChecker:username"] = value

    @username.deleter
    def username(self):
        flask.session.pop("LoginChecker:username", None)

    @property
    def user_id(self):
        return flask.session.get("LoginChecker:user_id", None)

    @user_id.setter
    def user_id(self, value):
        flask.session["LoginChecker:user_id"] = value

    @user_id.deleter
    def user_id(self):
        flask.session.pop("LoginChecker:user_id", None)

    @property
    def user_info(self):
        return self.get_user_info()


login_checker = LoginChecker()

if flask_admin:
    if use_mongoengine:
        from flask_admin.contrib.mongoengine import ModelView
    elif use_peewee:
        from flask_admin.contrib.peewee import ModelView
    import wtforms


    class NeedLoginViewMixin(object):
        def is_accessible(self):
            return login_checker.is_admin

        def inaccessible_callback(self, name, **kwargs):
            # redirect to login page if user doesn't have access
            return flask.redirect("/")


    class UserForm(wtforms.form.Form):
        id = wtforms.fields.StringField('用户ID')
        username = wtforms.fields.StringField('用户名')
        password2 = wtforms.fields.PasswordField('密码')
        role = wtforms.fields.StringField('身份')
        is_admin = wtforms.fields.BooleanField('是否为管理员')


    class UserView(NeedLoginViewMixin, ModelView):
        column_list = ('username', 'role', 'is_admin', 'id')
        column_sortable_list = ('username', 'role', 'is_admin', 'id')
        column_exclude_list = ('password',)
        column_searchable_list = ('username', 'role')
        column_labels = dict(username="用户名", is_admin="是否为管理员", id="用户ID", role='身份')

        form = UserForm

        def __init__(self):
            super(UserView, self).__init__(User, '用户管理')

        def on_model_change(self, form, model, is_created):
            if model.password2:
                model.password = login_checker.generate_password_hash(model.password2)
                del model.password2

            return model


    user_view = UserView()
