#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author wwqgtxx <wwqgtxx@gmail.com>
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

TEST_SERVER_MODE = False
FORCE_USE_GEVENT_WEBSOCKET = True
USE_FLASK_SESSION = True

import logging

if TEST_SERVER_MODE:
    LOGGER_LEVEL = logging.DEBUG
else:
    LOGGER_LEVEL = logging.WARNING
logging.getLogger("werkzeug").setLevel(LOGGER_LEVEL)
logging.getLogger("socketio").setLevel(LOGGER_LEVEL)
logging.getLogger("engineio").setLevel(LOGGER_LEVEL)
logging.getLogger("geventwebsocket").setLevel(LOGGER_LEVEL)
logging.getLogger("wsgi").setLevel(logging.INFO)
from common.utils import logger

logger.setLevel(logging.INFO)


def remove_eventlet():
    try:
        __import__("eventlet")
        logger.info('set sys.modules["eventlet"] = None')
        import sys
        sys.modules["eventlet"] = None
        global eventlet
        eventlet = None
    except ImportError:
        pass


gevent = None
try:
    import uwsgi
    import gevent
    import sys

    async_mode = "gevent_uwsgi"
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s{%(name)s}%(filename)s[line:%(lineno)d]<%(funcName)s> %(threadName)s %(levelname)s : %(message)s',
                        datefmt='%H:%M:%S', stream=sys.stdout)
    logger.info("Start server with UWSGI!")
    remove_eventlet()
except ImportError:
    uwsgi = None
    eventlet = None
    async_mode = None
    geventwebsocket = None
    if FORCE_USE_GEVENT_WEBSOCKET:
        try:
            import gevent
            import geventwebsocket

            async_mode = "gevent"
            logger.info("Start server with geventwebsocket!")
            remove_eventlet()
        except ImportError:
            geventwebsocket = None
    if not geventwebsocket:
        try:
            import eventlet

            async_mode = "eventlet"
            logger.info("Start server with eventlet!")
        except ImportError:
            pass
