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
    
     
    connnection = sqlite3.connect("FinanceDb")
         
    test = "LITE"
    query = "SELECT * FROM prices WHERE symbol = '%(symbol)s'"
    df = pd.read_sql( query % {"symbol":test}, connnection )  
      
    grouped = df.groupby('time').count()
    x = df['time']
    y = df['price']
    
    fig = plt.figure()
    fig.suptitle('Scatter Plot', fontsize=14, fontweight='bold')
    ax = fig.add_subplot(111)
    fig.subplots_adjust(top=0.85)

    ax.set_xlabel('Date/Time')
    ax.set_ylabel('price')


    ax.plot_date(x, y, 'b-', xdate=True, ydate=False, color='skyblue')
    
    fig.autofmt_xdate()
    
    plt.show()
    