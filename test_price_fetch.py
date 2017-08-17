#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  7 17:04:10 2017

@author: fredoleary
"""

from platform import python_version
import YahooFinanceNews
from DbFinance import FinanceDB


STOCK_DATA = [{"symbol": "INTC", "description": "Intel Corporation"},
              {"symbol": "LITE", "description": "Lumentum Corporation"},
              {"symbol": "MSFT", "description": "Microsoft Corporation"}]

if __name__ == "__main__":
    print('Python', python_version())
    SYMBOL = "MSFT"
    FINANCE = FinanceDB(STOCK_DATA)
    FINANCE.initialize()
    QUOTES = YahooFinanceNews.get_quotes_for_stock(SYMBOL)
    # print( quotes )
    FINANCE.add_quotes(SYMBOL, QUOTES)
    QUOTES = FINANCE.get_quotes(SYMBOL)
