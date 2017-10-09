#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 17 14:52:15 2017

@author: fredoleary
"""
from dateutil import parser
import NewsClassifyEx
from DbFinance import FinanceDB
from CompanyList import CompanyWatch

class BiasWeights():
    """ Update news weights for all news items """
    def __init__(self, connection):
        self.connection = connection
        self.finance = None

    def update_weights(self):
        """ Iterate all news items and refresh weights"""
        companies = CompanyWatch()
        self.finance = FinanceDB(companies.get_companies())
        self.finance.initialize()

        rows = self.finance.get_news_with_sentiment()
        for row in rows:
            symbol = row[0]
            time = row[1]
            sentiment = row[8]
            if sentiment != "I":
                news_item = {"title":row[3], "description":row[4], "hash":row[7], "sentiment":sentiment}
                classify_news = NewsClassifyEx.ClassifyNews(symbol, news_item)
                sentiment = classify_news.classify()
                weight = self._bias_weight(symbol, time, sentiment)
                update_sql = "UPDATE news SET weight = ? WHERE hash = ? "
                cursor = self.connection.cursor()
                cursor.execute(update_sql, [weight, row[7]])
                cursor.close()
#            if sentiment != 0:
#                print("Found sentiment: ", sentiment, " title: ", html.unescape(row[3]))
        self.connection.commit()

    def _bias_weight(self, symbol, time, weight):
        """
        Bias the weight by the closest stock price.
        for example if at 2017-8-20 10:0:0 the price is 100 and the weight is -10%
        the biased weight would be 90. ((100 - 10% * 100)
        """
        price_before = None
        price_after = None

        rows = self.finance.get_prices_before(symbol, time)
        if rows:
            price_before = rows[0][2]
            time_before = rows[0][1]

        rows = self.finance.get_prices_after(symbol, time)
        if rows:
            price_after = rows[0][2]
            time_after = rows[0][1]
        if price_before is not None and price_after is not None:
            #Take closest time ?
            delta1 = time - time_before
            delta2 = time_after - time
            if delta1 < delta2:
                weighted_price = price_before
            else:
                weighted_price = price_after
        elif price_before is not None:
            weighted_price = price_before
        elif price_after is not None:
            weighted_price = price_after
        else:
            weighted_price = 0

        weight = weighted_price + (weight * weighted_price)/100
        return weight
