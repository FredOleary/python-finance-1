#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 17 14:52:15 2017

@author: fredoleary
"""
from dateutil import parser

class BiasWeights():
    """ Update news weights for all news items """
    def __init__(self, connection):
        self.connection = connection

    def update_weights(self):
        """ Iterate all news items and refresh weights"""
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM news")
        rows = cursor.fetchall()
        cursor.close()
        for row in rows:
            symbol = row[0]
            time = row[1]
            sentiment = 0   ## TODO Calculate sentiment!!
            weight = self._bias_weight(symbol, time, sentiment)
            update_sql = "UPDATE news SET weight = ? WHERE hash = ? "
            cursor = self.connection.cursor()
            cursor.execute(update_sql, [weight, row[6]])
            cursor.close()
            print(weight)
        self.connection.commit()
        
    def _bias_weight(self, symbol, time, weight):
        """
        Bias the weight by the closest stock price.
        for example if at 2017-8-20 10:0:0 the price is 100 and the weight is -10%
        the biased weight would be 90. ((100 - 10% * 100)
        """
        price_before = None
        price_after = None

        query = "SELECT * FROM prices WHERE symbol = ? AND time <= ? ORDER BY TIME DESC LIMIT 5"
        cursor = self.connection.cursor()
        cursor.execute(query, [symbol, time])
        rows = cursor.fetchall()
        if rows:
            price_before = rows[0][2]
            time_before = rows[0][1]

        query = "SELECT * FROM prices WHERE symbol = ? AND time >= ? ORDER BY TIME ASC LIMIT 5"
        cursor = self.connection.cursor()
        cursor.execute(query, [symbol, time])
        rows = cursor.fetchall()
        if rows:
            price_after = rows[0][2]
            time_after = rows[0][1]
        if price_before is not None and price_after is not None:
            #Take closest time ?
            time = parser.parse(time)
            time_before = parser.parse(time_before)
            time_after = parser.parse(time_after)
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
