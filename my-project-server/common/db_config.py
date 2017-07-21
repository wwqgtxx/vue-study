#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author wwqgtxx <wwqgtxx@gmail.com>
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from future import standard_library

standard_library.install_aliases()
from builtins import *
from common.utils import logger

use_mongoengine = False
use_mysql = False
use_sqlite = True

if use_mongoengine:
    try:
        import mongoengine
        import mongoengine.base as mongoengine_base
    except ImportError:
        logger.warning("can't import mongoengine")
        mongoengine = None
        use_mongoengine = False

use_peewee = False
if use_mysql or use_sqlite:
    try:
        import peewee

        use_peewee = True
    except ImportError:
        logger.warning("can't import peewee")
        peewee = None

if use_peewee:
    if use_mysql:
        db = peewee.MySQLDatabase("TestServer", user="root", password="wwq")
    elif use_sqlite:
        db = peewee.SqliteDatabase("TestServer.db")
    else:
        use_peewee = False


    class BaseModel(peewee.Model):
        class Meta:
            database = db

if use_mongoengine:
    import mongoengine

    mongoengine.connect(db="TestServer")
