#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  7 17:04:10 2017

@author: fredoleary
"""

from platform import python_version
import sqlite3
from NewsKeywords import NewsKeywords

if __name__ == "__main__":
    print('Python', python_version())

    SYMBOL = "MSFT"
    CONNECTION = sqlite3.connect("FinanceDb")
    CURSOR = CONNECTION.cursor()
    CURSOR.execute("SELECT * FROM news")
    ROWS = CURSOR.fetchall()
    CURSOR.close()
    CONNECTION.close()
    KEYWORDS = NewsKeywords()
    LIST = []
    for ROW in ROWS:
        LIST.append({"title":ROW[3], "description":ROW[4], "hash":ROW[7]})
    KEYWORDS.update_news_items(LIST )
    DICTIONARY = KEYWORDS.get_dictionary()

    for key, value in sorted(DICTIONARY.items()):
        print(key)
   
    USE_WORDS = KEYWORDS.get_sentiment_dictionary()
    print("Dictionary length: ", len(DICTIONARY), " Use length: ", len(USE_WORDS))
    for key in USE_WORDS:
        if key in DICTIONARY:
            del DICTIONARY[key]
        
    print("New Dictionary length: ", len(DICTIONARY))
    WORDS_FILE = open("ignore_words.txt", "w") 
    for key, value in sorted(DICTIONARY.items()):
        WORDS_FILE.write(key + "\n")
    WORDS_FILE.close()
    print("Length: ", len(DICTIONARY))