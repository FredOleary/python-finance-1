#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  8 19:35:54 2017

@author: fredoleary
"""
import re
import NewsKeywords

SPECIFIC_NEWS_MULTIPLIER = 10
MAX_WEIGHT = 100
MIN_WEIGHT = -100

class ClassifyNews():
    """
        Calculate the sentiment of the news_item
    """
    def __init__(self, symbol, name, newsItem):
        self.keywords = NewsKeywords.NewsKeywords().get_sentiment_dictionary()
        self.symbol = symbol
        self.name = name
        self.news_item = newsItem

    def classify(self):
        """
        returns a weigth between -100 and +100.
        -100 => really negative news
         0 => neutral news
        +100 => really positive news
        """
        weight = 0
        if self.news_item:
            weight = self._get_item_weight()
        return weight

    def _get_item_weight(self):
        multiplier = self._get_item_multiplier()
        sentiment = self._get_item_sentiment()
        sentiment = multiplier*sentiment
        if sentiment > MAX_WEIGHT:
            sentiment = MAX_WEIGHT
        elif sentiment < MIN_WEIGHT:
            sentiment = MIN_WEIGHT
        return sentiment

    # test if the news item explicity mentions the symbol
    def _get_item_multiplier(self):
        regex = r'\b'+ self.symbol + r'\b|\b' + self.name + r'\b'
        search_results = re.findall(regex, self.news_item["title"], re.I | re.X)
        if search_results:
            return SPECIFIC_NEWS_MULTIPLIER
        search_results = re.findall(regex, self.news_item["description"], re.I | re.X)
        if search_results:
            return SPECIFIC_NEWS_MULTIPLIER
        return 1

    def _get_item_sentiment(self):
        sentiment = 0
        for key, value in self.keywords.items():
            regex = self._create_reg_ex(key)
            search_title = re.findall(regex, self.news_item["title"], re.I | re.X)
            search_description = re.findall(regex, self.news_item["description"], re.I | re.X)
            if search_title or search_description:
                sentiment += value

        return sentiment

    def _create_reg_ex(self, term):
        """ Create approbriate expression"""
        tokens = term.split()
        if len(tokens) > 1:
            result = r''
            for token in tokens:
                result = result + token + r'\s'
            return result
        return r'\b'+ term + r'\b'
