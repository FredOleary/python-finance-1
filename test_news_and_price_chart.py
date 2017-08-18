#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  7 17:04:10 2017

@author: fredoleary
"""

from platform import python_version
import sqlite3

import matplotlib.pyplot as plt
import pandas as pd

if __name__ == "__main__":
    print('Python', python_version())

    SYMBOL = "MSFT"
    
    # optional time filter - Use "" for none
    #TIME_FILTER =  "AND time BETWEEN '2017-08-11 18:57:00' AND '2017-08-11 19:05:00'")
    TIME_FILTER =  " AND time > '2017-08-17 00:00:00'"

    CONNECTION = sqlite3.connect("FinanceDb")

    QUERY = "SELECT * FROM news WHERE symbol = '%(symbol)s'"
    QUERY =  QUERY + TIME_FILTER
    DF_NEWS = pd.read_sql(QUERY % {"symbol":SYMBOL}, CONNECTION)

    # May need to bias the weight to better chart prices
    #DF_NEWS['weight'] = DF_NEWS['weight'].apply(lambda x: x+70)

    FIG = plt.figure()
    FIG.suptitle('Scatter/Line Plot', fontsize=14, fontweight='bold')
    AX_NEWS = FIG.add_subplot(111)
    FIG.subplots_adjust(top=0.85)
    AX_NEWS.set_xlabel('Date/Time')
    AX_NEWS.set_ylabel('Weight')
    AX_NEWS.plot_date(DF_NEWS['time'], DF_NEWS['weight'], xdate=True, ydate=False, color='skyblue')

    QUERY = "SELECT * FROM prices WHERE symbol = '%(symbol)s'"
    QUERY =  QUERY + TIME_FILTER

    DF = pd.read_sql(QUERY % {"symbol":SYMBOL}, CONNECTION)

    AX_PRICE = FIG.add_subplot(111)
    FIG.subplots_adjust(top=0.85)

    AX_PRICE.set_xlabel('Date/Time')
    AX_PRICE.set_ylabel('price')


    AX_PRICE.plot_date(DF['time'], DF['price'], 'b-', xdate=True, ydate=False, color='red')

    FIG.autofmt_xdate()

    plt.show()
