#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 14 18:47:23 2017

@author: fredoleary
Test various news classification functions

"""

import re
from platform import python_version

if __name__ == "__main__":
    print('Python', python_version())

    line = "Lumentum cats are smarter LITE dogs";
    
    searchResults = re.findall( r'\bLITE\b|\bLUMENTUM\b', line, re.I | re.X)
    
    
    if searchResults:
       print( "results : ", searchResults)
    else:
       print( "Nothing found!!")
