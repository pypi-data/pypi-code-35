from datetime import datetime
from decimal import Decimal
from typing import List

import pandas
import talib

from .chainable import Chainable
from .framework import Strategy
from .market_data import MarketData
from .ticker import Pair
from .common import Interval, Instructions
from .candle import Close
from .technical_analysis import MA


class BacktestResult():
    pass


class BacktestConfig(Chainable):
    def __init__(
        self, pairs: List[Pair], interval: Interval,
        start: datetime, end: datetime,
        maker_fee: Decimal, taker_fee: Decimal
    ):
        self.pairs = pairs
        self.interval = interval
        self.start = start
        self.end = end
        self.maker_fee = maker_fee
        self.taker_fee = taker_fee


class Backtest():
    def __init__(self, config: BacktestConfig):
        self.config = config

    def set_config(self, config: BacktestConfig) -> None:
        self.config = config

    def get_config(self) -> BacktestConfig:
        return self.config

    def run(self, strategy: Strategy):
        ohlcs = {}
        for pair in self.config.pairs:
            ohlcs[pair] = MarketData().ohlc_history(
                pair, self.config.interval,
                self.config.start, self.config.end
            )
        df = pandas.concat({
            pair: pandas.concat([
                ohlc[['open', 'close']],
                talib.SMA(ohlc['close'], 100).rename('ma_close_100')
            ], axis=1)
            for pair, ohlc in ohlcs.items()
        }, axis=1)
        for index, row in df.iterrows():
            for item in row.iteritems():
                close = Close(
                        pair=item[0][0],
                        interval=self.config.interval
                )
                if item[0][1] == 'close':
                    close.set_value(item[1])
                elif item[0][1] == 'ma_close_100':
                    ma = MA(
                        close,
                        100
                    )
                    ma.set_value(item[1])
            strategy.on_tick()
            for instruction in Instructions().get_all():
                print(index, instruction)
            Instructions().clear()
