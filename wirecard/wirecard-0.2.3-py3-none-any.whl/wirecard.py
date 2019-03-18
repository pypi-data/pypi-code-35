from base64 import b64encode
from decimal import Decimal
import os
import uuid

from glom import glom
import requests

from .constants import (
    CARD_ELIGIBLE_3D_ID,
    CHECK_ENROLLMENT,
    CREATION_SUCCESS_ID,
    PURCHASE,
    SUCCESS,
)
from .exceptions import (
    WirecardFailedInit,
    WirecardFailedTransaction,
    WirecardInvalidCard,
    WirecardInvalidRequestedAmount,
)


class Wirecard:
    def __init__(self, username=None, password=None, merchant_account_id=None, url=None, ip=None):
        self.username = os.getenv('WIRECARD_USERNAME', username)
        self.password = os.getenv('WIRECARD_PASSWORD', password)
        self.merchant_account_id = os.getenv('WIRECARD_MERCHANT_ACCOUNT_ID', merchant_account_id)
        self.url = os.getenv('WIRECARD_API_URL', url)
        self.origin_ip = os.getenv('WIRECARD_ORIGIN_IP', ip)

        self.basic_authorization = None

        self.validate()

    def check_3d_enrollment(self, card, account_holder, requested_amount):
        data = {
            'payment': {
                'merchant-account-id': {
                    'value': self.merchant_account_id,
                },
                'request-id': self._generate_request_id(),
                'transaction-type': CHECK_ENROLLMENT,
                'requested-amount': requested_amount.as_dict(),
                'account-holder': account_holder.as_dict(),
                'card': card.as_dict(),
                'ip-address': self.origin_ip,
            },
        }

        headers = self._make_headers()
        result = requests.post(self.url, json=data, headers=headers)
        response = result.json()

        statuses = glom(response, 'payment.statuses.status')
        statuses_codes = [status.get('code') for status in statuses]
        transaction_state = glom(response, 'payment.transaction-state')

        success_conditions = [
            CREATION_SUCCESS_ID in statuses_codes,
            CARD_ELIGIBLE_3D_ID in statuses_codes,
            transaction_state == SUCCESS,
        ]

        if all(success_conditions):
            return response

        transaction_id = glom(response, 'payment.transaction-id', default='transaction_id not present')
        raise WirecardFailedTransaction(transaction_id, 'check_3d_enrollment', statuses)

    def payment_request_with_pares(self, pares, parent_transaction_id):
        data = {
            'payment': {
                'merchant-account-id': {
                    'value': self.merchant_account_id,
                },
                'request-id': self._generate_request_id(),
                'transaction-type': PURCHASE,
                'parent-transaction-id': parent_transaction_id,
                'three-d': {
                    'pares': pares,
                },
                'ip-address': self.origin_ip,
            },
        }

        headers = self._make_headers()
        result = requests.post(self.url, json=data, headers=headers)
        response = result.json()

        statuses = glom(response, 'payment.statuses.status')
        statuses_codes = [status.get('code') for status in statuses]
        transaction_state = glom(response, 'payment.transaction-state')
        success_conditions = [
            CREATION_SUCCESS_ID in statuses_codes,
            transaction_state == SUCCESS,
        ]

        if all(success_conditions):
            return response

        raise WirecardFailedTransaction(
            parent_transaction_id,
            'payment_request_with_pares',
            statuses,
        )

    def validate(self):
        failed_conditions = [
            self.username is None,
            self.password is None,
            self.merchant_account_id is None,
            self.url is None,
        ]

        if any(failed_conditions):
            message = 'Parameters username, password, merchant_account_id and url are required'
            raise WirecardFailedInit(message)

    def _generate_request_id(self):
        return str(uuid.uuid4())

    def _generate_basic_authorization(self):
        if self.basic_authorization:
            return self.basic_authorization

        username_password = f'{self.username}:{self.password}'
        basic_credentials = b64encode(bytes(username_password.encode())).decode()
        self.basic_authorization = f'Basic {basic_credentials}'

        return self.basic_authorization

    def _make_headers(self):
        return {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': self._generate_basic_authorization(),
        }


class Card:
    def __init__(self, account_number, expiration_month, expiration_year, security_code, _type):
        self.account_number = account_number
        self.expiration_month = expiration_month
        self.expiration_year = expiration_year
        self.security_code = security_code
        self.type = _type

        self._clean()
        self.validate()

    def _clean(self):
        self.type = self.type.lower()
        self.account_number = self.account_number.replace(' ', '')

    def as_dict(self):
        return {
            'account-number': self.account_number,
            'expiration-month': self.expiration_month,
            'expiration-year': self.expiration_year,
            'card-security-code': self.security_code,
            'card-type': self.type,
        }

    def validate(self):
        if len(self.expiration_month) != 2:
            raise WirecardInvalidCard('expiration_month length should be 2')

        if len(self.expiration_year) != 4:
            raise WirecardInvalidCard('expiration_year length should be 4')

        if len(self.security_code) != 3:
            raise WirecardInvalidCard('security_code length should be 3')


class AccountHolder:
    def __init__(self, first_name, last_name, **kwargs):
        self.first_name = first_name
        self.last_name = last_name
        self.other_info = kwargs

    def as_dict(self):
        return {
            'first-name': self.first_name,
            'last-name': self.last_name,
            **self.other_info,
        }


class RequestedAmount:
    def __init__(self, amount, currency):
        self.amount = Decimal(amount).quantize(Decimal('.00'))
        self.currency = currency

        self.validate()

    def as_dict(self):
        return {
            'value': str(self.amount),
            'currency': self.currency,
        }

    def validate(self):
        if len(self.currency) != 3:
            raise WirecardInvalidRequestedAmount('currency length should be 3')

        integer_part, fractional_part = str(self.amount).split('.')
        if len(integer_part) > 18:
            raise WirecardInvalidRequestedAmount('integer_part length should be less than 18')

        if len(fractional_part) > 2:
            raise WirecardInvalidRequestedAmount('fractional_part length should be less than 2')
