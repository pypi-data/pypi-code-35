__version__ = '1.0.1'
__all__ = ['Revolt']

from concurrent.futures import ThreadPoolExecutor
from urllib.request import urlopen, Request
from datetime import datetime, timezone, timedelta
from multiprocessing import RLock
from threading import Timer
from uuid import uuid4
import locale
import time
import json

from typing import Any, Optional, List

from .config import _Config
from .event import _Event

if __debug__:
    import logging
    log = logging.getLogger(name='Revolt').debug


class Revolt:
    """
        Revolt analytics client.

        Use ``send_event`` to send analytics events.

        Current implementation ignores errors occuring when sending events.
        Errors will be shown in logs but there will be no retries.

        Parameters
        ----------
        tracking_id : str
            Your unique client tracking ID. If you don't have tracking_id please contact Revolt Team.
        secret_key : str
            Client authorization secret for your tracking ID
        app_code : str
            Your application name/identifier i.e. 'com.company.myapp'
        app_version : str
            Your application version i.e. `1.12.4`
        app_instance_id : Optional[str]
            Unique application instance ID. It will be randomly generated each time if None provided.
            It should be reused for same device/application instance.
        timezone : datetime.timezone
            Timezone used to send events. Default is current timezone provided by system.
        revolt_host : str
            Host name of Revolt server
        batch_size : int
            Maximum size of event batches sent to server. Events will be sent automatically when queue
            reaches batch_size. Default is 20.
        auto_flush_delay : Optional[int]
            Delay in miliseconds before automatically sending events batch if batch_size was not reached.
            Calling ``send_event`` will reset the timer. Auto flush will be disabled if you pass None instead.
            If auto flush is disabled events will be flushed only if queue reaches batch_size or manually.
            Default is 5 seconds (5000).

    """  # noqa: E501

    def __init__(self,
                 tracking_id: str,
                 secret_key: str,
                 app_code: str,
                 app_version: str,
                 app_instance_id: Optional[str] = None,
                 timezone: timezone = timezone(timedelta(seconds=time.localtime().tm_gmtoff)),  # noqa: E501
                 revolt_host: str = 'api.revolt.rocks',
                 batch_size: int = 20,
                 auto_flush_delay: Optional[int] = 5000):
        if __debug__:
            log(f'Initializing Revolt {__version__}')  # noqa: E501

        self._config: _Config = _Config(
            app_code=app_code,
            app_version=app_version,
            revolt_host=revolt_host,
            tracking_id=tracking_id,
            secret_key=secret_key,
            app_instance_id=app_instance_id,
            timezone=timezone,
            batch_size=batch_size,
            auto_flush_delay=auto_flush_delay
        )
        self._lock: RLock = RLock()
        self._executor = ThreadPoolExecutor(  # TODO: compare with ProcessPoolExecutor for performance # noqa: E501
            max_workers=1,
        )
        self._event_queue: List[_Event] = []

        if self._config.auto_flush_delay:
            self._delay_timer = Timer(
                self._config.auto_flush_delay / 1000.0,
                self._timed_flush
            )
        elif __debug__:
            log(f'Auto flush delay disabled')

        if __debug__:
            log(f'Initialized Revolt client with tracking_id: {tracking_id} and app_instance_id: {app_instance_id}')  # noqa: E501

        self._send_initial_event()

    def send_event(self, type: str, data: Optional[Any] = None, flush: bool = False):  # noqa: E501
        """
        Adds analytics event to queue. Event timestamp will be assigned when this method is called.
        Events are collected before sending and sent if forced by flush, after reaching queue size equal
        batch size defined when initializing client or after delay if auto flush is enabled, after
        defined time of inactivity. Calling this method resets auto flush timer.

        Parameters
        ----------
        type : str
            Event type name, max 32 characters. It should use dots for separating domain,
            object, event (example: ui.activity.started), last element of name should be a verb
            expressing what happened e.g. signedIn, started, deleted etc.  
            Type of event determines format of event data.
        data : Optional[Any]
            Event data. Must be json serializable or None
        flush : bool
            Forces to send this and all queued events immediately if set to True. Default is False
        Returns
        -------
        None
        """  # noqa: E501
        assert type  # nosec
        assert len(type) <= 32  # nosec

        self._send(
            _Event(
                id=str(uuid4()),
                type=type,
                data=data,
                timestamp=_timestamp()
            ),
            flush
        )

    # private

    def _send(self, event: _Event, flush: bool):
        if __debug__:
            log(f'Enqueueing event [{event.id}] of type: {event.type} with data: {event.data}')  # noqa: E501
        with self._lock:
            self._event_queue.append(event)
            if flush or len(self._event_queue) >= self._config.batch_size:
                self._async_flush(self._event_queue)
                self._event_queue = []
                if self._config.auto_flush_delay:
                    self._stop_timer()
            elif self._config.auto_flush_delay:
                self._reset_timer()
            else:
                pass  # keep waiting

    def _send_initial_event(self):
        self._send(
            _Event(
                id=str(uuid4()),
                type='system.appInstanceData',
                data={
                    'app': {
                        'type': 'backend',  # no reason to add more types for now # noqa: E501
                        'code': self._config.app_code,
                        'version': self._config.app_version,
                        'sdkVersion': __version__
                    },
                    'device': {
                        'language': locale.getlocale()[0],
                        'zoneOffset': self._config.timezone_offset
                    }
                },
                timestamp=_timestamp()
            ),
            flush=False
        )

    def _timed_flush(self):
        with self._lock:
            assert len(self._event_queue) >= 0  # nosec
            if __debug__:
                log(f'Flushing after {self._config.auto_flush_delay} miliseconds of inactivity')  # noqa: E501
            self._async_flush(self._event_queue)
            self._event_queue = []

    def _async_flush(self, events: List[_Event]):
        def flush():
            try:
                response = urlopen(self._prepare_request(events))  # nosec
            except Exception as e:
                log(f'Error when sending events {e}')
                return

            try:
                result = json.loads(response.read())
                log(f'Successfully sent {result["eventsAccepted"]} events')
                error = result.get('eventError')
                if error:
                    message = error.get('errorMessage')
                    if message:
                        log(f'There was an error while sending events (code: {error["errorCode"]}): {message}')  # noqa: E501
                    else:
                        log(f'There was an unknown error while sending events, code: {error["errorCode"]}')  # noqa: E501
            except Exception as e:
                log(f'Error when decoding response {e}')

        if __debug__:
            log(f'Flushing {len(events)} events')

        self._executor.submit(flush)

    def _prepare_request(self, events: List[_Event]):
        assert events  # nosec

        return Request(
            url=self._config.endpoint_url,
            method='POST',
            headers={
                'Authorization': 'Basic ' + self._config.credential,
                'Content-Type': 'application/json; charset=utf-8;',
                'User-Agent': f'Revolt Python SDK {__version__}'
            },
            data=self._prepare_request_body(events)
        )

    def _prepare_request_body(self, events: List[_Event]):
        return json.dumps(
            [
                {
                    'meta': {
                        'id': event.id,
                        'type': event.type,
                        'timestamp': event.timestamp
                    },
                    "data": event.data
                }
                for event in events
            ]
        ).encode('utf-8')

    def _stop_timer(self):
        assert self._config.auto_flush_delay  # nosec

        self._delay_timer.cancel()

    def _reset_timer(self):
        assert self._config.auto_flush_delay  # nosec

        self._delay_timer.cancel()
        self._delay_timer = Timer(
            self._config.auto_flush_delay / 1000.0,
            self._timed_flush
        )
        self._delay_timer.start()


def _timestamp() -> int:
    return int(datetime.utcnow().timestamp() * 1000)
