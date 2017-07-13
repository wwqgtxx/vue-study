#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author wwqgtxx <wwqgtxx@gmail.com>
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from future import standard_library

standard_library.install_aliases()
from builtins import *

import sys
import os
import configparser
import uuid
import threading
import subprocess
import multiprocessing
import time
import functools
import base64
import zlib
import six
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s{%(name)s}%(filename)s[line:%(lineno)d]<%(funcName)s> pid:%(process)d %(threadName)s %(levelname)s : %(message)s',
                    datefmt='%H:%M:%S', stream=sys.stdout)

logger = logging.getLogger("CAT")


def _zlib_base_method(zlib_base_method, input_data, encoding="utf-8", errors='ignore'):
    is_string = isinstance(input_data, str)
    is_bytes = isinstance(input_data, bytes)
    if not is_string and not is_bytes:
        raise Exception("Please provide a string or a byte sequence as \
                        argument for calculation.")
    if is_string:
        input_data = input_data.encode(encoding=encoding, errors=errors)
    return zlib_base_method(input_data) & 0xffffffff


def _base64_base_method(base64_base_method, input_data, return_type=str, encoding="utf-8", errors='ignore'):
    is_string = isinstance(input_data, str)
    is_bytes = isinstance(input_data, bytes)
    if not is_string and not is_bytes:
        raise Exception("Please provide a string or a byte sequence ")
    if is_bytes:
        bytes_string = input_data
    else:
        bytes_string = input_data.encode(encoding=encoding, errors=errors)
    result = base64_base_method(bytes_string)
    if return_type is str:
        return result.decode(errors=errors)
    else:
        return result


base16_encode = functools.partial(_base64_base_method, base64.b16encode)
base16_decode = functools.partial(_base64_base_method, base64.b16decode)
base32_encode = functools.partial(_base64_base_method, base64.b32encode)
base32_decode = functools.partial(_base64_base_method, base64.b32decode)
base64_encode = functools.partial(_base64_base_method, base64.b64encode)
base64_decode = functools.partial(_base64_base_method, base64.b64decode)
if six.PY34:
    base85_encode = functools.partial(_base64_base_method, base64.b85encode)
    base85_decode = functools.partial(_base64_base_method, base64.b85decode)
crc32 = functools.partial(_zlib_base_method, zlib.crc32)
adler32 = functools.partial(_zlib_base_method, zlib.adler32)

MAIN_PATH = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../__main__.py"))


def get_real_path(abstract_path):
    return os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(MAIN_PATH)), abstract_path))


CONFIG = configparser.ConfigParser()
CONFIG.read(get_real_path('config.ini'))


def get_config(key):
    return CONFIG[key]


def create_uuid():
    return uuid.uuid4().hex


class DefaultNamespace(object):
    def __init__(self, default_value=None):
        super(DefaultNamespace, self).__setattr__("_default_value", default_value)

    def __getattribute__(self, item):
        try:
            return super(DefaultNamespace, self).__getattribute__(item)
        except AttributeError:
            pass
        except KeyError:
            pass
        return super(DefaultNamespace, self).__getattribute__("_default_value")


def retry(retry_time=3):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for _ in range(retry_time):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    logger.exception(func.__name__)
                    last_exception = e
            raise last_exception

        return wrapper

    if callable(retry_time):
        func = retry_time
        retry_time = 3
        return decorator(func)
    else:
        return decorator


def import_and_run(module_name, method_name, *args, **kwargs):
    module = __import__(module_name)
    method = getattr(module, method_name)
    return method(*args, **kwargs)
