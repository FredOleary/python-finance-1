#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  3 11:15:04 2017

@author: fredoleary
"""

#from yahoo_finance import Share

import urllib.request
import json
from datetime import datetime
import demjson

from dateutil import parser
from tzlocal import get_localzone
import pytz

class FinanceWeb():
    """ Class for retreiving stock quotes and news """
    @classmethod
    def get_quotes_for_stock(cls, stock_ticker):
        """ Return intraday prices from alphavantage. """
        quotes = []
        url = "https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY" +\
              "&symbol=" + stock_ticker + "&interval=1min&outputsize=full" + \
              "&apikey=M8KGCPCGZQSJJO3V"
        response = urllib.request.urlopen(url)
        result = response.read()
        str_result = result.decode("utf-8")
        python_obj = json.loads(str_result)
        for key, value in python_obj["Time Series (1min)"].items():
            # The date/times are EST, convert to GMT and remove Tz info.
            # (sqlite doesn't like tz info)
            dt_est = parser.parse(key)  # Date time with no TZ info
            dt_est = pytz.timezone('US/Eastern').localize(dt_est) # Date time with EST info
            dt_gmt = dt_est.astimezone(pytz.utc) # Date time with as GMT
            dt_gmt = dt_gmt.replace(tzinfo=None) # GM time with tz info stripped
            quotes.append({"time": dt_gmt, "price":value["4. close"]})
        return quotes

    @classmethod
    def get_news_for_stock(cls, stock_ticker):
        """ Return the list of news items for stock_ticker using Googles Finance """
        news = []
        url = "https://www.google.com/finance/company_news?q=" + stock_ticker + "&output=json"
        response = urllib.request.urlopen(url)
        result = response.read()
        str_result = result.decode("utf-8")

        news_items = demjson.decode(str_result)
        for news_item in news_items["clusters"]:
            if news_item.get('a'):
                item_array = news_item["a"]
                for item in item_array:
                    dt_local = datetime.fromtimestamp(int(item["tt"]))
                    # this will be in local time, convert to GMT
                    dt_local = dt_local.astimezone(get_localzone())  # Adds local tz info
                    dt_gmt = dt_local.astimezone(pytz.utc)     # Converts to gmt
                    dt_gmt = dt_gmt.replace(tzinfo=None) # finally removes the tz info
                    #print( "date/time: ", dt_gmt)
                    news.append({"title":item["t"], "description":item["sp"], \
                                 "source":item["s"], "time":dt_gmt})

        return news
    