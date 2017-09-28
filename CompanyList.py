#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 17 11:16:03 2017

@author: fredoleary
"""

class CompanyWatch():
    """ Declares the companies to be watched """
    def __init__(self):
        self.company_list = [{"symbol": "INTC", "description": "Intel Corporation", "name": "Intel"},
                             {"symbol": "LITE", "description": "Lumentum Corporation", "name": "Lumentum"},
                             {"symbol": "AAPL", "description": "Apple Corporation", "name": "Apple"},
                             {"symbol": "MSFT", "description": "Microsoft Corporation", "name": "Microsoft"}]
    def get_companies(self):
        """ Returns the companies """
        return self.company_list
