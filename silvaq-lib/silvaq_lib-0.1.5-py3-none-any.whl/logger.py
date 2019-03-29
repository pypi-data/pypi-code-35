#!/usr/bin/python3
# _*_ coding:utf-8 _*_
import datetime, signal, os
from collections import OrderedDict

OTHER_EXIT_HANLDLE = []


def exit_hanle(signum, frame):
    for file_handle in Logger.LOG_HANDLE:
        ret_list = list(file_handle.items())
        for key, coro in ret_list:
            coro.close()
            del file_handle[key]

    for handle in OTHER_EXIT_HANLDLE:
        handle(signum, frame)
    # sys.exit()


class Logger():
    LOG_HANDLE = []
    '''
    - 备注，如果处理纯文本，不需要实时写入时文件句柄开启缓冲时提高性能降低写入开销的很好的处理方式
    - 注意 kill -9 退出程序会丢数据
    file_prefix, file_suffix 文件名前后缀，如果前缀存在，那么后缀一定存在
    如果不存在文件前缀，以 timestamp 为文件名
    - 实例:
    #log_obj = Logger('log', 'surfing', 'log')
    # log_obj.distribute_msg(msg="hello world")
    # # log_obj.distribute_msg('20171017', 'this is a pen!-----1\n')
    # log_obj.log('this is a pen!-----2\n')
    # time.sleep(30)
    # # LOG_OBJ.distribute_msg('20171018', 'this is a pen!-----1\n')
    # # LOG_OBJ.distribute_msg('20171019', 'this is a pen!-----1\n')
    # # time.sleep(30)
    '''

    def __init__(self, file_path, file_prefix, file_suffix, size=2):
        """

        :param file_path: 日志文件存放目录
        :param file_prefix: 日志文件名前缀
        :param file_suffix: 日志文件名后缀
        :param size:        文件句柄容器容量
        """
        # signal.signal(signal.SIGINT, exit_hanle)
        # signal.signal(signal.SIGTERM, exit_hanle)
        # signal.signal(signal.SIGKILL, exit_hanle)
        self.file_path = file_path
        self.file_prefix = file_prefix
        self.file_suffix = file_suffix
        self.dict_max = size
        self.file_handle = OrderedDict()
        Logger.LOG_HANDLE.append(self.file_handle)

    # def set_exit_handle(self, handle_name):
    #     global OTHER_EXIT_HANLDLE
    #     OTHER_EXIT_HANLDLE.append(handle_name)

    def set_exit_event(self):
        # du_log 退出处理 只有此类需要做 kill 捕获时候调用这个
        signal.signal(signal.SIGINT, self.Logger_exit_event)
        signal.signal(signal.SIGTERM, self.Logger_exit_event)

    def Logger_exit_event(self, signum, frame):
        self.Logger_exit()

    def Logger_exit(self):
        # 其他程序调用
        for file_handle in Logger.LOG_HANDLE:
            ret_list = list(file_handle.items())
            for key, coro in ret_list:
                coro.close()
                del file_handle[key]

    def write_log_coro(self, time_stamp):
        if self.file_prefix:
            file = '{}.{}.{}'.format(self.file_prefix, time_stamp, self.file_suffix)
        else:
            file = time_stamp

        abs_file = os.path.join(self.file_path, file)
        cur_path = os.path.dirname(abs_file)
        if not os.path.exists(cur_path):
            os.makedirs(cur_path)
        with open(abs_file, 'a', encoding='utf-8') as f:
            while True:
                content = yield
                if not content:
                    f.flush()
                    continue

                f.write(content)

    def create_file_hanle(self, time_stamp):
        coroutine = self.write_log_coro(time_stamp)
        coroutine.send(None)
        self.file_handle[time_stamp] = coroutine

        if len(self.file_handle) > 1:
            before_handle = list(self.file_handle.values())[-2]
            before_handle.send(None)

        if len(self.file_handle) > self.dict_max:
            first_key = list(self.file_handle.keys())[0]
            self.file_handle[first_key].close()
            del self.file_handle[first_key]

        return coroutine

    def distribute_msg(self, time_stamp, msg):
        # time_stamp 2017101010
        file_hanle = self.file_handle.get(time_stamp, None)

        if not file_hanle:
            file_hanle = self.create_file_hanle(time_stamp)

        try:
            file_hanle.send(msg)
        except Exception as e:
            del self.file_handle[time_stamp]
            raise e

    def log(self, message, timestamp=False, time_fmt='%Y%m%d'):
        this_time = datetime.datetime.now()
        time_stamp = this_time.strftime(time_fmt)

        if timestamp:
            log_time_stamp = this_time.strftime('%H:%M:%S')
            log_content = '{}\t{}\n'.format(log_time_stamp, message)
        else:
            log_content = '{}\n'.format(message)

        self.distribute_msg(time_stamp, log_content)
        # self.log_commit()

    def commit(self):
        self.log_commit()

    def log_commit(self):
        for file_handle in Logger.LOG_HANDLE:
            for key, coro in file_handle.items():
                coro.send(None)
