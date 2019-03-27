# -*- coding: utf-8 -*-

import logging
from multiprocessing import Process
import socket
import sqlite3
from urllib.parse import urlparse

import tornado.ioloop
import tornado.web

from .ip2loc import ip2loc


db_conn = None


def init_db_conn(sqlite_path_name):
    global db_conn
    db_conn = sqlite3.connect(sqlite_path_name)


# noinspection PyAbstractClass
class IP2LOCHandler(tornado.web.RequestHandler):

    def get(self):
        ip = self.get_argument('ip')
        # noinspection PyTypeChecker
        self.write(ip2loc(conn=db_conn, ip=ip))


# noinspection PyAbstractClass
class Url2LOCHandler(tornado.web.RequestHandler):

    def get(self):
        url = self.get_argument('url')
        if not url.startswith('http://') and not url.startswith('https://'):
            url = f'http://{url}'
        netloc = urlparse(url).netloc
        ip = socket.gethostbyname(netloc)
        # noinspection PyTypeChecker
        self.write(ip2loc(conn=db_conn, ip=ip))


def start_tornado_server(port):
    app = tornado.web.Application([
        (r"/ip2loc", IP2LOCHandler),
        (r"/url2loc", Url2LOCHandler),
    ])
    app.listen(port)
    try:
        tornado.ioloop.IOLoop.current().start()
    except (KeyboardInterrupt, InterruptedError):
        logging.info(f'User interrupt server on port {port}')


def runserver(sqlite_path_name, ports):
    init_db_conn(sqlite_path_name)

    assert len(ports) > 0
    if len(ports) == 1:
        logging.info(f'Starting local server on port {ports[0]}')
    else:
        logging.info(f'Starting local server on ports {ports}')

    for port in ports:
        # noinspection PyBroadException
        try:
            Process(
                target=start_tornado_server, kwargs={'port': port}).start()
            logging.info(f"\n>>>>> Start ip2loc server on port {port} success! <<<<<\n")
        except Exception as e:
            logging.error(f"Start ip2loc server on port {port} fail with error: {e}", exc_info=True)
