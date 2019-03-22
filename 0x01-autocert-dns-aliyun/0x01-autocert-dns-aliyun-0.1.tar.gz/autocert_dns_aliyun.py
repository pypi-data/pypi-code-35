"""Aliyun DNS plugin for autocert project"""

__all__ = [
    'AccessKeyCredential', 'StsTokenCredential', 'RamRoleArnCredential',
    'EcsRamRoleCredential', 'RsaKeyPairCredential',
    'AliyunDNS',
]

import json

import aliyunsdkcore.client
from aliyunsdkalidns.request.v20150109.GetMainDomainNameRequest import \
    GetMainDomainNameRequest
from aliyunsdkalidns.request.v20150109.AddDomainRecordRequest import \
    AddDomainRecordRequest
from aliyunsdkalidns.request.v20150109.DeleteDomainRecordRequest import \
    DeleteDomainRecordRequest
from aliyunsdkcore.auth.credentials import (
    AccessKeyCredential, StsTokenCredential, RamRoleArnCredential,
    EcsRamRoleCredential, RsaKeyPairCredential,
)


class AliyunDNS:
    def __init__(self, credential):
        self.aliyun = aliyunsdkcore.client.AcsClient(credential=credential)
        self.records = []

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.clean()

    def perform_dns01(self, domain, validation):
        domain_info = self._call(GetMainDomainNameRequest, InputString=domain)
        domain = domain_info['DomainName']
        rr = domain_info['RR']
        self.records.append(self._call(
            AddDomainRecordRequest,
            DomainName=domain, RR=rr, Type='TXT', Value=validation,
        )['RecordId'])

    def clean(self):
        for record_id in self.records:
            self._call(DeleteDomainRecordRequest, RecordId=record_id)

    def _call(self, request, **kwargs):
        if isinstance(request, type):
            request = request()
        for key, value in kwargs.items():
            getattr(request, f'set_{key}')(value)
        return json.loads(self.aliyun.do_action_with_exception(request))
