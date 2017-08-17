#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  8 19:35:54 2017

@author: fredoleary
"""
import re

SPECIFIC_NEWS_MULTIPLIER = 10

class ClassifyNews():
    def __init__(self, symbol, name, newsItem ):
        self.symbol = symbol
        self.name = name
        self.news_item = newsItem
        
    # returns a weigth between -100 and +100. 
    # -100 => really negative news
    # 0 => neutral news
    # +100 => really positive news
    def classify( self ) :   
        weight = 0;
        if self.news_item :
            weight =  self._get_item_weight(self.news_item)
        return weight
        
    
    def _get_item_weight(self, news_item) :
        weight = 0
        multiplier = self._get_item_multiplier( news_item )
        return multiplier*weight
    
    # test if the news item explicity mentions the symbol
    def _get_item_multiplier( self, news_item):
        regex = r'\b'+ self.symbol + r'\b|\b' + self.name + r'\b'
        searchResults = re.findall( regex, news_item["title"], re.I | re.X)
        if searchResults :
            return SPECIFIC_NEWS_MULTIPLIER
        searchResults = re.findall( regex, news_item["description"], re.I | re.X)
        if searchResults :
            return SPECIFIC_NEWS_MULTIPLIER
        return 1
