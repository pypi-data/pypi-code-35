import asyncio
import concurrent.futures
import logging
from typing import Optional, Union

from .objects import ServiceStatus, ServiceStatusList
from .utils import http_get, http_request

logger = logging.getLogger(__name__)


def healthcheck(url: str, timeout: Union[float, int],
                find_data: Optional[str] = None) -> ServiceStatus:
    """Check if a URL is alive or not.

    Optionally, it checks for a string existing in the body. The OK attribute
    of the result is True if the request is OK and the string is found or False
    otherwise.

    Considers the timeout and warn if request takes longer than 60% of the time.

    Returns a ServiceStatus object with the requested URL, its status and
    checks results.
    """
    logger.info('Begin checking URL %s...', url)
    body, request_time, error = http_get(url, timeout=timeout)
    if error and request_time > timeout:
        logger.warning('Request to %s timed out taking %.2f seconds', url,
                       request_time)
    elif request_time > (0.6 * timeout):
        logger.warning('Request to %s took too long: %.2f seconds', url,
                       request_time)
    alive = not error
    ok = body.find(find_data) != -1 if find_data and alive else alive
    result = ServiceStatus(url, alive, ok)
    if alive and ok:
        status = 'alive and OK'
    elif alive:
        status = 'alive but not OK'
    else:
        status = 'dead'
    logger.info('Finish checking URL %s: %s', url, status)
    return result


async def check_urls(urls: list, timeout,
                     validations: Optional[list]) -> ServiceStatusList:
    """Asynchronously check given URLs status, optionally validating them."""
    statuses = ServiceStatusList()
    with concurrent.futures.ThreadPoolExecutor(max_workers=32) as executor:
        loop = asyncio.get_event_loop()
        futures = []
        for index, url in enumerate(urls):
            if validations:
                try:
                    validation = validations[index]
                except IndexError:
                    validation = validations[-1]
            else:
                validation = None
            futures.append(
                loop.run_in_executor(
                    executor,
                    healthcheck,
                    url,
                    timeout,
                    validation
                )
            )
        for result in await asyncio.gather(*futures):
            statuses.append(result)
    return statuses


def notify(url: str, payload: Optional[str] = None,
           headers: Optional[dict] = None) -> bool:
    """Execute a POST request as a notification with optional data."""
    response, _, error = http_request('POST', url, timeout=5, data=payload,
                                      headers=headers)
    return not error and response.ok
