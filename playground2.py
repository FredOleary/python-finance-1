#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 11 10:26:16 2017

@author: fredoleary
"""
import urllib.request
import json
import sys
import feedparser
import requests
from html.parser import HTMLParser
import re
import demjson
from datetime import datetime
from WebFinance import FinanceWeb
from dateutil import parser
### alphavantage key M8KGCPCGZQSJJO3V

"""
https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=MSFT&interval=15min&outputsize=compact&apikey=M8KGCPCGZQSJJO3V
"""

class MyHTMLParser(HTMLParser):
    """ Custom HTML parser """
    def __init__(self):
        super().__init__()
        self.level = 0
        self.level_array = []
        self.triggered = False
        self.news_results = []
    def handle_starttag(self, tag, attrs):
        print("Encountered a start tag:", tag)
        """
        if tag == "script" or tag == "style":
            key = 0
        else:
            key = 1
        if self.level >= len(self.level_array):
            self.level_array.append(key)
        else:
            self.level_array[self.level] = key
        self.level = self.level+1
        """
    def handle_endtag(self, tag):
        print("Encountered an end tag :", tag)
        #self.level = self.level-1

    def handle_data(self, data):
        print("Encountered some data  :", data)
        self.news_results.append(data)
        """
        if self.level_array[self.level-1] == 1:
            if self.triggered is True:
                #print("Encountered some data len:", len(data), " ->",  data)
                self.news_results.append(data)
            elif data == "Press Releases":
                self.triggered = True
#            print("Encountered some data  :", self.level)
#        else:
#            print("Data suppressed for level  :", self.level)
         """
    def error(self, message):
        print("Encountered an error ", message)
    def get_raw_news(self):
        """ Returns the list of contents. """
        return self.news_results

if __name__ == "__main__":
    dt_gmt = parser.parse("2017-08-21T20:03:23.000+00:00")
    dt_gmt = dt_gmt.replace(tzinfo=None)     
    web = FinanceWeb()
    news = web.get_news_for_stock_cf("LITE")
    print("News: ", news)
    sys.exit()
    
    url = "https://www.google.com/finance/company_news?q=Nasdaq:MSFT&output=json"
    response = requests.get(url)
    #data = response.json()
    
    url =  "https://www.google.com/finance/company_news?q=Nasdaq:MSFT&output=json"   
        
    d = feedparser.parse('https://www.google.com/finance/company_news?q=Nasdaq:MSFT&output=rss')
    
    html = d["entries"][0]["summary_detail"]
    value = html["value"]
    
    html_parser = MyHTMLParser()
    html_parser.feed(value)
    news_parser = html_parser.get_raw_news()

    html_parser = MyHTMLParser()
    html_parser.feed(d["entries"][0]["summary"])
    news_parser2 = html_parser.get_raw_news()

    #https://finance.yahoo.com/quote/INTC?ltr=1
    response = urllib.request.urlopen( url)
    result = response.read()
    str_result = result.decode("utf-8")
    
    poo = re.sub(r'([a-zA-Z_]+):',r'"\1":',str_result)
 
    pee = re.sub(r'(/"/")',r'"\1":',str_result)

    crap = re.sub(r'#([^\s\[\]\{\}\:\,]+):#', '"\1":', str_result );
    #json_data = ast.literal_eval(str_result)
    
    sresult = demjson.decode(str_result)
    
    python_obj = json.loads(poo)
    for key, value in python_obj["Time Series (1min)"].items():
        print( key );
        print( value["close"])
    print( str_result )

 
    
