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

stock_data = [{"symbol": "INTC", "description": "Intel Corporation" },
              {"symbol": "LITE", "description": "Lumentum Corporation" }]
if __name__ == "__main__":
    print('Python', python_version())
    
    symbol = "INTC"
    
    connnection = sqlite3.connect("FinanceDb")
 
    query = "SELECT * FROM news WHERE symbol = '%(symbol)s'"
    df_news = pd.read_sql( query % {"symbol":symbol}, connnection )  
    
    # May need to bias the weight to better chart prices
    df_news['weight'] = df_news['weight'].apply(lambda x: x+53)

    x = df_news['time']
    y = df_news['weight']
    
    fig = plt.figure()
    fig.suptitle('Scatter/Line Plot', fontsize=14, fontweight='bold')
    ax_news = fig.add_subplot(111)
    fig.subplots_adjust(top=0.85)

    ax_news.set_xlabel('Date/Time')
    ax_news.set_ylabel('Weight')


    ax_news.plot_date(x, y, xdate=True, ydate=False, color='skyblue')
    
    
    query = "SELECT * FROM prices WHERE symbol = '%(symbol)s'"
    df = pd.read_sql( query % {"symbol":symbol}, connnection )  
      
    ax_price = fig.add_subplot(111)
    fig.subplots_adjust(top=0.85)

    ax_price.set_xlabel('Date/Time')
    ax_price.set_ylabel('price')


    ax_price.plot_date(df['time'], df['price'], 'b-', xdate=True, ydate=False, color='red')
   
    fig.autofmt_xdate()
    
    plt.show()
    
     