import json

import requests

from .client import Client
from .error import DownloadObjectError, UploadObjectError, CombineObjectsError

class SyncClient(Client):
    def __init__(self, **kwds):
        super().__init__(**kwds)


    def download_object(self, *,
            path,
            thumbnail=False,
            thumbnail_size=None,
            thumbnail_method=None,
            thumbnail_bgcolor=None,
            image_transform=None):
        download_url = self.build_download_object_url(
                path=path,
                thumbnail=thumbnail,
                thumbnail_size=thumbnail_size,
                thumbnail_method=thumbnail_method,
                thumbnail_bgcolor=thumbnail_bgcolor,
                image_transform=image_transform)
        r = requests.get(download_url)
        response = SyncResponse(
                status_code=r.status_code,
                content_type=r.headers['content-type'],
                data=r.content)
        if response.status_code == 200:
            return response
        else:
            raise DownloadObjectError(response)


    def upload_object(self, *,
            path,
            data,
            content_type,
            image_transform=None):
        upload_url = self.build_upload_object_url(
                path=path,
                image_transform=image_transform)
        r = requests.post(
                upload_url, 
                data=data,
                headers={'Content-Type': content_type})
        response = SyncResponse(
                status_code=r.status_code,
                content_type=r.headers['content-type'],
                data=r.content)
        if response.status_code == 200 and response.content_type == 'application/json':
            return json.loads(response.data.decode())
        else:
            raise UploadObjectError(response)


    async def combine_objects(self, *,
            path,
            objects,
            content_type):
        combine_url = self.build_combine_objects_url(
                path=path)
        r = requests.post(
                combine_url, 
                json={
                    'Files': objects,
                    'Content-Type': content_type
                    })
        response = SyncResponse(
                status_code=r.status_code,
                content_type=r.headers['content-type'],
                data=r.content)
        if response.status_code == 200 and response.content_type == 'application/json':
            return json.loads(response.data.decode())
        else:
            raise CombineObjectsError(response)


class SyncResponse:
    def __init__(self, *, status_code, content_type, data):
        self.status_code=status_code
        self.content_type=content_type
        self.data=data

