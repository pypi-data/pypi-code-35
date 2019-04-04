# -*- coding: utf-8 -*-
import os
import bgionline
import sys
import time
import json
import oss2
import fnmatch
import requests
from bgionline.utils import calculate_file_crc64, parse_size, parse_time, OSTYPE, progress as progres, to_zhcn, \
    init_queue, get_sts_token
from config import UPLOAD_THREADS_NUM, PART_SIZE, MULTIPART_THRESHOLD

# import boto3
# from filechunkio import FileChunkIO
# import threading

MULTIPROCESSING_CONSUMED = 0
LAST_PERCENT = -1
ERR_FILE = []
SUCCEED_FILE = []
WRITER = ''
FILE_NAME = ''

import logging

custom_logger = logging.getLogger('oss2')
oss2.defaults.logger = custom_logger

custom_logger.addHandler(logging.StreamHandler(sys.stdout))
custom_logger.setLevel(logging.WARNING)

if OSTYPE != "windows":
    from bgionline.utils import Writer


    def linux_mac_progress(consumed, total):
        """
        oss 进度回调
        :param consumed: 已下载大小
        :param total: 总大小
        :return:
        """
        global LAST_PERCENT
        global WRITER
        global FILE_NAME
        percent = round(consumed * 1.0 / total * 100, 2)
        # if percent - LAST_PERCENT > 0:
        WRITER.write("[%s%s]    %s    %s\r" % (
            '=' * int(percent / 2), (' ' * (50 - int(percent / 2))), '%4.1f' % (percent) + ' %', FILE_NAME,))
        LAST_PERCENT = percent


def progress(consumed, total):
    """
    oss 进度回调
    :param consumed: 已下载大小
    :param total: 总大小
    :return:
    """
    global MULTIPROCESSING_CONSUMED
    global LAST_PERCENT
    MULTIPROCESSING_CONSUMED.value += (consumed - LAST_PERCENT)
    LAST_PERCENT = consumed


def show_progress(consumed, total, total_files, err_file, succeed_file, list_pid, queue):
    """
    多进程进度条
    :param consumed: 已经下载的大小
    :param total: 需要下载文件的大小
    :param total_files: 需要下载的文件格式
    :param err_file: 下载中出错的文件数
    :param succeed_file: 下载中成功的文件数
    :param list_pid: 多进程的pid列表
    :param queue: 多进程的任务队列
    :return:
    """
    global MULTIPROCESSING_CONSUMED
    MULTIPROCESSING_CONSUMED = consumed
    global LAST_PERCENT

    try:
        while True:
            percent = round(MULTIPROCESSING_CONSUMED.value * 1.0 / total * 100, 2)
            velocity = MULTIPROCESSING_CONSUMED.value - LAST_PERCENT
            if velocity <= 0:
                velocity = 1
            consumed_file = err_file.__len__() + succeed_file.__len__()
            left_time = parse_time((total - MULTIPROCESSING_CONSUMED.value) / velocity)

            if consumed_file == total_files:
                sys.stdout.write("\r[%s%s]\t%s/s\t%s\t[%s/%s]" % (
                    '=' * 50, (' ' * 0), parse_size(0), parse_time(0), consumed_file, total_files))
            else:
                sys.stdout.write("\r[%s%s]\t%s/s\t%s\t[%s/%s]" % (
                    '=' * int(percent / 2), (' ' * (50 - int(percent / 2))), parse_size(velocity), left_time,
                    consumed_file,
                    total_files))
            sys.stdout.flush()
            LAST_PERCENT = MULTIPROCESSING_CONSUMED.value
            time.sleep(1)
    except KeyboardInterrupt:
        for i in list_pid:
            os.kill(i, 9)

        # 退出前清楚队列
        while not queue.empty():
            queue.get()
            queue.task_done()

        os.kill(os.getpid(), 9)


def download_dir(download_record_dict, download_record_f, lock, q, project_id, path_id, download_type,
                 download_size_list, download_name_list, local_path=os.sep):
    """
    :param download_record_dict: 断点续传信息记录字典
    :param download_record_f: 断点续传信息存放文件夹
    :param lock: 锁
    :param q: 队列
    :param project_id:项目id
    :param download_type: 过滤的下载联系
    :param download_size_list: 记录下文件大小
    :param download_name_list: 记录下文件名字
    :param local_path: 存放的本地路径
    :return:
    """
    while True:
        try:
            res = bgionline.api.file_list(project_id, input_params={"filePath": path_id, "deep": 0})
            for i in res['result']:
                if int(i.get('isFolder', -1)) == 1:
                    download_dir(download_record_dict, download_record_f, lock, q, project_id, i["filePath"]+i['name']+"/", download_type,
                                 download_size_list, download_name_list, os.path.join(local_path, i.get('name')))
                if int(i.get('isFolder', -1)) == 0 and int(i.get('status', -1)) == 2 and 3 != int(
                        i.get('tier', -1)):
                    if download_type is None or ((i.get('name') and fnmatch.fnmatch(i.get('name'), download_type))):
                        download_size_list.append(int(i.get('size')))

                        download_name_list.append(os.path.join((to_zhcn(local_path)).encode('utf-8'),
                                                               (to_zhcn(i.get('name'))).encode('utf-8')))
                        i['local_path'] = local_path
                        if q is None:
                            print (to_zhcn('downloading  ' + i.get('name')) + '...').encode('utf-8')
                            download_file(download_record_dict, download_record_f, lock, i, show_progres=progres)
                            print ' '
                        else:
                            q.put(i)
        except Exception as e:
            raise e
        else:
            break


def download_file_consumer(q, download_record_dict, download_record_f, lock, consumed, err_file, succeed_file, writer,
                           show_progres=None):
    """
    多进程下载下载的消费函数
    :param q: 任务队列
    :param download_record_dict: 已经下载的任务记录
    :param download_record_f: 任务记录文件
    :param lock: 多进程锁
    :param consumed: 已经下载的大小
    :param err_file: 下载出错的文件
    :param succeed_file: 下载成功的文件
    :return:
    """
    global MULTIPROCESSING_CONSUMED
    MULTIPROCESSING_CONSUMED = consumed
    global ERR_FILE
    ERR_FILE = err_file
    global SUCCEED_FILE
    SUCCEED_FILE = succeed_file

    if OSTYPE != "windows":
        global WRITER
        WRITER = Writer(writer)
        show_progres = linux_mac_progress

    while True:
        data = q.get()
        try:
            if OSTYPE != "windows":
                WRITER.write('%s\r' + ' ' * (120 + len(FILE_NAME)))
            download_fail = 1
            download_file(download_record_dict, download_record_f, lock, data, show_progres=show_progres,
                          is_concurrent=True)
            download_fail = 0
        except KeyboardInterrupt:
            # 退出前清楚队列
            while not q.empty():
                q.get()
                q.task_done()
            break
        finally:
            if OSTYPE != "windows":
                WRITER.write('\n')
            q.task_done()
            if download_fail:
                ERR_FILE.append(os.path.join(data['local_path'], data['name']))


def download_file(download_record_dict, download_record_f, lock, file_info, show_progres=None, is_concurrent=False):
    """
    下载单个文件
    :param download_record_dict: 已经下载的任务记录
    :param download_record_f: 任务记录文件
    :param lock: 多进程锁
    :param file_info: 需要下载文件的信息
    :param show_progres: 显示进度函数
    :return:
    """

    global ERR_FILE
    global FILE_NAME
    file_id = file_info['id']
    file_name = file_info['name']
    FILE_NAME = file_name
    dir_name = file_info['local_path']
    if OSTYPE == 'windows':
        dir_name = to_zhcn(dir_name)
    if not os.path.exists(dir_name):
        try:
            os.makedirs(dir_name)
        except OSError:
            pass
    real_name = os.path.join(dir_name, file_name)
    download_record_file_name = None
    sts_time = None

    if download_record_dict.has_key(file_id):
        if download_record_dict[file_id]['status'] == 2:
            if os.path.exists(download_record_dict[file_id]['real_name']):
                print("File %s already download, skip it." % real_name)
                global MULTIPROCESSING_CONSUMED
                global SUCCEED_FILE
                if hasattr(MULTIPROCESSING_CONSUMED, 'value'):
                    MULTIPROCESSING_CONSUMED.value += int(file_info['size'])
                SUCCEED_FILE.append(real_name)
                return
        download_record_file_name = download_record_dict[file_id]['real_name']

    if os.path.exists(real_name):
        count = 0
        tmp_name = real_name
        while os.path.exists(tmp_name):
            count += 1
            tmp_name = os.path.join(dir_name, str(count) + "_" + file_name)
        real_name = tmp_name

    # 判断是否是新建的下载任务，不是则记录
    if download_record_file_name:
        real_name = download_record_file_name
    else:
        if OSTYPE == 'windows':
            real_name = unicode(to_zhcn(real_name))
        download_record_dict[file_id] = {
            'real_name': (to_zhcn(real_name)).encode("utf-8"),
            'name': (to_zhcn(os.path.join(dir_name, file_name))).encode("utf-8"),
            'remote_name': os.path.join(file_info["filePath"], file_name),
            # 1上传中，2上传完成
            'status': 1
        }
        with lock:
            with open(download_record_f, 'w') as f:
                try:
                    json.dump(download_record_dict.copy(), f)
                except Exception as e:
                    pass
    try:
        # s3_download_file(real_name, file_id, is_concurrent)
        if bgionline.config.host.endswith("com") or bgionline.config.host == '54.158.150.183':
            res = s3_download_file(real_name, file_id, is_concurrent)
        else:
            res = oss_downlaod(file_id, real_name, dir_name, file_name, show_progres)

        SUCCEED_FILE.append(os.path.join(dir_name, file_name))
        download_record_dict[file_id] = {
            'real_name': (to_zhcn(real_name)).encode("utf-8"),
            'name': (to_zhcn(os.path.join(dir_name, file_name))).encode("utf-8"),
            'remote_real_name': os.path.join(file_info["filePath"], file_name),
            'status': 2,
            'crc64': res.get('crc64', None)
        }
        with lock:
            with open(download_record_f, 'w') as f:
                try:
                    json.dump(download_record_dict.copy(), f)
                except Exception as e:
                    pass
    except Exception as e:
        print e
        raise


START_TIME = time.time()
client = None


def oss_downlaod(file_id, real_name, dir_name, file_name, show_progres=None):
    global ERR_FILE
    try:
        download_info = bgionline.api.get_download_info(file_id)
    except Exception as e:
        raise e

    path = download_info['path']
    bucket_name = download_info['bucket_name']

    credentials = download_info['credentials']
    access_key_id = credentials['AccessKeyId']
    access_key_secret = credentials['AccessKeySecret']
    security_token = credentials['STS_Token']
    sts_time = time.time()

    auth = oss2.StsAuth(access_key_id, access_key_secret, security_token)
    bucket = oss2.Bucket(auth, bgionline.config.storage_host, bucket_name, enable_crc=False)

    retry = 0
    res = {}
    while retry < 5:
        if retry > 0:
            sys.stderr.write("retry %s times , %ss later\n" % (retry, retry * 10))
            time.sleep(retry * 10)
        try:
            while True:
                try:
                    oss2.resumable_download(bucket, path, real_name,
                                            multiget_threshold=MULTIPART_THRESHOLD,
                                            part_size=PART_SIZE,
                                            num_threads=UPLOAD_THREADS_NUM,
                                            progress_callback=show_progres or progress,
                                            store=oss2.ResumableStore(root=bgionline.config.default_config_dir))
                    result = bucket.head_object(path)
                    crc64 = result.headers['x-oss-hash-crc64ecma']
                    res['crc64'] = crc64
                    break
                except IOError as e:
                    if e.args[0] == 122:
                        print("Insufficient available size on target path")
                except Exception as e:
                    if hasattr(e, 'status') and e.status not in (-3, 403):
                        err = str(e)
                        if hasattr(e, 'id'):
                            err = e.id + ':   ' + err
                        print ('OSS_ERROR: %s' % err)
                    if time.time() - sts_time > 3000:
                        download_info = bgionline.api.get_download_info(file_id)

                        credentials = download_info['credentials']
                        access_key_id = credentials['AccessKeyId']
                        access_key_secret = credentials['AccessKeySecret']
                        security_token = credentials['STS_Token']
                        auth = oss2.StsAuth(access_key_id, access_key_secret, security_token)
                        bucket = oss2.Bucket(auth, bgionline.config.storage_host, bucket_name)
                        sts_time = time.time()
                    time.sleep(5)
            # print('\nDone.')



            # local_crc = calculate_file_crc64(real_name)
            #
            # if str(local_crc) != oss_crc64:
            #     sys.stdout.flush()
            #     print('The download file error: %s' % real_name)
            #     ERR_FILE.append(os.path.join(dir_name, file_name))
            break
        except Exception as e:
            print("Error: %s" % str(e))
            if retry == 4:
                ERR_FILE.append(os.path.join(dir_name, file_name))

        retry += 1
    return res

def s3_download_file(real_name, uuid, is_concurrent):
    global ERR_FILE
    try:
        download_link = bgionline.api.get_download_link(uuid)
        download_link = download_link['url']
    except Exception as e:
        raise e
    retry = 0
    res = {}

    def _get_download_link(uuid):
        try:
            ### 不应该每一次都更新
            download_link = bgionline.api.get_download_link(uuid)
            return download_link['url']
        except Exception as e:
            raise e

    def _get_or_create_record():

        def _create_record(record):
            with open(record, "w") as r:
                json.dump("{}", r)

        from hashlib import md5
        record_md5 = md5(real_name).hexdigest() + "-" + md5(uuid).hexdigest()
        try:
            os.makedirs(os.path.join(bgionline.config.user_config_dir, ".s3_download"))
        except:
            pass
        record = os.path.join(os.path.join(bgionline.config.user_config_dir, ".s3_download", record_md5))

        if os.path.exists(record):
            try:
                with open(record) as r:
                    return json.load(r)
            except:
                _del_record(record)
                _create_record(record)
                return {}
        else:
            _create_record(record)
            return {}

    def _write_record(info):
        from hashlib import md5
        record_md5 = md5(real_name).hexdigest() + "-" + md5(uuid).hexdigest()
        record = os.path.join(os.path.join(bgionline.config.user_config_dir, ".s3_download", record_md5))
        import fcntl
        with open(record, "rb+") as r:
            fcntl.flock(r.fileno(), fcntl.LOCK_EX)
            json.dump(info, r)

    def _del_record():
        from hashlib import md5
        record_md5 = md5(real_name).hexdigest() + "-" + md5(uuid).hexdigest()
        record = os.path.join(os.path.join(bgionline.config.user_config_dir, ".s3_download", record_md5))
        os.remove(record)

    def _split_file(chunk_size):
        part_number = 1
        index_list = [0] ## 初始化，第一个分片以 0 开始
        file_info = bgionline.api.get_file_info(input_params={"id": [uuid]})
        file_size = file_info[0]["size"]
        while file_size / chunk_size > 9999: ## 分片数量最大为10000
            chunk_size *= 3
        while chunk_size * part_number < file_size:
            index_list.append(chunk_size * part_number)
            part_number += 1
        return index_list, file_size

    def _create_download():
        record_info = _get_or_create_record()
        if record_info.has_key("temp_suffix"):
            return record_info["temp_suffix"]
        else:
            import random
            import string
            temp_suffix = "tmp-" + ''.join(random.choice(string.ascii_lowercase) for i in range(12))
            open(real_name + "-" + temp_suffix, "w").close()
            record_info["temp_suffix"] = temp_suffix
            _write_record(record_info.copy())
            return temp_suffix

    def _download_one_chunk(temp_file, part_number, start_index, chunk_size, record_info):
        download_link = _get_download_link(uuid)
        headers = {"Range": "bytes=%d-%d" % (start_index, start_index+chunk_size-1)}
        response = requests.get(download_link, stream=True, verify=False, headers=headers)
        with open(temp_file, "rb+") as f:
            f.seek(start_index)

            for data in response.iter_content(chunk_size=8*1024):
                f.write(data)
            #写入记录
            record_info["parts"].append({
                "part_number": part_number,
                "start": start_index,
                "chunk_size": chunk_size
            })
            _write_record(record_info)

    def _complete_download():
        record_info = _get_or_create_record()
        os.rename(real_name + "-" + record_info["temp_suffix"], real_name)
        _del_record()

    def _mutilple_download(index_list, chunk_size, file_size, max_thread=UPLOAD_THREADS_NUM):
        _create_download()
        from concurrent import futures
        open_file = {"num": 0}
        with futures.ThreadPoolExecutor(max_workers=max_thread) as pool:
            part_number = 1
            record = _get_or_create_record()
            temp_file = real_name + "-" + record["temp_suffix"]
            if record.has_key("parts"):
                finish_list = []
                for p in record["parts"]:
                    finish_list.append(p["part_number"])

            for part_start_number in index_list:
                if ( not record.has_key("parts")) or (not part_start_number in finish_list):
                    while (open_file["num"] > 1000):  # 文件最大打开数
                        time.sleep(0.01)
                    process = pool.submit(_download_one_chunk, temp_file, part_number, part_start_number,
                                          chunk_size, record)
                    process.arg = part_number * chunk_size
                    process.arg2 = open_file
                    process.arg3 = file_size
                    process.add_done_callback(_callback)
                    open_file["num"] += 1
                part_number += 1
        _complete_download()

    def _callback(fn):
        fn.arg2["num"] -= 1
        finish = fn.arg
        total = fn.arg3
        if finish > total:
            finish = total
        progres(finish, total)


    while retry < 5:
        if retry > 0:
            sys.stderr.write("retry %s times , %ss later\n" % (retry, retry * 10))
            time.sleep(retry * 10)
        try:
            chunk_size = PART_SIZE
            index_list, file_size = _split_file(chunk_size)
            _mutilple_download(index_list, chunk_size, file_size)
            break
        except Exception, e:
            print("s3_Error: %s" % str(e))
            if retry == 4:
                ERR_FILE.append(os.path.join(real_name))
        retry += 1
    return res
