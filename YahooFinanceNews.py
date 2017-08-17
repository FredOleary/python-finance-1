#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  3 11:15:04 2017

@author: fredoleary
"""

#from yahoo_finance import Share

import urllib.request
import json
from html.parser import HTMLParser
from datetime import datetime
from datetime import timedelta
from dateutil import parser
from dateutil import tz
import pytz

class MyHTMLParser(HTMLParser):
    """ Custom HTML parser """
    def __init__(self):
        super().__init__()
        self.level = 0
        self.level_array = []
        self.triggered = False
        self.news_results = []
    def handle_starttag(self, tag, attrs):
        #print("Encountered a start tag:", tag)
        if tag == "script" or tag == "style":
            key = 0
        else:
            key = 1
        if self.level >= len(self.level_array):
            self.level_array.append(key)
        else:
            self.level_array[self.level] = key
        self.level = self.level+1
    def handle_endtag(self, tag):
        #print("Encountered an end tag :", tag)
        self.level = self.level-1

    def handle_data(self, data):
        if self.level_array[self.level-1] == 1:
            if self.triggered is True:
                #print("Encountered some data len:", len(data), " ->",  data)
                self.news_results.append(data)
            elif data == "Press Releases":
                self.triggered = True
#            print("Encountered some data  :", self.level)
#        else:
#            print("Data suppressed for level  :", self.level)
    def error(self, message):
        print("Encountered an error ", message)
    def get_raw_news(self):
        """ Returns the list of contents. """
        return self.news_results
class NewsParser:
    """Parse the HTML content entities. """
    def __init__(self, raw_news):
        self.news_data = raw_news
        self.news = []
    def dummy(self):
        """ Just to satisfy PyLint. There are other ways. """
        return self.news
    def parse_news(self):
        """ Parse the HTML content entities for news items. """
        # raw news is of the form:
        # Editor's Pick -- optional
        #source (Barrons.com )
        #•
        # relative time, ( 3 days ago)
        #title ("ETF Flopper: No Power...")
        #description ("Stock futures rose slightly early Friday")
        # additional content
        index = 0
        while (index +1) < len(self.news_data):
            if self.news_data[index +1] == "•":
                if (index + 4) < len(self.news_data):
                    date_time = self._process_date_time(self.news_data[index + 2])
                    if date_time is not None:
                        news_item = {'source' : self.news_data[index], \
                                  'time' : date_time, \
                                  'title' : self.news_data[index + 3], \
                                  'description' : self.news_data[index + 4]}
                        self.news.append(news_item)
            index = index +1
        return self.news
    @staticmethod
    def _process_date_time(date_diff):
        #date_diff is of the form N days/minutes/hours ago. E.g. 3 hours ago
        news_date_time = datetime.now(tz.tzlocal())
        tokens = date_diff.split()
        if len(tokens) >= 3:
            num = int(tokens[0])
            units = tokens[1]
            if units[len(units)-1] == 's':
                units = units[:len(units)-1]
            if units == "minute":
                num = num * 60
            elif units == "hour":
                num = num * 60 * 60
            elif units == "day":
                num = num * 24* 60 * 60
            else:
                print("Skipping news for: ", date_diff)
                return None
            news_date_time = news_date_time - timedelta(seconds=num)
        #convert to GM time zone
        news_date_time = news_date_time.astimezone(pytz.utc)
        #remove timezone info - sqlite won't parse it correctly
        news_date_time = news_date_time.replace(tzinfo=None)
        return news_date_time
def get_news_for_stock(stock_ticker):
    """ Return the list of news objects for stock_ticker. """
    url = "https://finance.yahoo.com/quote/" + stock_ticker + "?ltr=1"
    #https://finance.yahoo.com/quote/INTC?ltr=1
    response = urllib.request.urlopen(url)
    result = response.read()
    str_result = result.decode("utf-8")
    html_parser = MyHTMLParser()
    html_parser.feed(str_result)
    news_parser = NewsParser(html_parser.get_raw_news())
    news = news_parser.parse_news()
    return news


#def get_quotes_for_stock_yahoo(stock_ticker ):
#
#    The yahoo stock quote service doesn't work well.... if at all
#
#    stock = Share(stock_ticker)
#    stock.refresh()
#    date_time = parser.parse(stock.get_trade_datetime())
#    date_time  =  date_time .replace(tzinfo=None) # remove timezone, all datetimes must be utc
#    return { "price": stock.get_price(), \
#             "time": date_time}
#
def get_quotes_for_stock(stock_ticker):
    """ The key for alphavantage is M8KGCPCGZQSJJO3V. """
    quotes = []
    url = "https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY" +\
          "&symbol=" + stock_ticker + "&interval=1min&outputsize=full" + \
          "&apikey=M8KGCPCGZQSJJO3V"
    response = urllib.request.urlopen(url)
    result = response.read()
    str_result = result.decode("utf-8")
    python_obj = json.loads(str_result)
    for key, value in python_obj["Time Series (1min)"].items():
        # the date/times are EST, convert to GMT and remove Tz info. (sqlite doesn't like tz info)
        dt_est = parser.parse(key)  # Date time with no TZ info
        dt_est = pytz.timezone('US/Eastern').localize(dt_est) # Date time with EST info
        dt_gmt = dt_est.astimezone(pytz.utc) # Date time with as GMT
        dt_gmt = dt_gmt.replace(tzinfo=None) # GM time with tz info stripped
        quotes.append({"time": dt_gmt, "price":value["4. close"]})
    return quotes
