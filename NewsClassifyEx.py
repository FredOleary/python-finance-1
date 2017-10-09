#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  8 19:35:54 2017

@author: fredoleary
"""
import re
import NewsKeywords
import logging


SPECIFIC_NEWS_MULTIPLIER = 2
SENTIMENT_SCALER = .3
MAX_WEIGHT = 100
MIN_WEIGHT = -100

class ClassifyNews():
    """
        Calculate the sentiment of the news_item
    """
    def __init__(self, symbol, newsItem):
        self.symbol = symbol
        self.name = "XXX" # TODO - Stock name isn't known!!!
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
        sentiment = self._get_item_sentiment() * SENTIMENT_SCALER
        sentiment = multiplier*sentiment
#        if sentiment != 0:
#            print(sentiment, " ", html.unescape(self.news_item["title"]))
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
        if self.news_item["sentiment"] == "G":
            sentiment = 1
        elif self.news_item["sentiment"] == "B":
            sentiment = -1
        elif self.news_item["sentiment"] == "N":
            sentiment = 0
        else:
            logging.error("Invalid sentiment: " + self.newsItem["sentiment"])
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
