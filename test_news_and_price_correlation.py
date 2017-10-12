#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  7 17:04:10 2017

@author: fredoleary
"""

from platform import python_version
import sqlite3
import argparse
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

if __name__ == "__main__":
    print('Python', python_version())
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--ticker", help="Ticker to chart, (MSFT, AAPL..., Default=AAPL)", dest="ticker", default="AAPL")
    args = parser.parse_args()
    print("Ticker: ", args.ticker)

    SYMBOL = args.ticker
    
    # optional time filter - Use "" for none
    # Also 6:30am PST is 1:30pm GMT, (13:30:00) and 1:00pm PST is 8pm GMT (20:00:00)
#    TIME_FILTER =  "AND time BETWEEN '2017-09-26 13:30:00' AND '2017-09-26 20:00:00'"
    TIME_FILTER =  " AND time > '2017-09-26 13:30:00'"

    CONNECTION = sqlite3.connect("FinanceDb")

    QUERY = "SELECT time, weight FROM news WHERE symbol = '%(symbol)s' AND sentiment != 'I'"
    QUERY =  QUERY + TIME_FILTER
    DF_NEWS = pd.read_sql(QUERY % {"symbol":SYMBOL}, CONNECTION)
    
    QUERY = "SELECT time, price FROM prices WHERE symbol = '%(symbol)s'"
    QUERY =  QUERY + TIME_FILTER
    DF_PRICE = pd.read_sql(QUERY % {"symbol":SYMBOL}, CONNECTION)
    
    pd.set_option('display.max_rows', 5000)
    
    DF_MERGE = pd.merge(DF_PRICE, DF_NEWS, how='outer', on='time', left_on=None, right_on=None,
         left_index=False, right_index=False, sort=True,
         suffixes=('_x', '_y'), copy=True, indicator=False)
    
    DF_MERGE['price'] = DF_MERGE['price'].fillna(method='ffill')
    DF_MERGE['weight'] = DF_MERGE['weight'].fillna(method='ffill')

    # May need to bias the weight to better chart prices
    #DF_NEWS['weight'] = DF_NEWS['weight'].apply(lambda x: x+70)
    #print( DF_MERGE.iloc[:1000])
#    for index in range(len(DF_MERGE)):
#         if not np.isnan( DF_MERGE.iloc[index]['weight'] ):
#             print( DF_MERGE.iloc[index])
    FIG = plt.figure()
    FIG.suptitle( SYMBOL + '-Scatter/Line Plot', fontsize=14, fontweight='bold')
    AX_NEWS = FIG.add_subplot(111)
    FIG.subplots_adjust(top=0.85)
    AX_NEWS.set_xlabel('Date/Time')
    AX_NEWS.set_ylabel('Weight')
    AX_NEWS.plot_date(DF_MERGE['time'], DF_MERGE['weight'], 'b-', xdate=True, ydate=False, color='skyblue')
    
    if True:
        AX_PRICE = FIG.add_subplot(111)
        FIG.subplots_adjust(top=0.85)

        AX_PRICE.set_xlabel('Date/Time')
        AX_PRICE.set_ylabel('price')


        AX_PRICE.plot_date(DF_MERGE['time'], DF_MERGE['price'], 'b-', xdate=True, ydate=False, color='red')
    FIG.autofmt_xdate()
    plt.show()
