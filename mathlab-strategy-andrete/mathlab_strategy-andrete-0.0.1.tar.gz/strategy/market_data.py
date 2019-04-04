from datetime import datetime

import requests
import pandas

from .exchange import Exchanges
from .common import Interval
from .ticker import Pair, Symbol

POSTGREST_URL = 'http://localhost:3000/test2'


class MarketData():
    def ohlc_history(
        self, pair: Pair, interval: Interval,
        start: datetime, end: datetime
    ) -> pandas.DataFrame:
        if pair.get_exchange() != Exchanges.Binance:
            return NotImplemented
        if not isinstance(pair, Pair):
            return NotImplemented
        if interval != Interval.M1:
            return NotImplemented
        params = {
            'and': '(time.gte.%s,time.lte.%s)' % (
                start.isoformat(), end.isoformat()),
            'pair': 'eq.%s%s' % (pair.quote_currency, pair.base_currency),
            'exchange_id': 'eq.6',
            'period': 'eq.1',
            'order': 'time'
        }
        r = requests.get(POSTGREST_URL, params=params)
        if r.status_code == 200:
            df = pandas.DataFrame(r.json())
            df.set_index('time', inplace=True)
            return df
        return NotImplemented
