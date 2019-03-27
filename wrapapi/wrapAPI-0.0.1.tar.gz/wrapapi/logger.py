
import logging


log = logging.getLogger('testing')


def request_logging(request, *args, **kwargs):
    log.info(
        f"Request:\n"
        f"\t{request.request.method.upper()}: {request.url}\n"
        f"\theaders: {request.request.headers}\n"
        f"\tbody: {request.request.body}\n"
    )
    # TODO change it require by settings
    log.warning(
        f"Response:\n"
        f"\tstatus code: {request.status_code}\n"
        f"\tcontent: {request.content}\n"
        f"\theaders: {request.headers}\n"
    )
