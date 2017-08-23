#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 14 19:22:00 2017

@author: fredoleary
"""
import unittest
from platform import python_version
from NewsKeywords import NewsKeywords

class SimplisticTest(unittest.TestCase):
    """ Unit tests for news classifiaction"""
    def test(self):
        """ Run news keywords tests """

        # Same title/description - different hash.
        keywords = NewsKeywords()
        news_item = {"symbol":"INTC", "title":"This contains four words", "description":"Three words here", "hash":"12345"}
        keywords.update_keywords(news_item)
        dictionary = keywords.get_dictionary()
        self.assertTrue(len(dictionary) == 6)
        self.assertTrue(dictionary["words"]["count"] == 2)

        news_item = {"symbol":"INTC", "title":"This contains four words", "description":"Three words here", "hash":"5678"}
        keywords.update_keywords(news_item)
        dictionary = keywords.get_dictionary()
        self.assertTrue(len(dictionary) == 6)
        self.assertTrue(dictionary["words"]["count"] == 4)
        
        # Mix of upper lower case
        keywords = NewsKeywords()
        news_item = {"symbol":"INTC", "title":"This Contains Four Words", "description":"This Contains Four Words", "hash":"12345"}
        keywords.update_keywords(news_item)
        dictionary = keywords.get_dictionary()
        self.assertTrue(len(dictionary) == 4)
        self.assertTrue(dictionary["words"]["count"] == 2)
        self.assertTrue(dictionary["contains"]["count"] == 2)
        self.assertFalse("This" in dictionary)
 
        # Ignore words
        keywords = NewsKeywords()
        keywords.add_ignore_word("THIS")
        news_item = {"symbol":"INTC", "title":"This Contains Four Words", "description":"This Contains Four Words", "hash":"12345"}
        keywords.update_keywords(news_item)
        dictionary = keywords.get_dictionary()
        self.assertTrue(len(dictionary) == 3)
        self.assertTrue(dictionary["words"]["count"] == 2)
        self.assertTrue(dictionary["contains"]["count"] == 2)
        self.assertFalse("this" in dictionary)
     

if __name__ == "__main__":
    print('Python', python_version())

    unittest.main()
