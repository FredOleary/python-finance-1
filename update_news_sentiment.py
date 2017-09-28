#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  7 17:04:10 2017

@author: fredoleary
"""
import html
from platform import python_version
from DbFinance import FinanceDB
from CompanyList import CompanyWatch

def get_news_without_sentiment(finance):
    """ Get rows where sentiment has not been set """
    rows = finance.get_without_sentiment()
    return rows

def update_sentiment(finance, rows):
    print("Records:", len(rows))
    for row in rows:
        choice_made = False
        while choice_made is False:
            print("----------------------------------------")
            print("Source: ", row[2],". Date: ", row[1], ". Title: ", html.unescape(row[3]))
            print("\nDescription: ", html.unescape(row[4]))
            sentiment = input("Sentiment: 'G=Good/Positive', 'B=Bad/Negative', 'N=Neutral', 'I=Ingore'").upper()
            if sentiment[0] == "G" or sentiment[0] == "B" or sentiment[0] == "N" or sentiment[0] == "I":
                choice_made = True
                finance.update_sentiment(row[7], sentiment[0])
            else:
                print("Invalid choice")
        
    
if __name__ == "__main__":
    print('Python', python_version())
    COMPANIES = CompanyWatch()
    FINANCE = FinanceDB(COMPANIES.get_companies())
    FINANCE.initialize()
    update_sentiment(FINANCE, get_news_without_sentiment(FINANCE))
    
    FINANCE.close()
    print("Done")
