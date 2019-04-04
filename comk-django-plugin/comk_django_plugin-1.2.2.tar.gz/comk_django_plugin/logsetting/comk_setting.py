# from django.conf import settings
#
# BASE_DIR = settings.BASE_DIR
import datetime

from django.conf import settings

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'comk_verbose': {
            # 'format': '%(levelname)s %(asctime)s %(module)s %(pathname)s %(lineno)d %(process)d %(thread)d %(message)s'
            'format': '%(levelname)s %(asctime)s %(message)s'
        },
    },
    'handlers': {
        'comk_request_log': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': settings.BASE_DIR + '/log/comk_request_' + datetime.datetime.now().strftime("%Y%m%d") + '.log',
            # 'filename': './log/comk_request.log',
            'maxBytes': 1024 * 1024 * 100,  # 100M
            'backupCount': 2,
            'formatter': 'comk_verbose',
            'encoding': 'utf-8',
        },
        'comk_exception_log': {
            'level': 'DEBUG',  # 打印DEBUG （或更高）级别的消息。
            'class': 'logging.handlers.RotatingFileHandler',  # 它的主体程序是RotatingFileHandler类，这是最重要的。
            'filename': settings.BASE_DIR + '/log/comk_error_traceback_' + datetime.datetime.now().strftime(
                "%Y%m%d") + '.log',
            # 'filename': "./log/comk_error_traceback.log",
            'maxBytes': 1024 * 1024 * 100,  # 每个日志文件大小
            'backupCount': 2,
            'formatter': 'comk_verbose',  # 采用verbose为格式化器。
            'encoding': 'utf-8',  # 设定编码，如不设定，则编码为ascii，无法写入中文
        },
    },
    'loggers': {
        'comk_request_log': {
            'handlers': ['comk_request_log'],
            'level': 'INFO',
            'propagate': True,
        },
        'comk_exception_log': {
            'handlers': ['comk_exception_log'],
            'level': 'ERROR',
        },
    }
}
