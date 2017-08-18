#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  7 17:04:10 2017

@author: fredoleary
"""

from platform import python_version
import YahooFinanceNews
from DbFinance import FinanceDB
from CompanyList import CompanyWatch


if __name__ == "__main__":
    print('Python', python_version())
    COMPANIES = CompanyWatch()
    SYMBOL = "LITE"
    FINANCE = FinanceDB(COMPANIES.get_companies())
    FINANCE.initialize()
    QUOTES = YahooFinanceNews.get_quotes_for_stock(SYMBOL)
    # print( quotes )
    FINANCE.add_quotes(SYMBOL, QUOTES)
    FINANCE.close()
    QUOTES = FINANCE.get_quotes(SYMBOL)
