import pandas_datareader as web
import pandas as pd
import datetime
import functools


class MarketDataService:

    def get_morning_star_df(self, stock_name, start, end):
        return web.DataReader(stock_name, 'morningstar', start, end).reset_index()

    def get_quandl_df(self, stock_name, start, end):
        return web.DataReader(stock_name, 'quandl', start, end).reset_index()

    def get_iex_df(self, stock_name, start, end):
        df = web.DataReader(stock_name, 'iex', start, end).reset_index()
        df = df.rename(columns = {'date':'Date', 'open':'Open', 'high':'High', 'low':'Low', 'close':'Close', 'volume':'Volume'})
        return df

    # Usage: MarketDataService.get_df(stockname, 'morningstar', startTime, endTime)
    #     or MarketDataService.get_df(stockname, 'iex', startTime, endTime)
    @functools.lru_cache(maxsize=None)
    def get_df(self, stock_name, service_name, start, end):

        return {
            'morningstar': self.get_morning_star_df(stock_name, start, end),
            # 'quandl': self.get_quandl_df(stock_name, start, end)
            'iex' : self.get_iex_df(stock_name, start, end)
        }[service_name]

