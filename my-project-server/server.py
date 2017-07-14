#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author wwqgtxx <wwqgtxx@gmail.com>
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from gevent.monkey import patch_all

patch_all()
from future import standard_library

standard_library.install_aliases()
from builtins import *

from common.webserver_preinit import *

import sys
import os
import random
import time
import queue
import requests
import pickle
import uuid
import binascii
from contextlib import closing
from flask import Flask, request, redirect, url_for, make_response, render_template, session, Response, jsonify
from flask_admin import Admin, BaseView, expose, AdminIndexView
from flask_admin.menu import MenuCategory, MenuView, MenuLink
from flask_babelex import Babel
from flask_socketio import SocketIO, emit, disconnect, join_room, leave_room
from flask_session import Session

app = Flask(__name__, static_folder='../my-project/dist/static', template_folder='../my-project/dist')
babel = Babel(app)
app.config['BABEL_DEFAULT_LOCALE'] = 'zh_CN'
app.secret_key = os.urandom(24)
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
socketio = SocketIO(app, async_mode=async_mode, engineio_logger=True)

from common.loginchecker import login_checker, user_view, ReturnType, NeedLoginViewMixin
from common.validate_code import validate_code_init
from common.utils import DefaultNamespace

namespace = DefaultNamespace()

login_checker.init_view(app)
validate_code_init(app)


class MyHomeView(NeedLoginViewMixin, AdminIndexView):
    pass


admin = Admin(app, name='TEST', index_view=MyHomeView(name="后台首页"), template_mode='bootstrap3')
admin.add_link(MenuLink("首页", "/"))
admin.add_view(user_view)


@app.route('/')
def index():
    return render_template("index.html")


@app.errorhandler(404)
def page_not_found(error):
    return render_template("index.html"), 200


def main(host="0.0.0.0", port=8070):
    logger.info("Start server!")
    # app.run(host="0.0.0.0", port=8070, threaded=True)  # ,debug=True,use_reloader=False)
    if eventlet:
        socketio.run(app, host=host, port=port, debug=False, log=logging.getLogger("wsgi"))
    else:
        socketio.run(app, host=host, port=port, debug=False)
    os._exit(0)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s{%(name)s}%(filename)s[line:%(lineno)d]<%(funcName)s> %(threadName)s %(levelname)s : %(message)s',
                        datefmt='%H:%M:%S', stream=sys.stdout)
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Exit server!")
