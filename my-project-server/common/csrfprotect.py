#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author wwqgtxx <wwqgtxx@gmail.com>
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from future import standard_library

standard_library.install_aliases()
from builtins import *

import uuid
import functools
import flask
from werkzeug.routing import NotFound
from enum import Enum
from common.utils import logger


class SocketIOType(Enum):
    CONNECT = "CONNECT"
    NORMAL = "NORMAL"


_csrf_protect_views = []
_csrf_protect_ajax_views = []


def csrf_protect(view):
    _csrf_protect_views.append(view)
    return view


def csrf_protect_ajax(view):
    _csrf_protect_ajax_views.append(view)
    return view


def csrf_protect_socketio(socketio_type=SocketIOType.NORMAL, socketio=None, namespace=None):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            pass_check_csrf_token = flask.session.get("csrfprotect:pass_check_csrf_token", False)
            if pass_check_csrf_token:
                return func(*args, **kwargs)
            else:
                import flask_socketio
                flask_socketio.disconnect()

        return wrapper

    if callable(socketio_type):
        func = socketio_type
        return decorator(func)
    else:
        if socketio_type == SocketIOType.NORMAL:
            return decorator
        elif socketio_type == SocketIOType.CONNECT:
            @socketio.on("check_csrf_token", namespace=namespace)
            def socketio_csrf_token(csrf_token):
                _csrf_token = get_csrf_token()
                if not csrf_token or not _csrf_token or csrf_token != _csrf_token:
                    return False
                flask.session["csrfprotect:pass_check_csrf_token"] = True
                return True

            def decorator(func):
                return func

            return decorator


def csrf_init(app, on_csrf=None):
    """
    use by
    
    <input type="hidden" name="_csrf_token" value="{{ csrf_token() }}" /> 
    
    or
    
    <meta name="csrf-token" content="{{ csrf_token() }}">
    <script type="text/javascript">
        // var csrftoken = $('meta[name=csrf-token]').attr('content');
        function get_csrftoken() {
            return $.cookie("X-CSRFToken");
        }
        function parse_csrf_token_input(){
            $("input[name='_csrf_token']").val(get_csrftoken());
        }
        
        $(document).ready(function () {
            $.ajaxSetup({
                beforeSend: function (xhr, settings) {
                    if (!this.crossDomain) {
                        xhr.setRequestHeader("X-CSRFToken", get_csrftoken());
                    }
                }
            });
            parse_csrf_token_input();
        });
    </script>
    
    or
    
    <script type="text/javascript">
        var csrftoken = "{{ csrf_token() }}"
    </script>
    :param app: 
    :param on_csrf: 
    :return: 
    """

    @app.before_request
    def _csrf_protect():
        try:
            dest = app.view_functions.get(flask.request.endpoint)
            if dest in _csrf_protect_views:
                if flask.request.method == "POST":
                    _csrf_token = flask.session.get('csrfprotect:_csrf_token', None)
                    csrf_token = flask.request.form.get('_csrf_token', None)
                    if not csrf_token or not _csrf_token or csrf_token != _csrf_token:
                        if on_csrf:
                            on_csrf(*app.match_request())
                        flask.abort(400)
            if dest in _csrf_protect_ajax_views:
                _csrf_token = flask.session.get('csrfprotect:_csrf_token', None)
                csrf_token = flask.request.headers.get("X-CSRFToken", None)
                if not csrf_token or not _csrf_token or csrf_token != _csrf_token:
                    if on_csrf:
                        on_csrf(*app.match_request())
                    data = {"status": "error", "reason": "error_csrf_token"}
                    response = flask.make_response(flask.jsonify(data))
                    return response
                    # flask.abort(400)
        except NotFound:
            pass

    @app.after_request
    def _csrf_protect_add_cookie(response):
        if response and isinstance(response, flask.Response):
            _csrf_token = get_csrf_token()
            response.set_cookie("X-CSRFToken", _csrf_token)
        return response

    app.jinja_env.globals['csrf_token'] = get_csrf_token


def get_csrf_token():
    if 'csrfprotect:_csrf_token' not in flask.session:
        flask.session['csrfprotect:_csrf_token'] = str(uuid.uuid4())
    return flask.session['csrfprotect:_csrf_token']
