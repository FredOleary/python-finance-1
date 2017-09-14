#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  7 17:04:10 2017

@author: fredoleary
"""

import sqlite3
import logging
import datetime
from platform import python_version
from WebFinance import FinanceWeb
from BiasWeight import BiasWeights
from DbFinance import FinanceDB
from CompanyList import CompanyWatch


if __name__ == "__main__":
    nowdt =  datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print('Python', python_version(), ' ', nowdt)
    logging.basicConfig(filename='UpdateAll.log', level=logging.INFO)
    logging.info('Pythonx ' + python_version() + ' ' + nowdt)
    COMPANIES = CompanyWatch()
    WEB= FinanceWeb()
    FINANCE = FinanceDB(COMPANIES.get_companies())
    FINANCE.initialize()
    for COMPANY in COMPANIES.get_companies():
        logging.info("Updating: " + COMPANY["symbol"] + " " + COMPANY["description"])

        QUOTES = WEB.get_quotes_for_stock(COMPANY["symbol"])
        FINANCE.add_quotes(COMPANY["symbol"], QUOTES)
        logging.info("Prices updated")

        NEWS = WEB.get_news_for_stock(COMPANY["symbol"])
        FINANCE.add_news(COMPANY["symbol"], NEWS, "Google")
        logging.info("News updated - Google aggregator")
        
        NEWS = WEB.get_news_for_stock_cf(COMPANY["symbol"])
        FINANCE.add_news(COMPANY["symbol"], NEWS, "City Falcon")
        logging.info("News updated - cityFalcon aggregator")

    FINANCE.close()

    CONNECTION = sqlite3.connect("FinanceDb")
    BIAS = BiasWeights(CONNECTION)
    BIAS.update_weights()
    CONNECTION.close()
    logging.info("Weights updated")

    logging.info("Done")
    print("Done")
