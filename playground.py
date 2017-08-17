#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  7 17:04:10 2017

@author: fredoleary
"""

import sqlite3
from platform import python_version
from BiasWeight import BiasWeights

if __name__ == "__main__":
    print('Python', python_version())
    CONNECTION = sqlite3.connect("FinanceDb")
    bias = BiasWeights(CONNECTION)
    bias.update_weights()
    CONNECTION.close()
"""
    CURSOR = CONNECTION.cursor()
    SYMBOL = "MSFT"
    CURSOR.execute("SELECT * FROM news WHERE symbol = ?", [SYMBOL])
    ROWS = CURSOR.fetchall()
    for ROW in ROWS:
        bw.bias_weight(CONNECTION, SYMBOL, ROW[1], ROW[5])
    CONNECTION.close()
"""
