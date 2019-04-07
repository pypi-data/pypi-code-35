import json
import mimetypes
import os
import re
import sys
import traceback
import jinja2
from importlib import reload

from FWeb.Http import HttpSession

from FWeb import Utils, Http
from FWeb.Utils import is_file_exist, parse_qs, url_decode


class WebPage:
    """
    一个用于路由函数与状态的列表
    """

    def __init__(self):
        self.page_init = lambda x: None
        self.page_route_map = []
        self.interceptor_route_map = []
        self.error_route_map = []

        @self.e(301)
        def redirect(p):
            if isinstance(p.error, HttpRedirect):
                p.hs.resp_head.set("Location", [p.error.url])

    def init(self):
        def decorator(fun):
            self.page_init = fun

        return decorator

    def p(self, Dir):

        def decorator(fun):
            if callable(Dir):
                def tmp(x):
                    res = Dir(x)
                    if res is False:
                        return False
                    elif type(res) == dict:
                        return res
                    else:
                        return {}

                self.page_route_map.append((tmp, fun))
            else:
                url_and_rex = self.parse_url(Dir)
                self.page_route_map.append((lambda x: self.march_url(x, url_and_rex), fun))

        return decorator

    def i(self, Dir):

        def decorator(fun):
            if callable(Dir):
                def tmp(x):
                    res = Dir(x)
                    if res is False:
                        return False
                    elif type(res) == dict:
                        return res
                    else:
                        return {}

                self.interceptor_route_map.append((tmp, fun))
            else:
                url_and_rex = self.parse_url(Dir)
                self.interceptor_route_map.append((lambda x: self.march_url(x, url_and_rex), fun))

        return decorator

    def e(self, error_code):
        def decorator(fun):
            self.error_route_map.append((lambda x: True if error_code == x else False, fun))

        return decorator

    def parse_url(self, url):
        pat = re.compile(r'<|>')
        url_rex = "^"
        val = []
        for i in pat.split(url):
            if not (i.startswith("int") or i.startswith("float") or i.startswith("str") or i.startswith("any")):
                url_rex += i
            else:
                key = ""
                if ":" in i:
                    key = i[i.find(":") + 1:]
                if key != "" and key in val: raise VariableAlreadyDefined()
                val.append(key)
                if i.startswith("int"):
                    url_rex += r'(\d+)'
                elif i.startswith("float"):
                    url_rex += r'([0-9]+[.][0-9]|\d+)'
                elif i.startswith("str"):
                    url_rex += r'([^/]*)'
                elif i.startswith("any"):
                    url_rex += r'([\s\S]*)'
                else:
                    raise UnknownUrlDataType()

        url_rex += "$"

        return val, url_rex

    def march_url(self, url, val_and_rex):
        val, rex = val_and_rex
        rex = re.compile(rex)
        if not rex.match(url): return False

        res = rex.findall(url)
        data = {}
        if len(val) > 0 and type(res[0]) == tuple: res = res[0]
        for i in range(len(val)):
            if val[i] != "":
                data[val[i]] = str(res[i])

        return data


class WebPageHandler:
    """
    调用PageManager里的函数，处理请求
    """

    def __init__(self, Dir, view_path, data, hs: HttpSession, page_manager):
        self.dir = Dir
        self.view_path = view_path
        self.data = data
        self.hs = hs

        self.error = None

        self.view_env = jinja2.Environment(loader=jinja2.FileSystemLoader(searchpath=self.view_path))

        self.page_manager = page_manager
        self.page_manager.page_init(self)

    def echo(self, txt: str):
        self.hs.resp_body += txt.encode()

    def view(self, file, data=None):
        template = self.view_env.get_template(file)
        return template.render(data or {})

    # --------------------参数存在-----------------------------

    def isset_data(self, src, key):
        return key in src.keys()

    def isset_get_data(self, key):
        return self.isset_data(self.data['Get'], key)

    def isset_post_data(self, key):
        return self.isset_data(self.data['Post'], key)

    def isset_pos_pro_data(self, key):
        return self.isset_data(self.data['PostPro'], key)

    def isset_cookie_data(self, key):
        return self.isset_data(self.data['Cookie'], key)

    def isset_url_data(self, key):
        return self.isset_data(self.data['UrlData'], key)

    # --------------------参数获取-----------------------------

    def get_data(self, src, key, Type=str, default=None):
        if key not in src.keys(): return default
        return Type(src[key])

    def get_get_data(self, key, Type=str, default=None):
        return self.get_data(self.data['Get'], key, Type, default)

    def get_post_data(self, key, Type=str, default=None):
        return self.get_data(self.data['Post'], key, Type, default)

    def get_pos_pro_data(self, key, Type=str, default=None):
        return self.get_data(self.data['PostPro'], key, Type, default)

    def get_cookie_data(self, key, Type=str, default=None):
        return self.get_data(self.data['Cookie'], key, Type, default)

    def get_url_data(self, key, Type=str, default=None):
        return self.get_data(self.data['UrlData'], key, Type, default)

    # --------------------------------------------------------

    def handle(self):
        hit = False
        try:
            for key, fun in self.page_manager.interceptor_route_map:  # 匹配检查器
                tmp = key(self.dir)
                if tmp is not False:
                    self.data['UrlData'] = tmp
                    res = fun(self)
                    if not res: return

            for key, fun in self.page_manager.page_route_map:  # 匹配页面
                tmp = key(self.dir)
                if tmp is not False:
                    hit = True
                    self.data['UrlData'] = tmp
                    res = fun(self)

                    if type(res) == str:
                        self.hs.resp_body += res.encode()
                    elif type(res) in (list, dict, tuple):
                        self.hs.resp_body += json.dumps(res).encode()
        except Exception as error:
            self.error_handle(error)

        return hit

    def error_handle(self, error):
        self.error = error
        if not isinstance(error, HttpError):
            self.error = HttpError(500, traceback.format_exc())

        self.hs.resp_head.resp_code = self.error.code
        for key, fun in self.page_manager.error_route_map:
            res = key(self.error.code)
            if res is not False:
                fun(self)
                return
        raise error


class WebApp:
    """
    解析请求所发送的数据，根据module_router等选择调用WebPage
    """

    def __init__(self, view_path, static_path, module_router, error_page=None, web_page=WebPageHandler,
                 page_reload=True):
        """

        :param view_path: 模板页面路径
        :param static_path: 静态文件路径
        :param module_router: WebPage模块或路由函数
        :param error_page: 用于处理全局错误的WebPage模块
        :param page_reload: 是否实时重载WebPage模块
        """
        self.view_path = view_path
        self.static_path = os.path.join(os.path.abspath(os.curdir), static_path)
        self.module_router = module_router
        self.web_page = web_page
        self.page_reload = page_reload
        self.error_page = error_page

    def handle(self, hs):
        url = hs.req_head.get("dir")
        if "?" in url:  # 获取请求路径
            Dir = url_decode((url[0:url.find("?")]))
        else:
            Dir = url_decode(url)
        if Dir[-1] == "/" and Dir != "/": Dir = Dir[:-1]
        if not Dir: raise ErrorUrl("URL为空")

        if callable(self.module_router):  # 执行WebPage页面模块的路由
            page_module = self.module_router(Dir)
        else:
            page_module = self.module_router

        data = None
        try:
            hit = bool(page_module)
            if page_module:  # 命中模块
                if self.page_reload: reload(page_module)
                data = self.parse_data(hs)
                page = self.web_page(Dir, self.view_path, data, hs, page_module.page)  # 构建WebPage
                hit = page.handle()
            if not hit:
                self.handle_static(Dir, hs)
        except HttpError as error:  # 截获未处理异常
            hs.resp_head.resp_code = error.code
            if self.error_page:
                if self.page_reload: reload(self.error_page)
                page = self.web_page(Dir, self.view_path, data, hs, self.error_page.page)
                try:
                    page.error_handle(error)
                except HttpError:
                    pass
        except Exception as error:
            if self.error_page:
                exc = HttpError(500, traceback.format_exc())
                if self.page_reload: reload(self.error_page)
                page = self.web_page(Dir, self.view_path, data, hs, self.error_page.page)
                page.error_handle(exc)
            else:
                raise error

    def handle_static(self, Dir, hs):  # 响应静态文件
        local_dir = self.static_path + Dir.replace("/", Utils.PATH_SEP)
        if not local_dir: raise HttpError(404)
        if not is_file_exist(local_dir): raise HttpError(404)

        with open(local_dir, "rb") as f:
            content_type = str(mimetypes.guess_type(local_dir)[0])
            hs.resp_head.add("Content-Type", content_type)
            hs.resp_body = f.read()

    def parse_data(self, hs: HttpSession):
        # -----------------获取Cookie数据--------------
        cookie = {}
        if hs.req_head.get("COOKIE"):
            cookie = parse_qs(hs.req_head.get("COOKIE"), line_split="; ")

        # -----------------获取Get数据-----------------
        get = {}
        Dir = hs.req_head.get("DIR")
        if "?" in Dir:
            get = parse_qs(Dir[Dir.find("?") + 1:])

        # -----------------获取Post数据----------------
        post = {}
        post_pro = {}
        if hs.req_body:
            if "multipart/form-data" in hs.req_head.content_type.val:
                boundary = hs.req_head.content_type.key_val["boundary"]

                for i in hs.req_body.split(("--" + boundary).encode()):
                    if not i or not "\r\n\r\n".encode() in i or len(i) < 5: continue
                    tmp = MultipartPostData(i)
                    name = tmp.post_head.content_disposition.key_val['name']
                    if name in post_pro.keys():
                        post_pro[name].append(tmp)
                    else:
                        post_pro[name] = [tmp]
                    if (
                            "filename" not in tmp.post_head.content_disposition.key_val.keys() and
                            "boundary" not in tmp.post_head.content_type.key_val.keys()
                    ):  # 若为纯文本数值，加入post简单字典
                        post[name] = url_decode(tmp.post_body)
            else:
                try:
                    post = parse_qs(hs.req_body.decode())
                except Exception:
                    pass

        return {
            "Cookie": cookie,
            "Get": get,
            "Post": post,
            "PostPro": post_pro,
            "UrlData": {}
        }

    def __call__(self, environ, start_response):
        """
        WSGI API
        :param environ:
        :param start_response:
        :return:
        """
        hs = HttpSession()
        hs.req_head.set("METHOD", [environ["REQUEST_METHOD"]])  # 基本HTTP信息
        hs.req_head.set("DIR", [environ["REQUEST_URI"]])
        hs.req_head.set("PROTOCOL", [environ["SERVER_PROTOCOL"]])
        for key, val in environ.items():  # 获取请求头
            if key.startswith("HTTP_"):  # WSGI参考CGI语法
                hs.req_head.add(key[5:], str(val))
        hs.req_head.load_parameters()  # 解析值

        content_length = hs.req_head.get("Content-Length")  # 获取POST数据
        if content_length is not None:
            hs.req_body = environ['wsgi.input'].read(int(content_length))

        self.handle(hs)

        if not hs.resp_head.get("Content-Type"): hs.resp_head.add("Content-Type", "text/html; charset=utf-8")
        resp_head = []
        for k, v in hs.resp_head.data.items():
            for i in v:
                resp_head.append((k, i))
        start_response("%s OK" % hs.resp_head.resp_code, resp_head)
        return [hs.resp_body]


class MultipartPostData:
    """
    multipart/form-data形式的POST数据解析器
    """

    def __init__(self, data):
        self.post_head = data[:data.find("\r\n\r\n".encode())][2:].decode()
        self.post_body = data[data.find("\r\n\r\n".encode()) + 4:][:-2]

        class MultipartPostHead(Http.HttpHead):
            def __init__(self, src=None):
                super(MultipartPostHead, self).__init__()

                if src:
                    src = src.replace("\r", "")
                    for i in src.split("\n"):
                        if not i: continue
                        if ": " in i:
                            k, v = i[:i.find(": ")], i[i.find(": ") + len(": "):]
                        else:
                            k, v = i, ""
                        self.add(k, v)

                    self.content_disposition = Http.MultiParameterVal()
                    self.content_disposition.load(self.get("Content-Disposition"))
                    self.content_type = Http.MultiParameterVal()
                    if self.get("Content-Type"):
                        self.content_disposition.load(self.get("Content-Type"))

        self.post_head = MultipartPostHead(self.post_head)


class ErrorUrl(Exception): pass


class HttpError(Exception):
    def __init__(self, code: int, info: str = ""):
        super(HttpError, self).__init__()
        self.code = code
        self.info = info


class HttpRedirect(HttpError):
    def __init__(self, url):
        super(HttpRedirect, self).__init__(301)
        self.url = url


class VariableAlreadyDefined(Exception): pass


class UnknownUrlDataType(Exception): pass
