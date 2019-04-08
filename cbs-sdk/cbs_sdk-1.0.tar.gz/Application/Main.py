# coding:utf-8

import logging

import motor
import tornado
import tornado.ioloop
import tornado.web
import os.path

from motor import web, MotorClient
from tornado.options import define, options
from Application.src.config.AppConfig import AppConfig
from Application.src.sdk.controller.IndexHanlder import IndexHandler
from Application.src.sdk.controller.SDKGenHandler import SDKGenHanlder
from Application.src.sdk.controller.SessionInfoHandler import SessionInfoHandler, SessionInfoPageHandler

# 初始化配置
from Application.src.sdk.session import Sessions

define("port", default=AppConfig.port, help="运行端口", type=int)

client = motor.MotorClient("mongodb://127.0.0.1:27017")
db = client[AppConfig.mongdbName]
def init_logging():
    """
        日志文件设置，每天切换一个日志文件
    :return:
    """
    logger = logging.getLogger()
    logger.setLevel("DEBUG")
    sh = logging.StreamHandler()
    file_log = logging.handlers.RotatingFileHandler('scooter_notify.log', maxBytes=10 * 1024 * 1024, backupCount=50)
    formatter = logging.Formatter(
            '[%(asctime)s] [%(levelname)-7s] [%(module)s:%(filename)s-%(funcName)s-%(lineno)d] %(message)s')
    sh.setFormatter(formatter)
    file_log.setFormatter(formatter)
    logger.addHandler(sh)
    logger.addHandler(file_log)
    logging.info("Current log level is : %s", logging.getLevelName(logger.getEffectiveLevel()))


# 启动主类
class Application(tornado.web.Application):
    def __init__(self):
        # 路由器
        handlers = [
            (r"/", IndexHandler),
            (r"/mongostatic/(.*)", web.GridFSHandler, {"database": db}),
            (r"/index", IndexHandler),
            # (r"/sdk/auth/upload", AuthHandler),
            (r"/sdk/nbp/sessioninfo/upload", SessionInfoHandler),
            (r"/sdk/nbp/sessioninfo/getPage", SessionInfoPageHandler),
            (r"/sdk/gensdk", SDKGenHanlder),
        ]
        # 基础配置参数
        settings = dict(
            # cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
            template_path=os.path.join(os.path.dirname(__file__), "static\\html"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies=False,
            db=db,
            cookie_secret="e446976943b4e8442f099fed1f3fea28462d5832f483a0ed9a3d5d3859f==78d",
            session_secret="3cdcb1f00803b6e78ab50b466a40b9977db396840c28307f428b25e2277f1bcc",
            session_timeout=60,
            store_options={
                'redis_host': 'localhost',
                'redis_port': 6379,
                'redis_pass': '',
            },
            # debug模式不好用
            # debug=True,
        )
        # 初始化
        tornado.web.Application.__init__(self, handlers, **settings)
        self.session_manager = Sessions.SessionManager(settings["session_secret"], settings["store_options"], settings["session_timeout"])


# xsrf攻击
# def xsrf_form_html(self):
#     return '<input type="hidden" name="_xsrf" value="' + xhtml_escape(self.xsrf_token) + '"/>'


# 主函数
if __name__ == "__main__":

    # Create the application before creating a MotorClient.
    application = Application()
    server = tornado.httpserver.HTTPServer(application)
    server.bind(options.port)
    # Forks one process per CPU.
    application.settings['db'] = MotorClient()[AppConfig.mongdbName]
    server.start()
    tornado.ioloop.IOLoop.instance().start()
    #
    #
    # # Now, in each child process, create a MotorClient.
    # application.settings['db'] = MotorClient().test_database
    # tornado.IOLoop.current().start()


    # app = Application()
    # sockets = tornado.netutil.bind_sockets(8888)
    # tornado.process.fork_processes(0)
    # server = tornado.httpserver.HTTPServer(app)
    #
    # server.add_sockets(sockets)
    # tornado.IOLoop.current().start()
