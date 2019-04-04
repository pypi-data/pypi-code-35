# 一个例子，仅作参考
# TODO 注意log文件要写在服务器系文件系统中，部署前要修改路径
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': "%(asctime)s|%(message)s",
            'datefmt': "%Y-%m-%d %H:%M:%S"
        },
        'verbose': {
            # 'format': '%(levelname)s %(asctime)s %(module)s %(pathname)s %(lineno)d %(process)d %(thread)d %(message)s'
            'format': '%(levelname)s %(asctime)s %(message)s'
        },
        'syslog': {
            'format': "%(asctime)s [%(levelname)s] [%(process)d.%(threadName)s:%(thread)d] [%(module)s.%(funcName)s] -- %(message)s",
            'datefmt': "%Y-%m-%d %H:%M:%S"
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {  # 控制台
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            # 'filters': ['require_debug_true'],
            'formatter': 'syslog'
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            # 'filters': ['require_debug_false'], # 仅当 DEBUG = False 时才发送邮件
        },
    },
    'loggers': {
        'console': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
    }
}
