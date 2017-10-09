#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  7 17:04:10 2017

@author: fredoleary
"""

from platform import python_version
from BiasWeight import BiasWeights
from DbFinance import FinanceDB
from CompanyList import CompanyWatch

if __name__ == "__main__":
    print('Python', python_version())
    COMPANIES = CompanyWatch()
    FINANCE = FinanceDB(COMPANIES.get_companies())
    FINANCE.initialize()

    BIAS = BiasWeights(FINANCE)
    BIAS.update_weights()
