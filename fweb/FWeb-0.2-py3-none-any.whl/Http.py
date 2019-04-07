import socket
import socketserver
from socketserver import BaseRequestHandler


class FwebTCPServer(socketserver.ThreadingTCPServer):
    def server_bind(self):
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(self.server_address)


def start_server(server_list):
    """
    启动服务器
    :param server_list: 由FwebTCPServer组成的List
    :return:
    """
    from threading import Thread
    for i in server_list:
        t = Thread(target=i.serve_forever)
        t.daemon = True
        t.start()


def get_connection_handler(app):
    """
    获取BaseRequestHandler
    :param app: 执行请求的WebApp
    :return: BaseRequestHandler
    """

    class ConnectionHandler(BaseRequestHandler):
        def setup(self):
            return

        def handle(self):
            keep_alive = True
            keep_alive_times = 0
            while keep_alive:
                keep_alive_times += 1
                data = b""
                req_head = None
                req_body = b""
                content_length = None
                while True:
                    rec = self.request.recv(1024)
                    data += rec
                    if not rec:  # 链接是否断开
                        return
                    if not req_head:
                        if "\r\n\r\n".encode() in data:
                            text = data.split("\r\n\r\n".encode())[0].decode(errors='strict')
                            req_head = HttpReqHead(text)
                            content_length = req_head.get("Content-Length")
                            if not content_length:
                                break
                            else:
                                content_length = int(content_length)
                                req_body += data[data.find("\r\n\r\n".encode()) + 4:]
                                rec = b""

                    if content_length is not None:
                        req_body += rec
                        if len(req_body) >= content_length:
                            break

                hs = HttpSession()
                hs.req_head = req_head
                hs.req_body = req_body
                self.http_handle(hs)

                if hs.req_head.get("Connection") == "close" or keep_alive_times >= 300:
                    keep_alive = False
                    hs.resp_head.set("Connection", ["close"])
                hs.resp_head.set("Content-Length", [str(len(hs.resp_body))])
                data = (hs.resp_head.dump() + "\r\n").encode() + hs.resp_body
                self.request.sendall(data)

            return

        def http_handle(self, hs):
            if hs.req_head.protocol != "HTTP/1.1":  # 未知请求协议
                hs.resp_head.resp_code = 505
                hs.resp_head.resp_msg = "HTTP Version Not Supported"
                return
            if hs.req_head.method in ("GET", "POST", "PUT", "DELETE"):  # 交由APP处理
                app.handle(hs)

                if not hs.resp_head.get("Content-Type"): hs.resp_head.add("Content-Type", "text/html; charset=utf-8")
                if hs.resp_head.get("Location"): hs.resp_head.set("First-line", ["HTTP/1.1 301 OK"])
            elif hs.req_head.method == "HEAD":
                app.handle(hs)
                hs.resp_body = b""
            elif hs.req_head.method == "OPTIONS":
                hs.resp_head.set("Allow", ["OPTIONS, GET, POST, PUT, DELETE, HEAD"])
            else:  # 未知请求方法
                hs.resp_head.resp_code = 405
                hs.resp_head.resp_msg = "Method Not Allowed"

        def finish(self):
            return

    return ConnectionHandler


class HttpSession:
    """
    http请求会话类。包含请求和响应的头部和数据
    """

    def __init__(self):
        self.req_head = HttpReqHead()
        self.req_body = b""
        self.resp_head = HttpRespHead()
        self.resp_body = b""


class MultiParameterVal:
    """
    可变多节的参数。例如Content-Type: multipart/form-data; boundary=something
    其包含多杰参数
    """

    def __init__(self, upper_remove=False, unique=True):
        self.upper_remove = upper_remove
        self.unique = unique
        self.key_val = {}
        self.val = []

    def load(self, src):
        src = src.split("; ")
        for i in src:
            if "=" in i:
                key = i[:i.find("=")]
                val = i[i.find("=") + 1:]
                key = key.lower()
                self.key_val[key] = val
            else:
                if self.upper_remove: i.lower()
                self.val.append(i)
                if self.unique: self.val = list(set(self.val))


class QualityValues:
    """
    带权重参数
    """

    def __init__(self, upper_remove=False, unique=True):
        self.quality_values = {}
        self.values = []
        self.best = None
        self.upper_remove = upper_remove
        self.unique = unique

    def load(self, src):
        if not src: return

        src = src.split(";")
        for i in src:
            val = i.split(",")
            w = 1
            if val[0].startswith("q="):
                w = float(val[0][2:])
                val = val[1:]

            if self.upper_remove: val = [i.lower() for i in val]

            if w in self.quality_values.keys():
                self.quality_values[w] += val
                if self.unique: self.quality_values[w] = list(set(self.quality_values[w]))
            else:
                self.quality_values[w] = val

            self.values += val
            if self.unique: self.values = list(set(self.values))

        if len(self.quality_values) > 0:
            val = sorted(self.quality_values.items(), key=lambda x: x[0], reverse=True)[0][1]
            if len(val) > 0:
                self.best = val[0]


class HttpHead:
    def __init__(self):
        self.data = {}

    def add(self, key, val):
        for i in self.data.keys():
            if i.upper() == key.upper():
                return self.data[i].append(val)
        self.data[key] = [val]

    def set(self, key, val):
        for i in self.data.keys():
            if i.upper() == key.upper():
                self.data[i] = val
                return
        self.data[key] = val

    def get(self, key, full=False):
        if full:
            for i in self.data.keys():
                if i.upper() == key.upper():
                    return self.data[i]
            return None
        else:
            for i in self.data.keys():
                if i.upper() == key.upper():
                    return self.data[i][0]
            return None


class HttpReqHead(HttpHead):
    def __init__(self, src=None):
        super(HttpReqHead, self).__init__()

        if src:
            if src[-4:] == "\r\n\r\n": src = src[:-4]
            src = src.replace("\r", "")
            first_line = src[:src.find("\n")]
            have_first_line = ": " not in first_line or (" " in first_line[:first_line.find(": ")])
            if have_first_line:
                self.add("METHOD", first_line.split(" ")[0])
                self.add("DIR", first_line.split(" ")[1])
                self.add("PROTOCOL", first_line.split(" ")[2])

            for i in src.split("\n")[1 if have_first_line else 0:]:
                if not i: continue
                if ": " in i:
                    k, v = i[:i.find(": ")], i[i.find(": ") + len(": "):]
                else:
                    k, v = i, ""
                self.add(k, v)

        self.load_parameters()

    def load_parameters(self):
        self.accept = self._load_quality_values("accept")
        self.accept_charset = self._load_quality_values("accept-charset")
        self.accept_encoding = self._load_quality_values("accept-encoding")
        self.accept_language = self._load_quality_values("accept-language")

        self.content_type = self._load_multi_parameter("Content-Type")

        self.authorization = self._load_str_values("authorization")
        self.connection = self._load_str_values("connection")
        self.cookie = self._load_str_values("cookie")
        self.upgrade = self._load_str_values("Upgrade")
        self.user_agent = self._load_str_values("User-Agent")
        self.referer = self._load_str_values("Referer")
        self.host = self._load_str_values("Host")

        self.dir = self._load_str_values("DIR")
        self.method = self._load_str_values("METHOD").upper()
        self.protocol = self._load_str_values("PROTOCOL").upper()

    def _load_quality_values(self, key):
        data = self.get(key, True)
        if data:
            res = QualityValues()
            for i in data:
                res.load(i)
            return res
        else:
            return QualityValues()

    def _load_multi_parameter(self, key):
        data = self.get(key, True)
        if data:
            res = MultiParameterVal()
            for i in data:
                res.load(i)
            return res
        else:
            return MultiParameterVal()

    def _load_str_values(self, key):
        data = self.get(key, True)
        if data:
            return str(data[0])
        else:
            return ""


class HttpRespHead(HttpHead):
    def __init__(self):
        super(HttpRespHead, self).__init__()
        self.resp_code = 200
        self.resp_msg = "OK"

    def dump(self):
        res = ""
        first_line = "HTTP/1.1 %s %s" % (self.resp_code, self.resp_msg)
        if first_line:
            res += first_line + "\r\n"

        for k, v in self.data.items():
            if k.upper() in ("FIRST-LINE", "METHOD", "DIR", "PROTOCOL"): continue
            for i in v:
                res += "%s: %s" % (k, i) + "\r\n"

        return res
