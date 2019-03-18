import logging
from decimal import Decimal, ROUND_DOWN, getcontext
from beem.instance import shared_steem_instance
from privex.jsonrpc import SteemEngineRPC
from privex.steemengine import exceptions
from privex.steemengine.SteemEngineHistory import SteemEngineHistory

log = logging.getLogger(__name__)
getcontext().rounding = ROUND_DOWN


class SteemEngineToken:
    """
    SteemEngineToken - a wrapper class around privex.jsonrpc.SteemEngineRPC, with support
    for signing transactions, including issuing/sending tokens.
    
        +===================================================+
        |                 © 2019 Privex Inc.                |
        |               https://www.privex.io               |
        +===================================================+
        |                                                   |
        |        Python Steem Engine Library                |
        |        License: X11/MIT                           |
        |                                                   |
        |        Core Developer(s):                         |
        |                                                   |
        |          (+)  Chris (@someguy123) [Privex]        |
        |                                                   |
        +===================================================+
    """

    steem = shared_steem_instance()

    def __init__(self, network_account='ssc-mainnet1', history_conf: dict =None, **rpc_args):
        self.rpc = SteemEngineRPC(**rpc_args)
        self.network_account = network_account
        history_conf = {} if history_conf is None else history_conf
        self.history_rpc = SteemEngineHistory(**history_conf)

    def get_balances(self, user) -> list:
        return self.rpc.find(
            contract='tokens',
            table='balances',
            query=dict(account=user)
        )

    def get_token_balance(self, user, token) -> Decimal:
        balances = self.get_balances(user)
        for bal in balances:
            if bal['symbol'] == token.upper():
                return Decimal(bal['balance'])
        return Decimal(0)

    def account_exists(self, user) -> bool:
        return len(self.steem.rpc.get_account(user)) > 0

    def list_tokens(self) -> list:
        return self.rpc.find(
            contract='tokens',
            table='tokens',
            query={}
        )

    def list_transactions(self, account, symbol=None, limit=100, offset=0) -> list:
        """
        Get the Steem Engine transaction history for a given account
        :param account: Account name to filter by
        :param symbol: Symbol to filter by, e.g. ENG (optional)
        :param limit: Return this many transactions
        :param offset: Skip this many transactions (for pagination)
        :return: list of dict(block, txid, timestamp, symbol, from, from_type, to, to_type, memo, quantity)
        """
        symbol = symbol.upper()
        return self.history_rpc.get_history(account=account, symbol=symbol, limit=limit, offset=offset)

    def get_token(self, symbol) -> dict:
        return self.rpc.findone(
            contract='tokens',
            table='tokens',
            query=dict(symbol=symbol.upper())
        )

    def send_token(self, token, from_acc, to_acc, amount: Decimal, memo=""):
        t = self.get_token(token)
        if t is None:
            raise exceptions.TokenNotFound('Token {} does not exist'.format(t))
        amount = Decimal(amount)
        if Decimal(amount) < Decimal(pow(10, -t['precision'])):
            raise ArithmeticError('Amount {} is lower than token {}s precision of {} DP'
                                  .format(amount, token, t['precision']))

        balance = self.get_token_balance(from_acc, token)
        if Decimal(amount) > balance:
            raise exceptions.NotEnoughBalance('Account {} has a balance of {} but {} is needed.'.format(from_acc, balance, amount))

        if not self.account_exists(from_acc):
            raise exceptions.AccountNotFound('Cannot send because the sender {} does not exist'.format(to_acc))
        if not self.account_exists(to_acc):
            raise exceptions.AccountNotFound('Cannot send because the receiver {} does not exist'.format(to_acc))

        custom = dict(
            contractName="tokens",
            contractAction="transfer",
            contractPayload=dict(
                symbol=token.upper(),
                to=to_acc,
                quantity=('{0:.' + str(t['precision']) + 'f}').format(amount),
                memo=memo
            )
        )
        return self.steem.custom_json(self.network_account, custom, [from_acc])

    def issue_token(self, token, to, amount):
        """
        Issues a specified amount `amount` of `token` to the Steem account `to`
        Automatically queries Steem Engine API to find issuer of the token, and broadcast using Beem

        :param token: The symbol of the token to issue, e.g. ENG
        :param to: The Steem username to issue the tokens to
        :param amount: The amount of tokens to issue.
        :raises TokenNotFound: When a token does not exist
        :raises AccountNotFound: When the `to` account doesn't exist on Steem
        :raises beem.exceptions.MissingKeyError: No active key found for the issuer in beem wallet
        :return: Beem broadcast result
        """
        t = self.get_token(token)
        if t is None:
            raise exceptions.TokenNotFound('Token {} does not exist'.format(t))
        if Decimal(amount) < Decimal(pow(10, -t['precision'])):
            raise ArithmeticError('Amount {} is lower than token {}s precision of {} DP'
                                  .format(amount, token, t['precision']))
        if not self.account_exists(to):
            raise exceptions.AccountNotFound('Cannot issue because the account {} does not exist'.format(to))

        custom = dict(
            contractName="tokens",
            contractAction="issue",
            contractPayload=dict(
                symbol=token.upper(),
                to=to,
                quantity=('{0:.' + str(t['precision']) + 'f}').format(amount)
            )
        )
        return self.steem.custom_json(self.network_account, custom, [t['issuer']])


"""
+===================================================+
|                 © 2019 Privex Inc.                |
|               https://www.privex.io               |
+===================================================+
|                                                   |
|        Python Steem Engine library                |
|        License: X11/MIT                           |
|                                                   |
|        Core Developer(s):                         |
|                                                   |
|          (+)  Chris (@someguy123) [Privex]        |
|                                                   |
+===================================================+

Python SteemEngine - A small library for querying and interacting with the SteemEngine network (https://steem-engine.com)
Copyright (c) 2019    Privex Inc. ( https://www.privex.io )

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation 
files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, 
modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the 
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of 
the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE 
WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS 
OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR 
OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

Except as contained in this notice, the name(s) of the above copyright holders shall not be used in advertising or 
otherwise to promote the sale, use or other dealings in this Software without prior written authorization.
"""
