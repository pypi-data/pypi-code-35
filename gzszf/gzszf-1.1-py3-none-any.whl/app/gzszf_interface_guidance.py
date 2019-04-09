# -*- coding: utf-8 -*- 
# @Time : 2019/4/4 15:43 
# @Author : Allen 
# @Site :  同步办事指南
from gzszf.config import guidance_jar_path
from gzszf.get_JVM import JRun
from gzszf.models.model_service import ModelService
from bs4 import BeautifulSoup
from gzszf.config import is_bool
import datetime
from gzszf.logger.logger import Log


def get_guidance(nCataId, nStart, nEnd, guidance, logger, strStartCTime='', strEndCTime=''):
    url = r'http://www.gzegn.gov.cn/jcms/services/WSReceive?wsdl'
    data = {
        'nCataId': nCataId,
        "bRef": 0,
        "iBase64": 0,
        "nStart": nStart,
        "nEnd": nEnd,
        "bAsc": 1,
        "strStartCTime": strStartCTime,
        "strEndCTime": strEndCTime,
        'strKey': '',
        'strLoginId': '85ea7933c2e0fe1c5d8064c71d8874e5f3b70784065fead07d3d28c6710d781cbfd9a123e4e131a132e8c4a7ee62c7620d2790ad62240773221b18c60754a1fa07b4fb3b83aef8d3c248152cf781c7ff113cfd1988f7d0440e8c96d009443c7df2e3b6df1829ad44fdd2cd16feae740ba23188743e2635ba0349b4ac0363dd49',
        'strPwd': '844db9b32ca83dfa44bcd6db9f9d367b4948f74238a5393dd97398890aa50a5015592c985964009588defd76ed9b5a262501de208537cc7454a7f2b35756d6266c52b038eb59042ac715c74ca32f2e774da7358ed2d3160c1e09328f59b265d0f917b3896646ca8e38ceedd23b14b30ccf18c939dc2870125e257550eebfe9b5',
    }
    logger.info("-" * 25)
    logger.info("请求参数：{}".format(str(data)))
    data = guidance.search(url, data['nCataId'], data['nStart'], data['nEnd'], data['strStartCTime'],
                           data['strEndCTime'],
                           data['strLoginId'], data['strPwd'], data['strKey'])
    logger.info("-" * 25)
    logger.info("\n")
    return data


def parser_guidance(g_data, logger):
    obj = BeautifulSoup(g_data, 'xml')
    data_list = []
    logger.info("-" * 25)
    logger.info("解析数据：\n")
    for field in obj.find_all('article'):
        data_dict = {}
        data_dict['title'] = field.find(id='vc_name').text
        data_dict['url'] = field.find('arturl').text
        data_dict['create_time'] = field.find(id="c_createtime").text
        data_dict['area_id'] = field.find(id='field_280')['dbfieldtype']
        data_dict['dept'] = field.find(id='field_2181').text
        data_dict['cat'] = field.find(id='field_2544').text
        data_list.append(data_dict)
        logger.info(str(data_dict))
    logger.info("解析数据完成\n")
    logger.info("-" * 25)
    logger.info("\n")
    return data_list


def multiprocessing_guidance(nCataId, nStart, nEnd, strStartCTime, strEndCTime, models, guidance, logger):
    try:
        g_data = get_guidance(nCataId, nStart, nEnd, guidance, logger, strStartCTime, strEndCTime)  # 通过接口请求数据
        data_list = parser_guidance(g_data, logger)  # 处理数据
        if data_list:
            logger.info("-" * 25)
            logger.info("插入数据库：\n")
            msg = models.insert_gzszf_data_guidance(data_list)
            logger.info("插入数据 {} 完成\n".format(msg))
            logger.info("-" * 25)
            logger.info("\n")
    except Exception as e:
        print(e)
        logger.info("*" * 25)
        logger.error("错误原因：{}，错误参数：{}-{}-{}-{}-{}".format(e, nCataId, nStart, nEnd, strStartCTime, strEndCTime))
        logger.info("*" * 25)


def get_timeStamp():
    if is_bool:
        from gzszf.config import strEndCTime, strStartCTime
        return strStartCTime, strEndCTime
    else:
        return str(datetime.date.today()), str(datetime.date.today())


def get_logger():
    # 日志模块
    logger = Log().get_logger()
    # 打印时间
    logger.info('*' * 25)
    logger.info("Star:" + datetime.datetime.now().strftime("%Y-%m-%d"))
    logger.info('*' * 25)
    return logger


def init_jvm():
    # 初始化jvm
    jRun = JRun()
    jRun.startJVM(guidance_jar_path)
    Guidance = jRun.get_jclass('Guidance')
    guidance = Guidance()
    return jRun, guidance


def run_guidance():
    '''

    283 行政处罚 291 行政裁决  290 公共服务 287 行政检查 286 行政给付 289 行政奖励 284 行政确认 292 其他行政权力 285 行政强制 282 行政许可 288 行政征收
    :return:
    '''
    # 获取时间
    _strStartCTime, _strEndCTime = get_timeStamp()
    # 获取logger
    logger = get_logger()

    nCataId_list = [283, 291, 290, 287, 286, 289, 284, 292, 285, 282, 288]
    # 初始化jvm
    jRun, guidance = init_jvm()

    # 初始化数据库
    models = ModelService()

    [multiprocessing_guidance(nCataId, nStart=1, nEnd=15, strStartCTime=_strStartCTime, strEndCTime=_strEndCTime,
                              models=models, guidance=guidance, logger=logger)
     for nCataId in nCataId_list]

    # 关闭jvm
    jRun.shutdownJVM()
    # 关闭数据库
    models.close_session()


if __name__ == '__main__':
    run_guidance()
