#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  7 17:04:10 2017

@author: fredoleary
"""

from platform import python_version
import YahooFinanceNews  
from DbFinance import FinanceDB
from datetime import datetime  


stock_data = [{"symbol": "INTC", "description": "Intel Corporation" },
              {"symbol": "LITE", "description": "Lumentum Corporation" }]
if __name__ == "__main__":
    print('Python', python_version())
    
    now = datetime.now()
    ts = now.timestamp()
    newNow = datetime.fromtimestamp(ts)
    
    symbol = "LITE"
    
    finance = FinanceDB(stock_data)
    finance.initialize()
    quotes = YahooFinanceNews.get_quotes_for_stock(symbol)
    print( quotes )
    finance.add_quotes( symbol, quotes)
    
    quotes =  finance.get_quotes( symbol)
    print( quotes )
#    news = YahooFinanceNews.get_news_for_stock("LITE")
#    finance.add_news( "LITE", news)
#    print( news)
    
    
