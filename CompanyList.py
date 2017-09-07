#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 17 11:16:03 2017

@author: fredoleary
"""

class CompanyWatch():
    """ Declares the companies to be watched """
    def __init__(self):
        self.company_list = [{"symbol": "INTC", "description": "Intel Corporation"},
                             {"symbol": "LITE", "description": "Lumentum Corporation"},
                             {"symbol": "AAPL", "description": "Apple Corporation"},
                             {"symbol": "MSFT", "description": "Microsoft Corporation"}]
    def get_companies(self):
        """ Returns the companies """
        return self.company_list
