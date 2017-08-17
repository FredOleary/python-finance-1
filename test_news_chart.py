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
    CONNECTION = sqlite3.connect("FinanceDb")
    QUERY = "SELECT * FROM news WHERE symbol = '%(symbol)s'"
    DF = pd.read_sql(QUERY % {"symbol":SYMBOL}, CONNECTION)
    CONNECTION.close()

    FIG = plt.figure()
    FIG.suptitle('Scatter Plot', fontsize=14, fontweight='bold')
    SUB_PLOT = FIG.add_subplot(111)
    FIG.subplots_adjust(top=0.85)

    SUB_PLOT.set_xlabel('Date/Time')
    SUB_PLOT.set_ylabel('Weight')

    SUB_PLOT.plot_date(DF['time'], DF['weight'], xdate=True, ydate=False, color='skyblue')
    FIG.autofmt_xdate()
    plt.show()
