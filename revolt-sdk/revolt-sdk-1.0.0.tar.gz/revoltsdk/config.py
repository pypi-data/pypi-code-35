import datetime
from base64 import b64encode
from uuid import uuid4

from typing import Optional


class _Config:

    def __init__(self,
                 app_code: str,
                 app_version: str,
                 revolt_host: str,
                 tracking_id: str,
                 secret_key: str,
                 app_instance_id: Optional[str],
                 timezone: datetime.timezone,
                 batch_size: int,
                 auto_flush_delay: Optional[int]):
        assert app_code  # nosec
        assert app_version  # nosec
        assert revolt_host  # nosec
        assert tracking_id  # nosec
        assert secret_key  # nosec
        assert timezone  # nosec
        assert batch_size > 0  # nosec
        assert auto_flush_delay is None or auto_flush_delay > 0  # nosec

        app_instance_id = app_instance_id or uuid4().hex
        self.app_code = app_code
        self.app_version = app_version
        self.timezone_offset: int = int(timezone.utcoffset(None).seconds / 60)  # offset in hours # noqa: E501
        self.credential: str = b64encode(
            f'{tracking_id}:{secret_key}'.encode('ascii')
        ).decode("utf-8")
        self.endpoint_url: str = f'https://{revolt_host}/api/v1/{tracking_id}/{app_instance_id}/events'  # noqa: E501
        self.batch_size: int = batch_size
        self.auto_flush_delay: Optional[int] = auto_flush_delay
