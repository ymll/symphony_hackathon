import pandas_datareader as web
import pandas as pd
import datetime
import requests
import base64
from requests.auth import HTTPBasicAuth
import functools
from pandas.io.json import json_normalize
import datetime

class MarketDataService:

    @functools.lru_cache(maxsize=None)
    def get_morning_star_df(self, stock_name, start, end):
        return web.DataReader(stock_name, 'morningstar', start, end).reset_index()

    @functools.lru_cache(maxsize=None)
    def get_quandl_df(self, stock_name, start, end):
        return web.DataReader(stock_name, 'quandl', start, end).reset_index()

    @functools.lru_cache(maxsize=None)
    def get_iex_df(self, stock_name, start, end):
        df = web.DataReader(stock_name, 'iex', start, end).reset_index()
        df = df.rename(columns = {'date':'Date', 'open':'Open', 'high':'High', 'low':'Low', 'close':'Close', 'volume':'Volume'})
        return df

    @functools.lru_cache(maxsize=None)
    def get_fx_df(self, currency_pair, start, end):
        timeframe = 'D1'
        start_date = start.strftime('%Y-%m-%d')
        end_date = end.strftime('%Y-%m-%d')
        page_size = 100000
        page_number = 1

        INTRINIO_USER = '00ce8b2727b4f3cf21e272fe3ce66b57'
        INTRINIO_PASS = 'eefa9363ad30aa65b8ad3b6c71da1b0a'
        df = pd.DataFrame()
        while (True):
            url = "https://api.intrinio.com/currency_prices?pair={}&timeframe={}&start_date={}&end_date={}&page_size={}&page_number={}"\
                .format(currency_pair, timeframe, start_date, end_date, page_size, page_number)
            r = requests.get(url, auth=(INTRINIO_USER, INTRINIO_PASS))

            print("url:", url)
            j = r.json()
            df = df.append(json_normalize(j['data']))
            if j['total_pages'] == 0:
                return None
            elif j['total_pages'] == j['current_page']:
                break
            else:
                page_number += 1
        df = df.rename(columns = {'date':'Date', 'open_ask':'Open', 'high_ask':'High', 'low_ask':'Low', 'close_ask':'Close', 'total_ticks':'Volume'})

        # print(df)
        return df

    # Usage: MarketDataService.get_df(stockname, 'morningstar', startTime, endTime)
    @functools.lru_cache(maxsize=None)
    def get_df(self, stock_name, service_name, start, end):
        return {
            'morningstar'   : self.get_morning_star_df,
            # 'quandl': self.get_quandl_df
            'iex'           : self.get_iex_df,
            'fx'            : self.get_fx_df
        }[service_name](stock_name, start, end)

