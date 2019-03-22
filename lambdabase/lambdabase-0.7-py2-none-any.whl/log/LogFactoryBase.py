from lambdabase.RequestContext import RequestContext
from lambdabase.log.LogMessage import LogMessage


def inject_context(func):
    """
    Inject request context data into log message
    """
    def wrapper(*func_args, **func_kwargs):
        obj = func_args[0]
        context = obj.context
        log_message = func(*func_args, **func_kwargs)

        if context is not None:
            log_message.add("request_id", context.request_id)
            log_message.add("correlation_id", context.correlation_id)
            log_message.add("user_id", context.user_id)

        return log_message

    return wrapper


class LogFactoryBase(object):

    context = RequestContext

    @classmethod
    def base_000(cls):
        log = LogMessage('BASE-000')
        log.message = 'Initialising base services'
        return log

    @classmethod
    @inject_context
    def base_001(cls):
        log = LogMessage('BASE-001')
        log.message = 'Entering pre-execute for new request'
        return log

    @classmethod
    @inject_context
    def base_002(cls, event_type):
        log = LogMessage('BASE-002')
        log.message = 'Incoming event type detected as [{}]'.format(event_type)
        log.add('event_type', event_type)
        return log

    @classmethod
    def base_003(cls, event_type):
        log = LogMessage('BASE-003')
        log.message = 'Registering event type [{}]'.format(event_type)
        log.add('event_type', event_type)
        return log

    @classmethod
    @inject_context
    def base_004(cls, response):
        log = LogMessage('BASE-004')
        log.message = 'Completed handling request. Response is of type [{}]'.format(response)
        return log

    @classmethod
    @inject_context
    def base_005(cls, exception):
        log = LogMessage('BASE-005')
        log.message = 'Error handling request [{}]'.format(exception.message)
        return log

    @classmethod
    def base_006(cls):
        log = LogMessage('BASE-006')
        log.message = 'Starting module bootstrap'
        return log

    @classmethod
    def base_007(cls, service_type):
        log = LogMessage('BASE-007')
        log.message = 'Requesting service of type [{}]'.format(service_type.__module__)
        log.add('service_type', service_type)
        return log

    @classmethod
    def base_008(cls, service, service_type):
        log = LogMessage('BASE-008')
        log.message = 'Returning service of type [{}] for request of type [{}]'\
            .format(service.__module__, service_type.__module__)
        log.add('requested_type', service_type)
        log.add('returned_type', service)
        return log

    @classmethod
    def base_009(cls, service_type):
        log = LogMessage('BASE-009')
        log.message = 'Registering service of type [{}]'.format(service_type)
        log.add('service_type', service_type)
        return log

