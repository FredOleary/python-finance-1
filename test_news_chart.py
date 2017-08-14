#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  7 17:04:10 2017

@author: fredoleary
"""

from platform import python_version
from datetime import datetime  
from datetime import timedelta  
import sqlite3
from hashlib import blake2b

import matplotlib.pyplot as plt
import pandas as pd

stock_data = [{"symbol": "INTC", "description": "Intel Corporation" },
              {"symbol": "LITE", "description": "Lumentum Corporation" }]
if __name__ == "__main__":
    print('Python', python_version())
    
    symbol = "LITE"
    
    connnection = sqlite3.connect("FinanceDb")
 
    query = "SELECT * FROM news WHERE symbol = '%(symbol)s'"
 #   df = pd.read_sql( query, connnection, params={"symbol":"LITE"} )  
    df = pd.read_sql( query % {"symbol":symbol}, connnection )  
#    df.time = datetime.fromtimestamp(df.time)
    #print( df)
#   df.time = df.time/2
    #convert time, (stored as float 'timestamps' to date time)
    #df['time'] = df['time'].apply(lambda x: datetime.fromtimestamp(x))
    #print("------------------------")
       
    #grouped = df.groupby('time').count()
    x = df['time']
    y = df['weight']
    
    fig = plt.figure()
    fig.suptitle('Scatter Plot', fontsize=14, fontweight='bold')
    ax = fig.add_subplot(111)
    fig.subplots_adjust(top=0.85)

    ax.set_xlabel('Date/Time')
    ax.set_ylabel('Weight')


    ax.plot_date(x, y, xdate=True, ydate=False, color='skyblue')
    
    fig.autofmt_xdate()
    
    plt.show()
    #df.plot(kind='scatter',x='time',y='weight')
    
    print( df)
    