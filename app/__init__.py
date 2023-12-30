# -*- coding: utf-8 -*-
"""
    :copyright: (c) 2023 by Jeffrey.
    :license: Apache 2.0, see LICENSE for more details.
"""
import atexit
import datetime
import fcntl
import logging
import os
from logging.handlers import TimedRotatingFileHandler

from dotenv import load_dotenv
from flask import Flask, request, g
from flask_apscheduler import APScheduler
from flask_cors import CORS
from flask_migrate import Migrate
from flask_socketio import SocketIO
from redis import StrictRedis
from werkzeug.exceptions import HTTPException

from .api.socket.chat import ChatNameSpace
from .lib.exception import APIException, ServerError, HeaderInvalid, AuthorizationInvalid, TokenInvalid
from .lib.token import auth, verify_token
from .model.base import db
from .patch.encoder import JSONEncoder

migrate = Migrate(db=db, render_as_batch=True, compare_type=True, compare_server_default=True)
cors = CORS(resources={'/*': {'origins': '*'}})
socketio = SocketIO(cors_allowed_origins='*')
scheduler = APScheduler()

# 存放微信令牌
access_token_db: StrictRedis
# 存放聊天室用户
chat_room_db: StrictRedis


def create_app():
    """
    创建应用
    """
    # 载入环境变量
    load_dotenv()
    app = Flask(__name__)

    register_config(app)
    register_logging(app)
    register_extension(app)
    register_socket(app)
    register_scheduler(app)
    register_redis(app)
    register_header(app)
    register_exception(app)
    register_encoder(app)
    register_resource(app)

    return app


def register_config(app):
    """
    注册配置
    """
    flask_env = app.config.get('ENV')
    app.config.from_object(f"app.config.{flask_env}.{flask_env.capitalize()}Config")


def register_logging(app):
    """
    注册日志
    """
    log_file = os.path.join('log', f"app-{datetime.date.today().strftime('%Y%m%d')}.log")
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(filename)s:%(lineno)d %(message)s')
    handler = TimedRotatingFileHandler(log_file, when='midnight', backupCount=90, encoding='UTF-8')
    handler.setFormatter(formatter)
    handler.setLevel(app.config['LOG_LEVEL'])
    app.logger.addHandler(handler)

    @app.before_first_request
    def prod_logging():
        if not app.debug:
            stream_handler = logging.StreamHandler()
            stream_handler.setFormatter(formatter)
            app.logger.addHandler(stream_handler)
            app.logger.setLevel(app.config['LOG_LEVEL'])


def register_extension(app):
    """
    注册扩展
    """
    db.init_app(app)
    migrate.init_app(app)
    cors.init_app(app)


def register_socket(app):
    """
    注册 Socket
    """
    socketio.init_app(app)
    socketio.on_namespace(ChatNameSpace('/socket/chat'))


def register_scheduler(app):
    """
    注册 Scheduler
    """
    scheduler.init_app(app)

    if app.debug and not scheduler.running:
        scheduler.start()

    f = open('scheduler.lock', 'wb')
    # noinspection PyBroadException
    try:
        fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
        scheduler.start()
    except:
        pass

    def unlock():
        fcntl.flock(f, fcntl.LOCK_UN)
        f.close()

    atexit.register(unlock)


def register_redis(app):
    """
    注册 Redis
    """
    global access_token_db
    global chat_room_db

    redis_config = {
        'host': app.config['REDIS_HOST'],
        'port': app.config['REDIS_PORT'],
        'password': app.config['REDIS_PASSWORD'],
        'decode_responses': True,
        'health_check_interval': 30
    }
    access_token_db = StrictRedis(**redis_config, db=app.config['REDIS_ACCESS_TOKEN_DB'])
    chat_room_db = StrictRedis(**redis_config, db=app.config['REDIS_CHAT_ROOM_DB'])


def register_header(app):
    """
    注册请求头
    """

    @app.before_request
    def app_name_validator():
        if 'APP_NAME' not in app.config:
            return
        if request.path in app.config['ALLOWED_PATH'] or '*' in app.config['ALLOWED_PATH']:
            return
        if 'X-App-Name' not in request.headers or request.headers['X-App-Name'] != app.config['APP_NAME']:
            raise HeaderInvalid

    @app.before_request
    def authorization_validator():
        g.user = None
        if 'Authorization' not in request.headers:
            return
        try:
            scheme, token = request.headers.get('Authorization', '').split(None, 1)
        except ValueError:
            raise AuthorizationInvalid
        if scheme != auth.scheme:
            raise TokenInvalid
        verify_token(token=token)


def register_exception(app):
    """
    注册全局异常
    """

    @app.errorhandler(Exception)
    def handle_error(e):
        if isinstance(e, APIException):
            return e
        elif isinstance(e, HTTPException):
            return APIException(code=e.code, msg_code=e.code, msg=e.name)
        else:
            app.logger.error({
                'error': e,
                'path': request.path,
                'args': request.args.to_dict(),
                'data': request.get_json(silent=True)
            })
            if not app.debug:
                return ServerError()
            raise e


def register_encoder(app):
    """
    注册编码器
    """
    app.json_encoder = JSONEncoder


def register_resource(app):
    """
    注册资源
    """
    from .api.v2 import create_v2

    app.register_blueprint(create_v2(), url_prefix='/v2')
