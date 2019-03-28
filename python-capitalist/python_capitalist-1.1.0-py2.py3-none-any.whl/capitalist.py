from decimal import Decimal
from pathlib import Path
from typing import Union

from capitalist.exceptions import ResponseException
from capitalist.models import Account, CurrencyRate
from .auth import Authenticator, Signer
from .exceptions import RequestException, ImproperlyConfigured
from .request_executor import RequestExecutor
from .utils import retry


class Capitalist:
    def __init__(
            self,
            login,
            password,
            request_executor_class=RequestExecutor,
            authenticator_class=Authenticator,
            signer_class=Signer,
            private_key: Union[bytes, Path] = None,
    ):
        self.login = login
        self.request_executor = request_executor_class()
        self.authenticator = authenticator_class(self.request_executor, login, password)
        self.signer = None
        if private_key is not None:
            if isinstance(private_key, Path):
                private_key = private_key.read_bytes()
            self.signer = signer_class(private_key)

    @retry((RequestException,))
    def secure_request(self, operation, data=None, **kwargs):
        if data is None:
            data = {}
        data.update({
            'operation': operation,
            'login': self.login,
            'token': self.authenticator.token,
            'encrypted_password': self.authenticator.encrypted_password.password,
        })
        kwargs['data'] = data
        response_json = self.request_executor.request(**kwargs)
        code = response_json['code']
        if code != 0:
            raise ResponseException(code, response_json['message'])
        return response_json

    def accounts(self):
        json_data = self.secure_request('get_accounts')
        return [Account.parse_json(acc_json) for acc_json in json_data['data']['accounts']]

    def currency_rates(self):
        json_data = self.secure_request('currency_rates')['data']['rates']
        rates = []
        for type_ in CurrencyRate.TYPES:
            for rate_data in json_data[type_]:
                rates.append(CurrencyRate.parse_json(rate_data, type_=type_))
        return rates

    def import_batch_advanced(self, payments, account_rur, account_usd, account_eur, account_btc):
        if self.signer is None:
            raise ImproperlyConfigured('Provide private key and/or passphrase to be able to sign data.')

        payment_data = '\n'.join([payment.as_batch_record() for payment in payments])
        data = {
            'batch': payment_data,
            'verification_type': 'SIGNATURE',
            'verification_data': self.signer.sign(payment_data.encode('utf-8')),
            'account_RUR': account_rur,
            'account_USD': account_usd,
            'account_EUR': account_eur,
            'account_BTC': account_btc,
        }
        return self.secure_request('import_batch_advanced', data)

    def get_document_fee(
            self, document_type: str, source_account: str, amount: Decimal, dest_account: str = None,
            wiretag: str = None):
        data = {
            'document_type': document_type,
            'source_account': source_account,
            'amount': amount,
        }
        if dest_account:
            data['dest_account'] = dest_account
        if wiretag:
            data['wiretag'] = wiretag
        return self.secure_request('get_document_fee', data)

    def get_batch_info(self, batch_id, page_size=1, start_offset=0):
        data = {
            'batch_id': batch_id,
            'page_size': page_size,
            'start_offset': start_offset,
        }
        return self.secure_request('get_batch_info', data)
