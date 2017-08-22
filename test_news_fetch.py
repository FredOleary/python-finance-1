#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  7 17:04:10 2017

@author: fredoleary
"""

from platform import python_version
from DbFinance import FinanceDB
from CompanyList import CompanyWatch
from WebFinance import FinanceWeb


if __name__ == "__main__":
    print('Python', python_version())
    COMPANIES = CompanyWatch()
    SYMBOL = "LITE"
    FINANCE = FinanceDB(COMPANIES.get_companies())
    FINANCE.initialize()
    WEB= FinanceWeb()
    NEWS = WEB.get_news_for_stock(SYMBOL)
    FINANCE.add_news(SYMBOL, NEWS)
    FINANCE.close()
    print(NEWS)

