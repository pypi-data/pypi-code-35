from aiohttp import ClientSession
import functools
from logging import getLogger
from urllib.parse import quote_plus

_logger = getLogger(__name__)
_logger.setLevel('NOTSET')


CACHE_DURATION = 15 * 60  # seconds

class Extensions:
    pass

class PaybearError(Exception):
    pass

class Paybear:
    # https://github.com/Paybear/paybear-samples
    def __init__(self, app, raise_for_status=True, logger=None):
        global _logger

        if logger is not None:
            _logger = logger

        self.token = app.config.SERVICES['paybear-v1']['creds']['client_secret']
        self.public_key = app.config.SERVICES['paybear-v1']['creds']['client_id']
        self.callback_url = app.config.SERVICES['paybear-v1']['creds']['callback_url']
        self.raise_for_status = raise_for_status
        if not hasattr(app, 'exts'):
            app.exts = Extensions()
        app.exts.paybear = self

    async def get_currencies(self):
        '''
        Get a list of enabled currencies
        '''
        BASE = 'https://api.savvy.io/v3/currencies?token={token}'
        async with ClientSession() as sess:
            async with sess.get(BASE.format(token=self.token)) as resp:
                json = await resp.json()
                if self.raise_for_status is not False:
                    try:
                        resp.raise_for_status()
                    except Exception as e:
                        _logger.error(json)
                        raise PaybearError(e)
                return json

    async def create_payment(self, crypto, callback_url=None, lock_address_timeout=None):
        '''
        The API always responds with a JSON string. 
            [data] collection contains the important values: 
                [address] is the payment address to show to the customer 
                [invoice] is our inner payment identifier, 
                keep it in a safe place and never disclose to your clients

        crypto: One of (eth, btc, bch, ltc, dash, btg, etc)

        lock_address_timeout:
            Time interval in seconds during which the address is locked for this invoice only. 86400 seconds by default. Set ‑1 for infinite lock
        
        Example ::

            {
                "success": true,
                "data": {
                    "invoice": "d1ddf6e3767030b08032cf2eae403600",
                    "address": "0x2073eb3be1a41908e0353427da7f16412a01ae71"
                }
            }
        '''
        if callback_url is not None:
            self.callback_url = callback_url
        BASE = 'https://api.savvy.io/v3/{crypto}/payment/{callback_url}?token={token}'
        if lock_address_timeout:
            lck_addr = '&lock_address_timeout={}'.format(lock_address_timeout)
            BASE += lck_addr
        async with ClientSession() as sess:
            async with sess.get(BASE.format(crypto=crypto, callback_url=quote_plus(self.callback_url), token=self.token)) as resp:
                json = await resp.json()
                if self.raise_for_status is not False:
                    try:
                        resp.raise_for_status()
                    except Exception as e:
                        _logger.error(json)
                        raise PaybearError(e)
                return json

    async def xrate_all(self, fiat):
        ''' 
        The API returns a JSON string containing the rates from several online exchanges, 
        as well as the average rate. It is recommended to cache the rates for 10-15 minutes.
        
        Example ::

        {
            "success": true,
            "data": {
                "ltc": {
                    "poloniex": 340.986909455,
                    "hitbtc": 340.568,
                    "bittrex": 340.25,
                    "bitfinex": 341.295,
                    "mid": 340.77497736375
                },
                "eth": {
                    "poloniex": 804.580989955,
                    "hitbtc": 805.88,
                    "bittrex": 803.47641155,
                    "bitfinex": 805.125,
                    "mid": 804.76560037625
                },
                "dash": {
                    "poloniex": 1129.8512215,
                    "hitbtc": 1130.145,
                    "bittrex": 1134.1035001,
                    "mid": 1131.3665738666666
                },
                "btg": {
                    "hitbtc": 320.485,
                    "bittrex": 317.90500002,
                    "bitfinex": 320.46500003,
                    "mid": 319.61833334
                },
                "btc": {
                    "poloniex": 17348.94643245,
                    "hitbtc": 17322.91,
                    "bittrex": 17347.05,
                    "bitfinex": 17355.5,
                    "mid": 17343.6016081125
                },
                "bch": {
                    "poloniex": 2595.49999996,
                    "hitbtc": 2600.6334100004,
                    "bitfinex": 2591.55,
                    "mid": 2595.8944699866665
                }
            }
        }

        One of (usd, eur, cad, rub etc) '''
        BASE = 'https://api.savvy.io/v3/exchange/{fiat}/rate'
        async with ClientSession() as sess:
            async with sess.get(BASE.format(fiat=fiat)) as resp:
                json = await resp.json()
                if self.raise_for_status is not False:
                    try:
                        resp.raise_for_status()
                    except Exception as e:
                        _logger.error(json)
                        raise PaybearError(e)
                return json

    async def xrate(self, fiat, crypto):
        '''
        If you are using more than one currency, we recommend usng the call above to get all rates with one request.

        Example ::

            {
                "success": true,
                "data": {
                    "poloniex": 301.71905,
                    "bittrex": 302.05,
                    "bitfinex": 301.53499,
                    "mid": 301.76807
                }
            }
   
        ones of:
        crypto	Crypto currency (eth, btc, bch, ltc, dash, btg)
        fiat	Fiat currency (usd, eur, cad, rub etc)
        '''
        BASE = 'https://api.savvy.io/v3/{crypto}/exchange/{fiat}/rate'
        async with ClientSession() as sess:
            async with sess.get(BASE.format(crypto=crypto, fiat=fiat)) as resp:
                json = await resp.json()
                if self.raise_for_status is not False:
                    try:
                        resp.raise_for_status()
                    except Exception as e:
                        _logger.error(json)
                        raise PaybearError(e)
                return json
