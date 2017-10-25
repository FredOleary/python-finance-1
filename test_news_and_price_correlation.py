#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  7 17:04:10 2017

@author: fredoleary
"""

from platform import python_version
import sqlite3
import argparse
import matplotlib.pyplot as plt
import pandas as pd
import dateutil.parser
from datetime import timedelta  
import math

def pad_news( df_in, column_name ):
    """ pad news/price data_frame on minute boundry using linear extrapolation"""
    print("Extrapolating:", column_name)
    print("")
    next_index = 1
    df_out = pd.DataFrame({})
    while next_index < len(df_in):
        df_begin = pd.DataFrame([[df_in.loc[next_index-1,"time"],df_in.loc[next_index-1,column_name]]], columns=['time', column_name])
        df_out = df_out.append(df_begin, ignore_index=True)
        start_time = df_begin.loc[0,"time"]
        dt_start = dateutil.parser.parse(start_time)
        
        df_end = pd.DataFrame([[df_in.loc[next_index,"time"],df_in.loc[next_index,column_name]]], columns=['time', column_name])
        end_time = df_end.loc[0,"time"]
        dt_end = dateutil.parser.parse(end_time)
        delta = dt_end - dt_start
        diff_seconds = range_seconds = delta.total_seconds()
        delta_seconds = 0
        range_weight = df_end.loc[0, column_name] - df_begin.loc[0, column_name]
        while diff_seconds > 60:
            sec_delta = 60 - dt_start.second
            delta_seconds += sec_delta
            """ Algoritm delta_seconds/range_seconds = delta_weigth/range_weight"""
            delta_weigth = (delta_seconds/range_seconds)*range_weight
            extrap_weight  = delta_weigth + df_begin.loc[0, column_name]
            dt_start = dt_start + timedelta(seconds=sec_delta)
            df_append = pd.DataFrame([[dt_start.strftime("%Y-%m-%d %H:%M:%S"),extrap_weight]], columns=['time', column_name])
            df_out = df_out.append(df_append, ignore_index=True)
            diff_seconds -= sec_delta
            
        next_index += 1
    return df_out

def fill_price_na(df_m):
    """ fill NaNs in the price column where news item has fractional seconds
        The merge of Price and News will create nans in the price column when
        news is not on a minute boundry"""
    index = 0
    while (index+2) < len(df_m):
        first = df_m.loc[index, "price"]
        second = df_m.loc[index+1, "price"]
        third = df_m.loc[index+2, "price"]
        if not math.isnan(first) and \
           math.isnan(second) and \
           not math.isnan(third):
               df_m.loc[index+1, "price"] = (first+third)/2
        index +=1            
def create_figure( df_merge, symbol, shift):
    fig = plt.figure()
    fig.suptitle( symbol + '-Line Plot. Price shift: ' + str(shift), fontsize=14, fontweight='bold')
    ax_plot = fig.add_subplot(111)
    ax_plot.set_xlabel('Date/Time') 
    ax_plot.set_ylabel('Price/Weight')
    
    #AX_PRICE = FIG.add_subplot(111)

    ax_plot.plot_date(df_merge['time'], df_merge['price'], '-', xdate=True, ydate=False, color='red')
    ax_plot.plot_date(df_merge['time'], df_merge['weight'], '-', xdate=True, ydate=False, color='green')
    ax_plot.plot_date(df_merge['time'], df_merge['price'].shift(best_shift), '-', xdate=True, ydate=False, color='blue')
    fig.autofmt_xdate()
    return fig
     
def eval_best_correlation(df_merge):
    max_correlation = 0
    best_shift = 0
    for shift in range(1000):
        correlation = df_merge['price'].shift(-shift).corr(df_merge['weight'])
        if correlation > max_correlation:
            max_correlation = correlation
            best_shift = -shift
    for shift in range(1000):
        correlation = df_merge['price'].shift(shift).corr(df_merge['weight'])
        if correlation > max_correlation:
            max_correlation = correlation
            best_shift = shift
    return  max_correlation, best_shift
    
if __name__ == "__main__":
    print('Python', python_version())
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--ticker", help="Ticker to chart, (MSFT, AAPL..., Default=AAPL)", dest="ticker", default="AAPL")
    parser.add_argument("-s", "--start", help="Start Time, (2017-10-09 00:00:00, Default=none)", dest="start", default= "2017-10-16 20:00:00")
    parser.add_argument("-e", "--end", help="End Time, (2017-10-09 20:00:00, Default=none)", dest="end", default= "2017-10-24 20:00:00")
    args = parser.parse_args()
    print("Ticker: ", args.ticker)

    SYMBOL = args.ticker
    pd.set_option('display.max_rows', 5000)
    
    # optional time filter - Use "" for none
    # Also 6:30am PST is 1:30pm GMT, (13:30:00) and 1:00pm PST is 8pm GMT (20:00:00)
#    TIME_FILTER =  "AND time BETWEEN '2017-09-26 13:30:00' AND '2017-09-26 20:00:00'"
    TIME_FILTER = ""
    if args.start is not None and args.end is None:
        TIME_FILTER = " AND time >= '" + args.start + "'"
    elif args.start is None and args.end is not None:    
        TIME_FILTER = " AND time  <= '" + args.end + "'"
    elif args.start is not None and args.end is not None:    
        TIME_FILTER =  " AND time BETWEEN '" + args.start + "' AND '" + args.end + "'"

    CONNECTION = sqlite3.connect("FinanceDb")

    QUERY = "SELECT time, weight FROM news WHERE symbol = '%(symbol)s' AND sentiment != 'I' AND sentiment != 'N'"
    QUERY =  QUERY + TIME_FILTER
    QUERY =  QUERY + " ORDER BY time"
    print("Query:" + QUERY)
    DF_NEWS = pd.read_sql(QUERY % {"symbol":SYMBOL}, CONNECTION)
    DF_NEWS = pad_news(DF_NEWS, 'weight')
    
    QUERY = "SELECT time, price FROM prices WHERE symbol = '%(symbol)s'"
    QUERY =  QUERY + TIME_FILTER
    QUERY =  QUERY + " ORDER BY time"
    DF_PRICE = pd.read_sql(QUERY % {"symbol":SYMBOL}, CONNECTION)
    DF_PRICE = pad_news(DF_PRICE, 'price')
    
    
    DF_MERGE = pd.merge(DF_PRICE, DF_NEWS, how='outer', on='time', left_on=None, right_on=None,
         left_index=False, right_index=False, sort=True,
         suffixes=('_x', '_y'), copy=True, indicator=True)
    
    fill_price_na(DF_MERGE)
    
    max_correlation, best_shift = eval_best_correlation(DF_MERGE)
    
    FIG1 = create_figure( DF_MERGE, SYMBOL,  best_shift)        
    FIG1.show()
    
    print("Best price Shift:", best_shift, "Correlation:", max_correlation )

    input()
    
  
    
