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
    FINANCE = FinanceDB(COMPANIES.get_companies())
    FINANCE.initialize()
    for COMPANY in COMPANIES.get_companies():
        print("Updating: ", COMPANY["symbol"], " ", COMPANY["description"])
        QUOTES = YahooFinanceNews.get_quotes_for_stock(COMPANY["symbol"])
        FINANCE.add_quotes(COMPANY["symbol"], QUOTES)
        print("Prices updated")
        NEWS = YahooFinanceNews.get_news_for_stock(COMPANY["symbol"])
        FINANCE.add_news(COMPANY["symbol"], NEWS)
        print("News updated")

    print("Done")
