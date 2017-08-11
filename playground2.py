#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 11 10:26:16 2017

@author: fredoleary
"""
import urllib.request
import json

### alphavantage key M8KGCPCGZQSJJO3V

"""
https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=MSFT&interval=15min&outputsize=compact&apikey=M8KGCPCGZQSJJO3V
"""
if __name__ == "__main__":
    url =  "https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=MSFT&interval=1min&outputsize=compact&apikey=M8KGCPCGZQSJJO3V"   
        
    
    #https://finance.yahoo.com/quote/INTC?ltr=1
    response = urllib.request.urlopen( url)
    result = response.read()
    str_result = result.decode("utf-8")
    python_obj = json.loads(str_result)
    for key, value in python_obj["Time Series (1min)"].items():
        print( key );
        print( value["close"])
    print( str_result )

 