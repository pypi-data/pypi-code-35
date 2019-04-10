from SCLibrary.base import keyword
from robot.libraries.BuiltIn import BuiltIn
from argparse import Namespace
from locust import HttpLocust, TaskSet, task, runners, InterruptTaskSet
from robot.api import logger
import inspect

Locust_Task_Pool = []
Locust_User_Pool = []

class LocustKeyword(object):

    # ==========================================================
    # ========================== 便捷 ===========================
    # ==========================================================

    '''
    为传入的user添加一个断言的匿名函数
    '''
    def append_assert(self, user, func):
        if user.task.all_assets is None:
            user.task.all_assets = [func]
        else:
            user.task.all_assets.append(func)

    # ==========================================================
    # ========================== 断言 ===========================
    # ==========================================================

    @keyword("Locust HTTP Status Code Should Be")
    def status_code_should_be(self, user, code):
        '''
        断言HTTP完成之后响应状态码
        ``user`` HttpLocust对象
        ``code`` HTTP的响应状态码
        '''
        def core_status_code_should_be(task, response):
            if response.status_code != int(code):
                raise Exception(f"Locust响应状态码期望为{code}, 当前实际得到的状态码为{response.status_code}")
        self.append_assert(user, core_status_code_should_be)

    @keyword("Locust JSON Should Be")
    def locust_response_json_equal(self, user, keypath, value):
        '''
        该断言关键字主要用于对返回JSON内容的断言
        ``user`` HttpLocust对象
        ``Keypath`` 键路径，比如data.foo，对应的是data中的foo的内容
        ``value`` 期望的值
        '''
        def core_locust_response_json_equal(task, response):
            try:
                json = response.json()
                for key in keypath.split('.'):
                    json = json[key]
                if json != value:
                    raise Exception(f'期望从{keypath}中得到{value}, 但是实际上却得到了{json}')
            except KeyError:
                raise Exception(f'{response}不存在{keypath}')
        self.append_assert(user, core_locust_response_json_equal)

    @keyword("Locust Expect")
    def locust_core_expect(self, user, expection):
        '''
        自定义断言机制
        ``user`` HttpLocust类
        ``expection`` 一个关键字的名字，建议命名规则： 场景-期望
        讨论：
        expection是一个接受一个response参数的关键字，使用者可以拿到这个response进行自定义的断言。\n
        `response.json()`: 本次响应的JSON对象(Returns the json-encoded content of a response, if any)\n
        `response.content`: 本次响应的字节内容(Content of the response, in bytes)
        `response.headers`: 本次响应的响应投(Case-insensitive Dictionary of Response Headers. For example, headers['content-encoding'] will return the value of a 'Content-Encoding' response header)\n
        `response.encoding`: 本次响应的编码方式(Encoding to decode with when accessing r.text)\n
        `response.cookies`: 本次响应的cookies
        `response.status_code`: 本次响应的状态码
        `response.url`: 本次响应的请求地址
        '''
        self.append_assert(user, expection)

    @keyword("Locust AVE Threshold")
    def locust_ave_response_duration_should_less_than(self, user, time):
        '''
        平均阈值设置，超过阈值测试用例失败
        所有的响应中的平均响应时间不应该大于这个阈值
        ``user`` 模拟用户
        ``time`` 响应时间阈值(毫秒单位)
        '''
        def core_locust_response_duration_should_less_than(task, response):
            globalVaildator.rd_ave_threshold[task.path] = time
        self.append_assert(user, core_locust_response_duration_should_less_than)

    @keyword("Locust MAX Threshold")
    def locust_max_response_duration_should_less_than(self, user, time):
        '''
        最大阈值设置，超过阈值测试用例失败
        所有的响应中的最大响应时间不应该大于这个阈值
        ``user`` 模拟用户
        ``time`` 响应时间阈值(毫秒单位)
        '''
        def core_locust_response_duration_should_less_than(task, response):
            globalVaildator.rd_max_threshold[task.path] = time
        self.append_assert(user, core_locust_response_duration_should_less_than)

    @keyword("Locust MIN Threshold")
    def locust_min_response_duration_should_less_than(self, user, time):
        '''
        最小阈值设置，超过阈值测试用例失败
        所有的响应中的最小响应时间不应该大于这个阈值
        ``user`` 模拟用户
        ``time`` 响应时间阈值(毫秒单位)
        '''
        def core_locust_response_duration_should_less_than(task, response):
            globalVaildator.rd_min_threshold[task.path] = time
        self.append_assert(user, core_locust_response_duration_should_less_than)

    # ==========================================================
    # ========================== 任务 ===========================
    # ==========================================================

    @keyword("Locust GET Task")
    def build_locust_get_task(self, path='/', header=None):
        '''
        创建一个`GET`压测任务
        ``path`` 请求路径
        ``header`` 请求头
        返回一个包含该任务的HttpLocust
        '''
        return LocustWorker.build_locust_core_task('GET', path=path)

    @keyword("Locust POST Task")
    def build_locust_post_task(self, path='/', header=None, body=None):
        '''
        创建一个`POST`任务
        ``path`` 请求路径
        ``header`` 请求头
        ``body`` 请求体
        返回一个包含该任务的HttpLocust
        '''
        return LocustWorker.build_locust_core_task('POST', path=path, header=header, body=body)

    @keyword("Locust PUT Task")
    def build_locust_put_task(self, path='/', header=None, body=None):
        '''
        创建一个`PUT`任务
        ``path`` 请求路径
        ``header`` 请求头
        ``body`` 请求体
        返回一个包含该任务的HttpLocust
        '''
        return LocustWorker.build_locust_core_task('PUT', path=path, header=header, body=body)

    @keyword("Locust DELETE Task")
    def build_locust_delete_task(self, path='/', header=None):
        '''
        创建一个`DELETE`任务
        ``path`` 请求路径
        ``header`` 请求头
        返回一个包含该任务的HttpLocust
        '''
        return LocustWorker.build_locust_core_task("DELETE",path=path, header=header)

    # ==========================================================
    # ========================== 执行 ===========================
    # ==========================================================

    @keyword("Locust Run")
    def run_locust(self, task, host, num_clients=1, hatch_rate=10):
        '''
        开始执行所输入的压测任务
        ``task`` 任务类型的数组
        ``host`` 测试接口的域名
        ``num_clients`` 模拟的用户数量， 默认为1
        ``hatch_rate`` 请求发起的速率，默认为10
        '''
        num_requests = int(num_clients) * int(hatch_rate)
        LocustWorker.run(task=task, host=host, num_requests=num_clients, num_clients=num_clients, hatch_rate=hatch_rate)


class LocustWorker(object):
    '''
    创建`locust`HTTP任务的核心方法
    `method` 请求方法
    `path` 请求路径
    `header` 请求头
    `body` 请求体
    '''
    @staticmethod
    def build_locust_core_task(method, path='/', header=None, body=None):
        task_name = fetch_task_name()
        user_name = fetch_user_name()
        base_task = None
        if method == 'GET':
            base_task = LocustGetTask
        elif method == 'POST':
            base_task = LocustPostTask
        elif method == 'PUT':
            base_task = LocustPutTask
        elif method == 'DELETE':
            base_task = LocustDeleteTask
        else:
            AssertionError("不支持%s的请求方式" % method)
        task_cls = type(task_name, (base_task,), {'path': path, 'header': header, 'body': body})
        locust_excutor = type(user_name, (HttpLocust,), {'task_set': task_cls, 'max_wait': 2000, 'stop_timeout': 7000})
        locust_excutor.task = task_cls
        Locust_Task_Pool.append(locust_excutor)
        return locust_excutor

    '''
    开始运行压测任务
    `host` 域名
    `num_requests` 总共发起的请求数
    `num_clients` 模拟用户数
    `hatch_rate` 请求频率
    '''
    @staticmethod
    def run(task, host, num_requests=10, num_clients=1, hatch_rate=10):
        logger.info(f'num_requests: {num_requests} num_clients: {num_clients} hatch_rate: {hatch_rate}')
        if task is None:
            all_task = Locust_Task_Pool
        elif inspect.isclass(task) and issubclass(task, HttpLocust):
            all_task = [task]
        else:
            all_task = task
        options = Namespace()
        options.host = host
        options.num_clients = int(num_clients)
        options.hatch_rate = int(hatch_rate)
        options.num_requests = int(num_requests)
        runners.locust_runner = runners.LocalLocustRunner(all_task, options)
        runners.locust_runner.start_hatching(wait=True)
        runners.locust_runner.greenlet.join()
        globalVaildator.host = host
        for name, value in runners.locust_runner.stats.entries.items():
            globalVaildator.vaildate(name[0], value)
            max_response_time = "N/A"
            min_response_time = "N/A"
            median_response_time = "N/A"
            total_rps = "N/A"
            if value.min_response_time:
                min_response_time = value.min_response_time
            if value.median_response_time:
                median_response_time = value.median_response_time
            if value.max_response_time:
                max_response_time = value.max_response_time
            if value.total_rps:
                total_rps = int(value.total_rps)
            logger.info(f"[压测报告]==> 接口:{name[0]} 请求方式:{name[1]} 最快响应时间:{min_response_time} ms 平均响应时间:{median_response_time} ms 最慢响应时间:{max_response_time} ms 每秒请求数:{total_rps}")
        for error in runners.locust_runner.errors.values():
            raise AssertionError(error.error)
        Locust_Task_Pool.clear()
        Locust_User_Pool.clear()

'''
从`task`命名池中获取一个`task name`
'''
def fetch_task_name():
    return '__rf_locust_task' + str(len(Locust_Task_Pool))

'''
从`user`命名池获取一个`user name`
'''
def fetch_user_name():
    name = '__rf_locust_user' + str(len(Locust_User_Pool))
    Locust_User_Pool.append(name)
    return name

class LocustVaildator(object):
    # 最快响应阈值，毫秒级别
    rd_min_threshold = {}
    # 平均响应阈值，毫秒级别
    rd_ave_threshold = {}
    # 最慢响应阈值，毫秒级别
    rd_max_threshold = {}
    host = None
    # 核心验证行为
    def vaildate(self, url, result):
        if not result: return
        try:
            if self.rd_min_threshold[url]:
                assert int(self.rd_min_threshold[url]) >= int(result.min_response_time), f'接口: {self.host}{url} ===> 最快响应不大于{self.rd_min_threshold[url]}毫秒'
        except KeyError:
            pass
        try:
            if self.rd_ave_threshold[url]:
                assert int(self.rd_ave_threshold[url]) >= int(result.median_response_time), f'接口: {self.host}{url} ===> 平均响应时间不能大于{self.rd_ave_threshold[url]}毫秒'
        except KeyError:
            pass
        try:
            if self.rd_max_threshold[url]:
                assert int(self.rd_max_threshold[url]) >= int(result.max_response_time), f'接口: {self.host}{url} ===> 最大响应时间不能大于{self.rd_max_threshold[url]}毫秒'
        except KeyError:
            pass

globalVaildator = LocustVaildator()

class RobotBaseTask(TaskSet):
    path = None
    header = None
    body = None
    all_assets = []
    '''
    统一处理 Response
    '''
    def handle_response(self, response):
        try:
            for asset in self.all_assets:
                if callable(asset):
                    asset(self, response)
                else:
                    BuiltIn().run_keyword(asset, response)
        except Exception as e:
            response.failure(e)
            self.interrupt()
            return
        response.success()
            

class LocustGetTask(RobotBaseTask):
    @task(1)
    def get(self):
        if not self.path:
            raise AssertionError("请求的Path为必传参数!")
        if len(self.all_assets) > 0:
            with self.client.get(self.path, headers=self.header, catch_response=True) as response:
                self.handle_response(response)
        else:
            self.client.get(self.path, headers=self.header)

class LocustPostTask(RobotBaseTask):
    @task(1)
    def post(self):
        if not self.path:
            raise AssertionError("请求的Path为必传参数!")
        if len(self.all_assets) > 0:
            with self.client.post(self.path, self.body, headers=self.header, catch_response=True) as response:
                self.handle_response(response)
        else:
            self.client.post(self.path, self.body, headers=self.header)

class LocustPutTask(RobotBaseTask):
    @task(1)
    def put(self):
        if not self.path:
            raise AssertionError("请求的Path为必传参数!")
        if len(self.all_assets) > 0:
            with self.client.put(self.path, self.body, headers=self.header, catch_response=True) as response:
                self.handle_response(response)
        else:
            self.client.put(self.path, self.body, headers=self.header)

class LocustDeleteTask(RobotBaseTask):
    @task(1)
    def delete(self):
        if not self.path:
            raise AssertionError("请求的Path为必传参数!")
        if len(self.all_assets) > 0:
            with self.client.delete(self.path, headers=self.header, catch_response=True) as response:
                self.handle_response(response)
        else:
            self.client.delete(self.path, headers=self.header)