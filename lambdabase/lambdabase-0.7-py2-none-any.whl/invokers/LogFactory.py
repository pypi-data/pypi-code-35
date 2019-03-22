from lambdabase.log.LogFactoryBase import LogFactoryBase, inject_context
from lambdabase.log.LogMessage import LogMessage
import simplejson as json


class LogFactory(LogFactoryBase):
    @classmethod
    @inject_context
    def invoker_000(cls, function_name, data):
        log = LogMessage('INVOKER-000')
        log.message = 'Invoking remote service function [{}] with the following data [{}]'\
            .format(function_name, json.dumps(data))
        log.add('remote_function', function_name)
        return log

    @classmethod
    @inject_context
    def invoker_001(cls, function_name, data):
        log = LogMessage('INVOKER-001')
        log.message = 'Remote service [{}] responded with the following data [{}]' \
            .format(function_name, data)
        log.add('remote_function', function_name)
        return log

    @classmethod
    @inject_context
    def invoker_002(cls, function_name, exception):
        log = LogMessage('INVOKER-002')
        log.message = 'Invoking remote service failed for function [{}]'.format(function_name)
        log.add('remote_function', function_name)
        log.add('error_message', exception.message)
        return log
